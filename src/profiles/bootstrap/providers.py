from collections.abc import AsyncIterator

from alembic.config import Config as AlembicConfig
from bazario.asyncio import Dispatcher, Registry
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import (
    Provider,
    Scope,
    WithParents,
    alias,
    from_context,
    provide,
    provide_all,
)
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from taskiq_aio_pika.broker import AioPikaBroker
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from profiles.application.common.behaviors.commition_behavior import (
    CommitionBehavior,
)
from profiles.application.common.behaviors.event_id_generation_behavior import (
    EventIdGenerationBehavior,
)
from profiles.application.common.behaviors.event_publishing_behavior import (
    EventPublishingBehavior,
)
from profiles.application.common.markers.command import Command
from profiles.application.operations.read.load_profile_by_profile_id import (
    LoadProfileById,
    LoadProfileByIdHandler,
)
from profiles.application.operations.write.create_profile import (
    CreateProfile,
    CreateProfileHandler,
)
from profiles.application.operations.write.delete_profile import (
    DeleteProfile,
    DeleteProfileHandler,
)
from profiles.application.operations.write.update_info import (
    UpdateInfo,
    UpdateInfoHandler,
)
from profiles.application.ports.committer import Committer
from profiles.bootstrap.config import (
    DatabaseConfig,
    RabbitmqConfig,
)
from profiles.domain.shared.events import DomainEvent
from profiles.infrastructure.domain_events import DomainEvents
from profiles.infrastructure.outbox.adapters.rabbitmq_outbox_publisher import (
    RabbitmqOutboxPublisher,
)
from profiles.infrastructure.outbox.outbox_processor import OutboxProcessor
from profiles.infrastructure.outbox.outbox_publisher import OutboxPublisher
from profiles.infrastructure.outbox.outbox_storing_handler import (
    OutboxStoringHandler,
)
from profiles.infrastructure.persistence.adapters.sql_outbox_gateway import (
    SqlOutboxGateway,
)
from profiles.infrastructure.persistence.adapters.sql_profile_gateway import (
    SqlProfileGateway,
)
from profiles.infrastructure.persistence.adapters.sql_profile_repository import (
    SqlProfileRepository,
)
from profiles.infrastructure.persistence.transaction import Transaction
from profiles.infrastructure.profile_factory import ProfileFactoryImpl
from profiles.infrastructure.utc_time_provider import UtcTimeProvider
from profiles.infrastructure.uuid7_id_generator import UUID7IdGenerator
from profiles.presentation.api.htpp_identity_provider import HttpIdentityProvider


class ApiConfigProvider(Provider):
    scope = Scope.APP

    rabbitmq_config = from_context(RabbitmqConfig)
    database_config = from_context(DatabaseConfig)


class PersistenceProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    async def engine(self, postgres_config: DatabaseConfig) -> AsyncIterator[AsyncEngine]:
        engine = create_async_engine(postgres_config.uri)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

    @provide(provides=AsyncSession)
    async def session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_maker() as session:
            yield session


class DomainAdaptersProvider(Provider):
    scope = Scope.REQUEST

    repositories = provide_all(
        WithParents[SqlProfileRepository],  # type: ignore[misc]
    )
    domain_events = provide(WithParents[DomainEvents])  # type: ignore[misc]
    profile_factory = provide(WithParents[ProfileFactoryImpl])  # type: ignore[misc]


class ApplicationAdaptersProvider(Provider):
    scope = Scope.REQUEST

    gateways = provide_all(
        WithParents[SqlProfileGateway],  # type: ignore[misc]
        WithParents[SqlOutboxGateway],  # type: ignore[misc]
    )
    id_generator = provide(
        WithParents[UUID7IdGenerator],  # type: ignore[misc]
        scope=Scope.APP,
    )
    time_provider = provide(
        WithParents[UtcTimeProvider],  # type: ignore[misc]
        scope=Scope.APP,
    )
    committer = alias(AsyncSession, provides=Committer)


class InfrastructureAdaptersProvider(Provider):
    scope = Scope.REQUEST

    transaction = alias(AsyncSession, provides=Transaction)


class ApplicationHandlersProvider(Provider):
    scope = Scope.REQUEST

    hanlers = provide_all(
        OutboxStoringHandler,
        CreateProfileHandler,
        UpdateInfoHandler,
        DeleteProfileHandler,
        LoadProfileByIdHandler,
    )
    behaviors = provide_all(
        CommitionBehavior,
        EventPublishingBehavior,
        EventIdGenerationBehavior,
    )


class BazarioProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def registry(self) -> Registry:
        registry = Registry()

        registry.add_request_handler(CreateProfile, CreateProfileHandler)
        registry.add_request_handler(UpdateInfo, UpdateInfoHandler)
        registry.add_request_handler(DeleteProfile, DeleteProfileHandler)
        registry.add_request_handler(LoadProfileById, LoadProfileByIdHandler)
        registry.add_notification_handlers(DomainEvent, OutboxStoringHandler)
        registry.add_pipeline_behaviors(DomainEvent, EventIdGenerationBehavior)
        registry.add_pipeline_behaviors(
            Command,
            EventPublishingBehavior,
            CommitionBehavior,
        )

        return registry

    resolver = provide(WithParents[DishkaResolver])  # type: ignore[misc]
    dispatcher = provide(WithParents[Dispatcher])  # type: ignore[misc]


class CliConfigProvider(Provider):
    scope = Scope.APP

    alembic_config = from_context(AlembicConfig)
    uvicorn_config = from_context(UvicornConfig)
    uvicorn_server = from_context(UvicornServer)
    taskiq_broker = from_context(AioPikaBroker)


class BrokerProvider(Provider):
    scope = Scope.APP

    faststream_rabbit_broker = from_context(RabbitBroker)


class OutboxProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def outbox_publisher(
        self,
        broker: RabbitBroker,
    ) -> OutboxPublisher:
        return RabbitmqOutboxPublisher(broker=broker)

    @provide
    async def outbox_processor(
        self,
        transaction: Transaction,
        outbox_gateway: SqlOutboxGateway,
        outbox_publisher: OutboxPublisher,
    ) -> OutboxProcessor:
        return OutboxProcessor(
            transaction=transaction,
            outbox_gateway=outbox_gateway,
            outbox_publisher=outbox_publisher,
        )


class AuthProvider(Provider):
    scope = Scope.REQUEST

    identity_provider = provide(
        WithParents[HttpIdentityProvider],  # type: ignore[misc]
    )

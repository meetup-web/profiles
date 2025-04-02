from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.faststream import (
    setup_dishka as add_container_to_faststream,
)
from faststream import ContextRepo, FastStream
from faststream.rabbit.broker import RabbitBroker

from profiles.bootstrap.config import get_database_config, get_rabbitmq_config
from profiles.bootstrap.container import (
    bootstrap_api_container as bootstrap_stream_container,
)
from profiles.infrastructure.persistence.sql_tables import (
    map_outbox_table,
    map_profile_table,
)
from profiles.presentation.stream.exception_handlers import fastream_exception_middleware
from profiles.presentation.stream.routers.profiles import PROFILE_ROUTER


@asynccontextmanager
async def lifespan(context: ContextRepo) -> AsyncGenerator[None, None]:
    map_outbox_table()
    map_profile_table()

    yield


def add_middlewares(broker: RabbitBroker) -> None:
    broker.add_middleware(middleware=fastream_exception_middleware())


def add_consumers(broker: RabbitBroker) -> None:
    broker.include_router(PROFILE_ROUTER)


def bootstrap_stream() -> FastStream:
    rabbit_config = get_rabbitmq_config()
    broker = RabbitBroker(rabbit_config.uri)

    add_middlewares(broker=broker)
    add_consumers(broker=broker)

    application = FastStream(broker=broker, lifespan=lifespan)
    container = bootstrap_stream_container(
        rabbitmq_config=rabbit_config,
        database_config=get_database_config(),
    )
    add_container_to_faststream(container=container, app=application)

    return application

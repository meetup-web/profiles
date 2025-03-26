from bazario.asyncio import HandleNext, PipelineBehavior

from users.application.models.user import UserReadModel
from users.application.operations.write.create_user import CreateUser
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_factory import SessionFactory
from users.infrastructure.auth.session_login_handler import Login
from users.infrastructure.auth.session_provider import SessionStorer
from users.infrastructure.auth.session_read_model import SessionReadModel
from users.infrastructure.auth.session_repository import SessionRepository


class UserCreatedBehavior(PipelineBehavior[CreateUser, UserId]):
    def __init__(
        self,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
        session_storer: SessionStorer,
    ) -> None:
        self._session_factory = session_factory
        self._sesion_repository = session_repository
        self._session_storer = session_storer

    async def handle(
        self, request: CreateUser, handle_next: HandleNext[CreateUser, UserId]
    ) -> UserId:
        user_id = await handle_next(request)

        session = self._session_factory.create_session(
            user_id=user_id, user_role=UserRole.USER
        )

        self._sesion_repository.add(session)
        self._session_storer.store_session_id(
            SessionReadModel(
                session.entity_id, session.user_id, session.user_role, session.expires_at
            )
        )

        return user_id


class UserLoggedInBehavior(PipelineBehavior[Login, UserReadModel]):
    def __init__(
        self,
        session_factory: SessionFactory,
        session_repository: SessionRepository,
        session_storer: SessionStorer,
    ) -> None:
        self._session_factory = session_factory
        self._sesion_repository = session_repository
        self._session_storer = session_storer

    async def handle(
        self, request: Login, handle_next: HandleNext[Login, UserReadModel]
    ) -> UserReadModel:
        user = await handle_next(request)

        session = self._session_factory.create_session(
            user_id=user.user_id, user_role=user.user_role
        )

        self._sesion_repository.add(session)
        self._session_storer.store_session_id(
            SessionReadModel(
                session.entity_id, session.user_id, session.user_role, session.expires_at
            )
        )

        return user

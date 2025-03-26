from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.query import Query
from users.application.ports.context.identity_provider import IdentityProvider
from users.infrastructure.auth.session_gateway import SessionGateway
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_read_model import SessionReadModel


@dataclass(frozen=True)
class GetSessionById(Query[SessionReadModel]):
    session_id: SessionId


class GetSessionByIdHandler(RequestHandler[GetSessionById, SessionReadModel]):
    def __init__(self, session_gateway: SessionGateway) -> None:
        self._session_gateway = session_gateway

    async def handle(self, request: GetSessionById) -> SessionReadModel:
        session = await self._session_gateway.with_session_id(request.session_id)

        if not session:
            raise ApplicationError(
                message="Invalid session", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return session


@dataclass(frozen=True)
class GetUserSessions(Query[list[SessionReadModel]]): ...


class GetUserSessionsHandler(RequestHandler[GetUserSessions, list[SessionReadModel]]):
    def __init__(self, gateway: SessionGateway, idp: IdentityProvider) -> None:
        self._session_gateway = gateway
        self._identity_provider = idp

    async def handle(self, request: GetUserSessions) -> list[SessionReadModel]:
        current_user_id = await self._identity_provider.current_user_id()
        sessions = await self._session_gateway.with_user_id(user_id=current_user_id)

        return sessions

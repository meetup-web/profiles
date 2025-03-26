from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.command import Command
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_repository import SessionRepository


@dataclass(frozen=True)
class Logout(Command[None]):
    session_id: SessionId


class LogoutHandler(RequestHandler[Logout, None]):
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository = session_repository

    async def handle(self, request: Logout) -> None:
        session = await self._session_repository.with_session_id(
            session_id=request.session_id
        )

        if not session:
            raise ApplicationError(
                error_type=ErrorType.AUTHORIZATION_ERROR, message="Unauthorized"
            )

        self._session_repository.delete(session)

from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.command import Command
from users.application.ports.time_provider import TimeProvider
from users.domain.user.repository import UserRepository
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId


@dataclass(frozen=True)
class ChangeUserRole(Command[None]):
    user_id: UserId
    user_role: UserRole


class ChangeUserRoleHandler(RequestHandler[ChangeUserRole, None]):
    def __init__(
        self, user_repository: UserRepository, time_provider: TimeProvider
    ) -> None:
        self._user_repository = user_repository
        self._time_provider = time_provider

    async def handle(self, request: ChangeUserRole) -> None:
        user = await self._user_repository.with_id(request.user_id)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="User not found"
            )

        user.change_role(
            role=request.user_role, current_date=self._time_provider.provide_current()
        )

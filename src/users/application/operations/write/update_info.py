from dataclasses import dataclass
from datetime import date

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.command import Command
from users.application.ports.context.identity_provider import IdentityProvider
from users.application.ports.time_provider import TimeProvider
from users.domain.user.repository import UserRepository
from users.domain.user.value_objects import Fullname


@dataclass(frozen=True)
class UpdateInfo(Command[None]):
    fullname: Fullname
    birth_date: date | None


class UpdateInfoHandler(RequestHandler[UpdateInfo, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        time_provider: TimeProvider,
        identity_provider: IdentityProvider,
    ) -> None:
        self._user_repository = user_repository
        self._time_provider = time_provider
        self._identity_provider = identity_provider

    async def handle(self, request: UpdateInfo) -> None:
        user_id = await self._identity_provider.current_user_id()

        user = await self._user_repository.with_id(user_id)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="User not found"
            )

        user.update_user_info(
            birth_date=request.birth_date,
            fullname=request.fullname,
            current_date=self._time_provider.provide_current(),
        )

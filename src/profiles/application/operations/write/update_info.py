from dataclasses import dataclass
from datetime import date

from bazario.asyncio import RequestHandler

from profiles.application.common.application_error import ApplicationError, ErrorType
from profiles.application.common.markers.command import Command
from profiles.application.ports.identity_provider import IdentityProvider
from profiles.application.ports.time_provider import TimeProvider
from profiles.domain.profile.repository import ProfileRepository
from profiles.domain.profile.value_objects import Fullname


@dataclass(frozen=True)
class UpdateInfo(Command[None]):
    fullname: Fullname
    birth_date: date | None


class UpdateInfoHandler(RequestHandler[UpdateInfo, None]):
    def __init__(
        self,
        profile_repository: ProfileRepository,
        time_provider: TimeProvider,
        identity_provider: IdentityProvider,
    ) -> None:
        self._user_repository = profile_repository
        self._time_provider = time_provider
        self._identity_provider = identity_provider

    async def handle(self, request: UpdateInfo) -> None:
        user_id = self._identity_provider.current_user_id()

        profile = await self._user_repository.with_user_id(user_id)

        if not profile:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="User not found"
            )

        profile.update_profile_info(
            birth_date=request.birth_date,
            fullname=request.fullname,
            current_date=self._time_provider.provide_current(),
        )

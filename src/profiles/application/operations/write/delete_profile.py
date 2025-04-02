from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from profiles.application.common.application_error import ApplicationError, ErrorType
from profiles.application.common.markers.command import Command
from profiles.application.ports.identity_provider import IdentityProvider
from profiles.application.ports.time_provider import TimeProvider
from profiles.domain.profile.events import ProfileDeleted
from profiles.domain.profile.repository import ProfileRepository
from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class DeleteProfile(Command[None]):
    user_id: UserId


class DeleteProfileHandler(RequestHandler[DeleteProfile, None]):
    def __init__(
        self,
        profile_repository: ProfileRepository,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
    ) -> None:
        self._profile_repository = profile_repository
        self._identity_provider = identity_provider
        self._time_provider = time_provider

    async def handle(self, request: DeleteProfile) -> None:
        profile = await self._profile_repository.with_user_id(request.user_id)

        if not profile:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Profile not found"
            )

        event = ProfileDeleted(
            profile_id=profile.entity_id, event_date=self._time_provider.provide_current()
        )
        profile.add_event(event)

        await self._profile_repository.delete(profile)

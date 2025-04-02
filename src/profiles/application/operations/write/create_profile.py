from dataclasses import dataclass
from typing import Final

from bazario.asyncio import RequestHandler

from profiles.application.common.markers.command import Command
from profiles.application.ports.time_provider import TimeProvider
from profiles.domain.profile.factory import ProfileFactory
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.repository import ProfileRepository
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class CreateProfile(Command[ProfileId]):
    user_id: UserId


class CreateProfileHandler(RequestHandler[CreateProfile, ProfileId]):
    _DEFAULT_FIRSTNAME: Final[str] = "AnonymousUser"

    def __init__(
        self,
        profile_factory: ProfileFactory,
        time_provider: TimeProvider,
        profile_repository: ProfileRepository,
    ) -> None:
        self._user_factory = profile_factory
        self._time_provider = time_provider
        self._profile_repository = profile_repository

    async def handle(self, request: CreateProfile) -> ProfileId:
        profile = await self._user_factory.create_profile(
            fullname=Fullname(first_name=self._DEFAULT_FIRSTNAME), user_id=request.user_id
        )

        self._profile_repository.add(profile)

        return profile.entity_id

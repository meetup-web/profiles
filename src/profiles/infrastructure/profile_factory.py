from datetime import date

from profiles.application.common.application_error import ApplicationError, ErrorType
from profiles.application.ports.id_generator import IdGenerator
from profiles.application.ports.time_provider import TimeProvider
from profiles.domain.profile.events import ProfileCreated
from profiles.domain.profile.factory import ProfileFactory
from profiles.domain.profile.profile import Profile
from profiles.domain.profile.repository import ProfileRepository
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.events import DomainEventAdder
from profiles.domain.shared.user_id import UserId


class ProfileFactoryImpl(ProfileFactory):
    def __init__(
        self,
        profile_repository: ProfileRepository,
        event_adder: DomainEventAdder,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
    ) -> None:
        self._profile_repository = profile_repository
        self._time_provider = time_provider
        self._event_adder = event_adder
        self._id_generator = id_generator

    async def create_profile(
        self, *, fullname: Fullname, birth_date: date | None = None, user_id: UserId
    ) -> Profile:
        if await self._profile_repository.with_user_id(user_id):
            raise ApplicationError(
                message="Profile already exists", error_type=ErrorType.ALREADY_EXISTS
            )

        profile = Profile(
            entity_id=self._id_generator.generate_profile_id(),
            owner_id=user_id,
            event_adder=self._event_adder,
            birth_date=birth_date,
            fullname=fullname,
            created_at=self._time_provider.provide_current(),
        )

        event = ProfileCreated(
            profile_id=profile.entity_id,
            user_id=user_id,
            fullname=fullname,
            birth_date=birth_date,
            event_date=self._time_provider.provide_current(),
        )

        profile.add_event(event)

        return profile

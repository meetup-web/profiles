from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from profiles.domain.profile.profile import Profile
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.repository import ProfileRepository
from profiles.domain.shared.events import DomainEventAdder
from profiles.domain.shared.user_id import UserId
from profiles.infrastructure.persistence.sql_tables import PROFILES_TABLE


class SqlProfileRepository(ProfileRepository):
    def __init__(
        self,
        session: AsyncSession,
        event_adder: DomainEventAdder,
    ) -> None:
        self._session = session
        self._event_adder = event_adder

    def add(self, profile: Profile) -> None:
        self._session.add(profile)

    async def delete(self, profile: Profile) -> None:
        await self._session.delete(profile)

    async def with_profile_id(self, profile_id: ProfileId) -> Profile | None:
        profile = await self._session.get(Profile, profile_id)

        if profile is None:
            return None

        return self._load(profile)

    async def with_user_id(self, user_id: UserId) -> Profile | None:
        stmt = select(Profile).where(PROFILES_TABLE.c.user_id == user_id)
        profile = (await self._session.execute(stmt)).scalars().first()

        if profile is None:
            return None

        return self._load(profile)

    def _load(self, profile: Profile) -> Profile:
        profile.__setattr__("_event_adder", self._event_adder)
        return profile

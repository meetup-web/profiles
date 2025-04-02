from abc import ABC, abstractmethod

from profiles.domain.profile.profile import Profile
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.shared.user_id import UserId


class ProfileRepository(ABC):
    @abstractmethod
    def add(self, user: Profile) -> None: ...
    @abstractmethod
    async def delete(self, profile: Profile) -> None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> Profile | None: ...
    @abstractmethod
    async def with_profile_id(self, profile_id: ProfileId) -> Profile | None: ...

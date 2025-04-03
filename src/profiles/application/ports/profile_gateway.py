from abc import ABC, abstractmethod

from profiles.application.models.profile import ProfileReadModel
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.shared.user_id import UserId


class ProfileGateway(ABC):
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> ProfileReadModel | None: ...
    @abstractmethod
    async def with_profile_id(self, profile_id: ProfileId) -> ProfileReadModel | None: ...
    @abstractmethod
    async def with_user_ids(self, user_ids: list[UserId]) -> list[ProfileReadModel]: ...

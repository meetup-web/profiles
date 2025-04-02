from abc import ABC, abstractmethod
from datetime import date

from profiles.domain.profile.profile import Profile
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.user_id import UserId


class ProfileFactory(ABC):
    @abstractmethod
    async def create_profile(
        self, *, fullname: Fullname, user_id: UserId, birth_date: date | None = None
    ) -> Profile: ...

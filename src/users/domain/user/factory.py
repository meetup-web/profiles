from abc import ABC, abstractmethod
from datetime import date

from users.domain.user.user import User
from users.domain.user.value_objects import Contacts, Fullname


class UserFactory(ABC):
    @abstractmethod
    async def create_user(
        self,
        *,
        fullname: Fullname,
        contacts: Contacts,
        birth_date: date | None,
    ) -> User: ...

from abc import ABC, abstractmethod

from users.domain.user.user import User
from users.domain.user.user_id import UserId


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None: ...
    @abstractmethod
    def delete(self, user: User) -> None: ...
    @abstractmethod
    async def with_id(self, user_id: UserId) -> User | None: ...
    @abstractmethod
    async def with_email(self, email: str) -> User | None: ...

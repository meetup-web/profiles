from abc import ABC, abstractmethod

from users.application.models.pagination import Pagination
from users.application.models.user import UserReadModel
from users.domain.user.user_id import UserId


class UserGateway(ABC):
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> UserReadModel | None: ...
    @abstractmethod
    async def load_admins(self, pagination: Pagination) -> list[UserReadModel]: ...

from abc import ABC, abstractmethod

from users.application.models.user import UserReadModel
from users.domain.user.user_id import UserId


class UserGateway(ABC):
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> UserReadModel | None: ...

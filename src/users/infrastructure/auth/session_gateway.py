from abc import ABC, abstractmethod

from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_read_model import SessionReadModel


class SessionGateway(ABC):
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[SessionReadModel]: ...
    @abstractmethod
    async def with_session_id(self, session_id: SessionId) -> SessionReadModel | None: ...

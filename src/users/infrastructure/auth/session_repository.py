from abc import ABC, abstractmethod

from users.domain.user.user_id import UserId
from users.infrastructure.auth.session import Session
from users.infrastructure.auth.session_id import SessionId


class SessionRepository(ABC):
    @abstractmethod
    def add(self, session: Session) -> None: ...
    @abstractmethod
    def delete(self, session: Session) -> None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserId) -> list[Session]: ...
    @abstractmethod
    async def with_session_id(self, session_id: SessionId) -> Session | None: ...

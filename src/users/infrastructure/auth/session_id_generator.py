from abc import ABC, abstractmethod

from users.infrastructure.auth.session_id import SessionId


class SessionIdGenerator(ABC):
    @abstractmethod
    def generate_session_id(self) -> SessionId: ...

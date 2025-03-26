from abc import ABC, abstractmethod

from users.infrastructure.auth.session_read_model import SessionReadModel


class SessionStorer(ABC):
    @abstractmethod
    def store_session_id(self, session: SessionReadModel) -> None: ...


class SessionRaiser(ABC):
    @abstractmethod
    def raise_session_id(self) -> SessionReadModel | None: ...

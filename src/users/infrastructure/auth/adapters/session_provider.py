from users.infrastructure.auth.session_provider import SessionRaiser, SessionStorer
from users.infrastructure.auth.session_read_model import SessionReadModel


class SessionProvider(SessionStorer, SessionRaiser):
    def __init__(self) -> None:
        self._session: SessionReadModel | None = None

    def store_session(self, session: SessionReadModel) -> None:
        self._session = session

    def raise_session(self) -> SessionReadModel | None:
        return self._session

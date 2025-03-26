from uuid_extensions import uuid7  # type: ignore

from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_id_generator import SessionIdGenerator


class UUID7SessionIdGenerator(SessionIdGenerator):
    def generate_session_id(self) -> SessionId:
        return SessionId(uuid7())

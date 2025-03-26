from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_gateway import SessionGateway
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_read_model import SessionReadModel
from users.infrastructure.persistence.sql_tables import SESSIONS_TABLE


class SqlSessionGateway(SessionGateway):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection
        self._identity_map: dict[SessionId, SessionReadModel] = {}

    async def with_session_id(self, session_id: SessionId) -> SessionReadModel | None:
        if session_id in self._identity_map:
            return self._identity_map[session_id]

        statement = select(
            SESSIONS_TABLE.c.session_id.label("session_id"),
            SESSIONS_TABLE.c.user_id.label("user_id"),
            SESSIONS_TABLE.c.user_role.label("user_role"),
            SESSIONS_TABLE.c.expires_at.label("expires_at"),
        ).where(SESSIONS_TABLE.c.session_id == session_id)
        cursor_result = await self._connection.execute(statement)
        cursor_row = cursor_result.fetchone()

        if cursor_row is None:
            return None

        return self._load(cursor_row)

    async def with_user_id(self, user_id: UserId) -> list[SessionReadModel]:
        statement = select(
            SESSIONS_TABLE.c.session_id.label("session_id"),
            SESSIONS_TABLE.c.user_id.label("user_id"),
            SESSIONS_TABLE.c.user_role.label("user_role"),
            SESSIONS_TABLE.c.expires_at.label("expires_at"),
        ).where(SESSIONS_TABLE.c.user_id == user_id)
        cursor_result = await self._connection.execute(statement)

        sessions: list[SessionReadModel] = []
        for session_row in cursor_result:
            sessions.append(session := self._load(session_row))
            self._identity_map[session.session_id] = session

        return sessions

    def _load(self, row: Row) -> SessionReadModel:
        return SessionReadModel(
            session_id=row.session_id,
            user_id=row.user_id,
            user_role=row.user_role,
            expires_at=row.expires_at,
        )

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session import Session
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_repository import SessionRepository
from users.infrastructure.persistence.sql_tables import SESSIONS_TABLE


class SqlSessionRepository(SessionRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
    ) -> None:
        self._connection = connection
        self._unit_of_work = unit_of_work
        self._event_adder = event_adder
        self._identity_map: dict[SessionId, Session] = {}

    def add(self, session: Session) -> None:
        self._unit_of_work.register_new(session)
        self._identity_map[session.entity_id] = session

    def delete(self, session: Session) -> None:
        self._unit_of_work.register_deleted(session)
        self._identity_map.pop(session.entity_id, None)

    async def with_session_id(self, session_id: SessionId) -> Session | None:
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

    async def with_user_id(self, user_id: UserId) -> list[Session]:
        statement = select(
            SESSIONS_TABLE.c.session_id.label("session_id"),
            SESSIONS_TABLE.c.user_id.label("user_id"),
            SESSIONS_TABLE.c.user_role.label("user_role"),
            SESSIONS_TABLE.c.expires_at.label("expires_at"),
        ).where(SESSIONS_TABLE.c.user_id == user_id)
        cursor_result = await self._connection.execute(statement)

        sessions: list[Session] = []
        for session_row in cursor_result:
            sessions.append(session := self._load(session_row))
            self._identity_map[session.entity_id] = session

        return sessions

    def _load(self, row: Row) -> Session:
        return Session(
            entity_id=row.session_id,
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            user_role=row.user_role,
            user_id=row.user_id,
            expires_at=row.expires_at,
        )

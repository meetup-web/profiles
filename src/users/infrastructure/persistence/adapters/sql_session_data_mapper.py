from sqlalchemy.ext.asyncio import AsyncConnection

from users.infrastructure.auth.session import Session
from users.infrastructure.persistence.data_mapper import DataMapper
from users.infrastructure.persistence.sql_tables import SESSIONS_TABLE


class SqlSessionDataMapper(DataMapper[Session]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: Session) -> None:
        statement = SESSIONS_TABLE.insert().values(
            session_id=entity.entity_id,
            user_id=entity.user_id,
            user_role=entity.user_role,
            expires_at=entity.expires_at,
        )

        await self._connection.execute(statement)

    async def update(self, entity: Session) -> None:
        statement = (
            SESSIONS_TABLE.update()
            .values(user_role=entity.user_role)
            .where(SESSIONS_TABLE.c.session_id == entity.entity_id)
        )

        await self._connection.execute(statement)

    async def delete(self, entity: Session) -> None:
        statement = SESSIONS_TABLE.delete().where(
            SESSIONS_TABLE.c.session_id == entity.entity_id
        )

        await self._connection.execute(statement)

from sqlalchemy.ext.asyncio import AsyncConnection

from users.domain.user.user import User
from users.infrastructure.persistence.data_mapper import DataMapper
from users.infrastructure.persistence.sql_tables import USERS_TABLE


class SqlUserDataMapper(DataMapper[User]):
    def __init__(self, connection: AsyncConnection) -> None:
        self._connection = connection

    async def insert(self, entity: User) -> None:
        statement = USERS_TABLE.insert().values(
            user_id=entity.entity_id,
            birth_date=entity.birth_date,
            first_name=entity.fullname.first_name,
            last_name=entity.fullname.last_name,
            middle_name=entity.fullname.middle_name,
            email=entity.contacts.email,
            phone_number=entity.contacts.phone_number,
            created_at=entity.created_at,
            user_role=entity.user_role,
        )
        await self._connection.execute(statement)

    async def update(self, entity: User) -> None:
        statement = (
            USERS_TABLE.update()
            .where(USERS_TABLE.c.user_id == entity.entity_id)
            .values(
                birth_date=entity.birth_date,
                first_name=entity.fullname.first_name,
                last_name=entity.fullname.last_name,
                middle_name=entity.fullname.middle_name,
                user_role=entity.user_role,
            )
        )
        await self._connection.execute(statement)

    async def delete(self, entity: User) -> None:
        statement = USERS_TABLE.delete().where(USERS_TABLE.c.user_id == entity.entity_id)
        await self._connection.execute(statement)

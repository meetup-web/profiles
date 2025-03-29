from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from users.application.models.user import UserReadModel
from users.application.ports.user_gateway import UserGateway
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname
from users.infrastructure.persistence.sql_tables import USERS_TABLE


class SqlUsersGateway(UserGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._identity_map: dict[UserId, UserReadModel] = {}

    async def with_user_id(self, user_id: UserId) -> UserReadModel | None:
        if user_id in self._identity_map:
            return self._identity_map[user_id]

        statement = select(
            USERS_TABLE.c.user_id.label("user_id"),
            USERS_TABLE.c.birth_date.label("birth_date"),
            USERS_TABLE.c.first_name.label("first_name"),
            USERS_TABLE.c.last_name.label("last_name"),
            USERS_TABLE.c.middle_name.label("middle_name"),
            USERS_TABLE.c.created_at.label("created_at"),
        ).where(USERS_TABLE.c.user_id == user_id)
        cursor_result = await self._session.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        return self._load(row)

    def _load(self, row: Row) -> UserReadModel:
        return UserReadModel(
            user_id=UserId(row.user_id),
            fullname=Fullname(
                first_name=row.first_name,
                last_name=row.last_name,
                middle_name=row.middle_name,
            ),
            birth_date=row.birth_date,
            created_at=row.created_at,
        )

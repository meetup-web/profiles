from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncConnection

from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.repository import UserRepository
from users.domain.user.user import User
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname
from users.infrastructure.persistence.sql_tables import USERS_TABLE


class SqlUserRepository(UserRepository):
    def __init__(
        self,
        connection: AsyncConnection,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
    ) -> None:
        self._connection = connection
        self._unit_of_work = unit_of_work
        self._event_adder = event_adder
        self._identity_map: dict[UserId, User] = {}

    def add(self, user: User) -> None:
        self._unit_of_work.register_new(user)
        self._identity_map[user.entity_id] = user

    def delete(self, user: User) -> None:
        self._unit_of_work.register_deleted(user)
        self._identity_map.pop(user.entity_id, None)

    async def with_phone(self, phone: int) -> User | None:
        statement = select(
            USERS_TABLE.c.user_id.label("user_id"),
            USERS_TABLE.c.birth_date.label("birth_date"),
            USERS_TABLE.c.first_name.label("first_name"),
            USERS_TABLE.c.last_name.label("last_name"),
            USERS_TABLE.c.middle_name.label("middle_name"),
            USERS_TABLE.c.email.label("email"),
            USERS_TABLE.c.created_at.label("created_at"),
            USERS_TABLE.c.user_role.label("user_role"),
            USERS_TABLE.c.password.label("password"),
        ).where(USERS_TABLE.c.phone_number == phone)
        cursor_result = await self._connection.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        return self._load(row)

    async def with_email(self, email: str) -> User | None:
        statement = select(
            USERS_TABLE.c.user_id.label("user_id"),
            USERS_TABLE.c.birth_date.label("birth_date"),
            USERS_TABLE.c.first_name.label("first_name"),
            USERS_TABLE.c.last_name.label("last_name"),
            USERS_TABLE.c.middle_name.label("middle_name"),
            USERS_TABLE.c.email.label("email"),
            USERS_TABLE.c.created_at.label("created_at"),
            USERS_TABLE.c.user_role.label("user_role"),
            USERS_TABLE.c.password.label("password"),
        ).where(USERS_TABLE.c.email == email)
        cursor_result = await self._connection.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        return self._load(row)

    async def with_id(self, user_id: UserId) -> User | None:
        if user_id in self._identity_map:
            return self._identity_map[user_id]

        statement = select(
            USERS_TABLE.c.user_id.label("user_id"),
            USERS_TABLE.c.birth_date.label("birth_date"),
            USERS_TABLE.c.first_name.label("first_name"),
            USERS_TABLE.c.last_name.label("last_name"),
            USERS_TABLE.c.middle_name.label("middle_name"),
            USERS_TABLE.c.email.label("email"),
            USERS_TABLE.c.created_at.label("created_at"),
            USERS_TABLE.c.user_role.label("user_role"),
            USERS_TABLE.c.password.label("password"),
        ).where(USERS_TABLE.c.user_id == user_id)
        cursor_result = await self._connection.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        return self._load(row)

    def _load(self, row: Row) -> User:
        user = User(
            entity_id=UserId(row.user_id),
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            fullname=Fullname(
                first_name=row.first_name,
                last_name=row.last_name,
                middle_name=row.middle_name,
            ),
            email=row.email,
            created_at=row.created_at,
            birth_date=row.birth_date,
            user_role=row.user_role,
            password=row.password,
        )

        return user

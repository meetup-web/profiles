from sqlalchemy.ext.asyncio import AsyncSession

from users.domain.shared.events import DomainEventAdder
from users.domain.user.repository import UserRepository
from users.domain.user.user import User
from users.domain.user.user_id import UserId


class SqlUserRepository(UserRepository):
    def __init__(
        self,
        session: AsyncSession,
        event_adder: DomainEventAdder,
    ) -> None:
        self._session = session
        self._event_adder = event_adder

    def add(self, user: User) -> None:
        self._session.add(user)

    async def delete(self, user: User) -> None:
        await self._session.delete(user)

    async def with_id(self, user_id: UserId) -> User | None:
        user = await self._session.get(User, user_id)

        if user is None:
            return None

        return self._load(user)

    def _load(self, user: User) -> User:
        user.__setattr__("_event_adder", self._event_adder)
        return user

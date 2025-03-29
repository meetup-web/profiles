from datetime import date

from users.application.ports.id_generator import IdGenerator
from users.application.ports.time_provider import TimeProvider
from users.domain.shared.events import DomainEventAdder
from users.domain.user.events import UserCreated
from users.domain.user.factory import UserFactory
from users.domain.user.repository import UserRepository
from users.domain.user.user import User
from users.domain.user.value_objects import Fullname


class UserFactoryImpl(UserFactory):
    def __init__(
        self,
        user_repository: UserRepository,
        event_adder: DomainEventAdder,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
    ) -> None:
        self._user_repository = user_repository
        self._time_provider = time_provider
        self._event_adder = event_adder
        self._id_generator = id_generator

    async def create_user(self, *, fullname: Fullname, birth_date: date | None) -> User:
        user = User(
            entity_id=self._id_generator.generate_user_id(),
            event_adder=self._event_adder,
            birth_date=birth_date,
            fullname=fullname,
            created_at=self._time_provider.provide_current(),
        )

        event = UserCreated(
            user_id=user.entity_id,
            fullname=fullname,
            birth_date=birth_date,
            event_date=self._time_provider.provide_current(),
        )

        user.add_event(event)

        return user

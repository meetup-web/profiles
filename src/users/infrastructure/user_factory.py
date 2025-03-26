from datetime import date

from users.application.common.application_error import (
    ApplicationError,
    ErrorType,
)
from users.application.ports.id_generator import IdGenerator
from users.application.ports.time_provider import TimeProvider
from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.events import UserCreated
from users.domain.user.factory import UserFactory
from users.domain.user.repository import UserRepository
from users.domain.user.user import User
from users.domain.user.value_objects import Fullname
from users.infrastructure.auth.password_managment import PasswordHasher


class UserFactoryImpl(UserFactory):
    def __init__(
        self,
        user_repository: UserRepository,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        time_provider: TimeProvider,
        id_generator: IdGenerator,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._time_provider = time_provider
        self._event_adder = event_adder
        self._unit_of_work = unit_of_work
        self._id_generator = id_generator
        self._password_hasher = password_hasher

    async def create_user(
        self, *, fullname: Fullname, email: str, birth_date: date | None, password: str
    ) -> User:
        if await self._user_repository.with_email(email=email):
            raise ApplicationError(
                message="User already exists", error_type=ErrorType.CONFLICT_ERROR
            )

        user = User(
            entity_id=self._id_generator.generate_user_id(),
            event_adder=self._event_adder,
            unit_of_work=self._unit_of_work,
            birth_date=birth_date,
            email=email,
            fullname=fullname,
            created_at=self._time_provider.provide_current(),
            password=self._password_hasher.hash_password(password=password),
        )

        event = UserCreated(
            user_id=user.entity_id,
            fullname=fullname,
            email=email,
            birth_date=birth_date,
            event_date=self._time_provider.provide_current(),
            password=user.password,
        )

        user.add_event(event)

        return user

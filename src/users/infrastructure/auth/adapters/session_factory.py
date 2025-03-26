from datetime import timedelta
from typing import Final

from users.application.ports.time_provider import TimeProvider
from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session import Session
from users.infrastructure.auth.session_factory import SessionFactory
from users.infrastructure.auth.session_id_generator import SessionIdGenerator


class SessionFactoryImpl(SessionFactory):
    _SESSION_LIFETIME: Final[timedelta] = timedelta(days=30)

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        id_generator: SessionIdGenerator,
        time_provider: TimeProvider,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._event_adder = event_adder
        self._id_generator = id_generator
        self._time_provider = time_provider

    def create_session(self, user_id: UserId, user_role: UserRole) -> Session:
        session = Session(
            entity_id=self._id_generator.generate_session_id(),
            unit_of_work=self._unit_of_work,
            event_adder=self._event_adder,
            user_role=user_role,
            user_id=user_id,
            expires_at=self._time_provider.provide_current() + self._SESSION_LIFETIME,
        )

        return session

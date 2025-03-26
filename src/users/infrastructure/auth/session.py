from datetime import datetime

from users.domain.shared.entity import Entity
from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_id import SessionId


class Session(Entity[SessionId]):
    def __init__(
        self,
        entity_id: SessionId,
        unit_of_work: UnitOfWork,
        event_adder: DomainEventAdder,
        *,
        user_role: UserRole,
        user_id: UserId,
        expires_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder, unit_of_work)

        self._user_role = user_role
        self._user_id = user_id
        self._expires_at = expires_at

    @property
    def user_role(self) -> UserRole:
        return self._user_role

    @property
    def user_id(self) -> UserId:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at

    def change_user_roles(self, user_role: UserRole) -> None:
        self._user_role = user_role

        self.mark_dirty()

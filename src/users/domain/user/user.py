from collections.abc import Hashable
from datetime import date, datetime

from users.domain.shared.entity import Entity
from users.domain.shared.events import DomainEventAdder
from users.domain.shared.unit_of_work import UnitOfWork
from users.domain.user.events import (
    BirthDateChanged,
    FullnameChanged,
    UserPasswordChanged,
    UserRoleUpdated,
)
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


class User(Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        unit_of_work: UnitOfWork,
        *,
        birth_date: date | None = None,
        fullname: Fullname,
        created_at: datetime,
        user_role: UserRole = UserRole.USER,
        password: Hashable,
        email: str,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder, unit_of_work)

        self._birth_date = birth_date
        self._email = email
        self._fullname = fullname
        self._created_at = created_at
        self._user_role = user_role
        self._password = password

    def change_role(self, role: UserRole, current_date: datetime) -> None:
        if self._user_role == role:
            return

        self._user_role = role
        event = UserRoleUpdated(
            user_id=self._entity_id, role=role, event_date=current_date
        )

        self.mark_dirty()
        self.add_event(event)

    def change_password(self, password: Hashable, current_date: datetime) -> None:
        self._password = password
        event = UserPasswordChanged(
            user_id=self._entity_id, password=password, event_date=current_date
        )

        self.mark_dirty()
        self.add_event(event)

    def update_user_info(
        self,
        *,
        birth_date: date | None = None,
        fullname: Fullname,
        current_date: datetime,
    ) -> None:
        self.change_birth_date(birth_date, current_date)
        self.change_fullname(fullname, current_date)

    def change_fullname(self, fullname: Fullname, current_date: datetime) -> None:
        if self._fullname == fullname:
            return

        self._fullname = fullname
        event = FullnameChanged(
            user_id=self._entity_id, fullname=fullname, event_date=current_date
        )

        self.mark_dirty()
        self.add_event(event)

    def change_birth_date(self, birth_date: date | None, current_date: datetime) -> None:
        if self._birth_date == birth_date:
            return

        self._birth_date = birth_date
        event = BirthDateChanged(
            user_id=self._entity_id, birth_date=birth_date, event_date=current_date
        )

        self.mark_dirty()
        self.add_event(event)

    @property
    def fullname(self) -> Fullname:
        return self._fullname

    @property
    def birth_date(self) -> date | None:
        return self._birth_date

    @property
    def email(self) -> str:
        return self._email

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def user_role(self) -> UserRole:
        return self._user_role

    @property
    def password(self) -> Hashable:
        return self._password

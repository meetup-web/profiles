from datetime import date, datetime

from users.domain.shared.entity import Entity
from users.domain.shared.events import DomainEventAdder
from users.domain.user.events import BirthDateChanged, FullnameChanged
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


class User(Entity[UserId]):
    def __init__(
        self,
        entity_id: UserId,
        event_adder: DomainEventAdder,
        *,
        birth_date: date | None = None,
        fullname: Fullname,
        created_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder)

        self._birth_date = birth_date
        self._fullname = fullname
        self._created_at = created_at

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

        self.add_event(event)

    def change_birth_date(self, birth_date: date | None, current_date: datetime) -> None:
        if self._birth_date == birth_date:
            return

        self._birth_date = birth_date
        event = BirthDateChanged(
            user_id=self._entity_id, birth_date=birth_date, event_date=current_date
        )

        self.add_event(event)

    @property
    def fullname(self) -> Fullname:
        return self._fullname

    @property
    def birth_date(self) -> date | None:
        return self._birth_date

    @property
    def created_at(self) -> datetime:
        return self._created_at

from datetime import date, datetime

from profiles.domain.profile.events import BirthDateChanged, FullnameChanged
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.entity import Entity
from profiles.domain.shared.events import DomainEventAdder
from profiles.domain.shared.user_id import UserId


class Profile(Entity[ProfileId]):
    def __init__(
        self,
        entity_id: ProfileId,
        event_adder: DomainEventAdder,
        *,
        owner_id: UserId,
        birth_date: date | None = None,
        fullname: Fullname,
        created_at: datetime,
    ) -> None:
        Entity.__init__(self, entity_id, event_adder)

        self._owner_id = owner_id
        self._birth_date = birth_date
        self._fullname = fullname
        self._created_at = created_at

    def update_profile_info(
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
            profile_id=self._entity_id, fullname=fullname, event_date=current_date
        )

        self.add_event(event)

    def change_birth_date(self, birth_date: date | None, current_date: datetime) -> None:
        if self._birth_date == birth_date:
            return

        self._birth_date = birth_date
        event = BirthDateChanged(
            profile_id=self._entity_id, birth_date=birth_date, event_date=current_date
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

    @property
    def owner_id(self) -> UserId:
        return self._owner_id

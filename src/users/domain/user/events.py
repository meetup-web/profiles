from dataclasses import dataclass
from datetime import date

from users.domain.shared.events import DomainEvent
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


@dataclass(frozen=True)
class UserCreated(DomainEvent):
    user_id: UserId
    fullname: Fullname
    birth_date: date | None


@dataclass(frozen=True)
class FullnameChanged(DomainEvent):
    user_id: UserId
    fullname: Fullname


@dataclass(frozen=True)
class BirthDateChanged(DomainEvent):
    user_id: UserId
    birth_date: date | None


@dataclass(frozen=True)
class UserDeleted(DomainEvent):
    user_id: UserId

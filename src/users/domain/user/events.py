from collections.abc import Hashable
from dataclasses import dataclass
from datetime import date

from users.domain.shared.events import DomainEvent
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


@dataclass(frozen=True)
class UserCreated(DomainEvent):
    user_id: UserId
    fullname: Fullname
    email: str
    birth_date: date | None
    password: Hashable


@dataclass(frozen=True)
class UserRoleUpdated(DomainEvent):
    user_id: UserId
    role: UserRole


@dataclass(frozen=True)
class FullnameChanged(DomainEvent):
    user_id: UserId
    fullname: Fullname


@dataclass(frozen=True)
class BirthDateChanged(DomainEvent):
    user_id: UserId
    birth_date: date | None


@dataclass(frozen=True)
class UserPasswordChanged(DomainEvent):
    user_id: UserId
    password: bytes


@dataclass(frozen=True)
class UserDeleted(DomainEvent):
    user_id: UserId

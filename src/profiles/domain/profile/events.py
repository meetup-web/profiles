from dataclasses import dataclass
from datetime import date

from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.events import DomainEvent
from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ProfileCreated(DomainEvent):
    user_id: UserId
    profile_id: ProfileId
    fullname: Fullname
    birth_date: date | None


@dataclass(frozen=True)
class FullnameChanged(DomainEvent):
    profile_id: ProfileId
    fullname: Fullname


@dataclass(frozen=True)
class BirthDateChanged(DomainEvent):
    profile_id: ProfileId
    birth_date: date | None


@dataclass(frozen=True)
class ProfileDeleted(DomainEvent):
    profile_id: ProfileId

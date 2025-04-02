from dataclasses import dataclass
from datetime import date, datetime

from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class ProfileReadModel:
    user_id: UserId
    profile_id: ProfileId
    fullname: Fullname
    birth_date: date | None
    created_at: datetime

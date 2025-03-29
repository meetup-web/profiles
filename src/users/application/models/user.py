from dataclasses import dataclass
from datetime import date, datetime

from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


@dataclass(frozen=True)
class UserReadModel:
    user_id: UserId
    fullname: Fullname
    birth_date: date | None
    created_at: datetime

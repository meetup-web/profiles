from dataclasses import dataclass

from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class UserDeleted:
    user_id: UserId


@dataclass(frozen=True)
class UserCreated:
    user_id: UserId
    username: str

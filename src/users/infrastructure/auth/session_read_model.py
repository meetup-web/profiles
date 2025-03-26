from dataclasses import dataclass
from datetime import datetime

from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_id import SessionId


@dataclass(frozen=True)
class SessionReadModel:
    session_id: SessionId
    user_id: UserId
    user_role: UserRole
    expires_at: datetime

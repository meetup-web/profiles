from abc import ABC, abstractmethod

from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session import Session


class SessionFactory(ABC):
    @abstractmethod
    def create_session(self, user_id: UserId, user_role: UserRole) -> Session: ...

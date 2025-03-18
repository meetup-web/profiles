from abc import ABC, abstractmethod

from users.domain.shared.event_id import EventId
from users.domain.user.user_id import UserId


class IdGenerator(ABC):
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_user_id(self) -> UserId: ...

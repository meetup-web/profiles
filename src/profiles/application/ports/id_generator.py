from abc import ABC, abstractmethod

from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.shared.event_id import EventId


class IdGenerator(ABC):
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_profile_id(self) -> ProfileId: ...

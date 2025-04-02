from uuid_extensions import uuid7  # type: ignore

from profiles.application.ports.id_generator import IdGenerator
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.shared.event_id import EventId


class UUID7IdGenerator(IdGenerator):
    def generate_event_id(self) -> EventId:
        return EventId(uuid7())

    def generate_profile_id(self) -> ProfileId:
        return ProfileId(uuid7())

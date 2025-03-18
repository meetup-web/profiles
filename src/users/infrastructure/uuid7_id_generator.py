from uuid_extensions import uuid7  # type: ignore

from users.application.ports.id_generator import IdGenerator
from users.domain.shared.event_id import EventId
from users.domain.user.user_id import UserId


class UUID7IdGenerator(IdGenerator):
    def generate_event_id(self) -> EventId:
        return EventId(uuid7())

    def generate_user_id(self) -> UserId:
        return UserId(uuid7())

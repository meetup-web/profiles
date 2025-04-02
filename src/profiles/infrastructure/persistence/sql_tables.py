from sqlalchemy import (
    UUID,
    Column,
    Date,
    DateTime,
    MetaData,
    Table,
    Text,
)
from sqlalchemy.orm import composite, registry

from profiles.domain.profile.profile import Profile
from profiles.domain.profile.value_objects import Fullname
from profiles.infrastructure.outbox.outbox_message import OutboxMessage

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)


PROFILES_TABLE = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("profile_id", UUID, primary_key=True),
    Column("user_id", UUID, nullable=False, unique=True),
    Column("birth_date", Date, nullable=True),
    Column("first_name", Text, nullable=False),
    Column("last_name", Text, nullable=True),
    Column("middle_name", Text, nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
)

OUTBOX_TABLE = Table(
    "outbox",
    MAPPER_REGISTRY.metadata,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)


def map_profile_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        Profile,
        PROFILES_TABLE,
        properties={
            "_entity_id": PROFILES_TABLE.c.profile_id,
            "_owner_id": PROFILES_TABLE.c.user_id,
            "_fullname": composite(
                Fullname,
                PROFILES_TABLE.c.first_name,
                PROFILES_TABLE.c.last_name,
                PROFILES_TABLE.c.middle_name,
            ),
            "_birth_date": PROFILES_TABLE.c.birth_date,
            "_created_at": PROFILES_TABLE.c.created_at,
        },
    )


def map_outbox_table() -> None:
    MAPPER_REGISTRY.map_imperatively(OutboxMessage, OUTBOX_TABLE)

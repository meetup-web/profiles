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

from users.domain.user.user import User
from users.domain.user.value_objects import Fullname
from users.infrastructure.outbox.outbox_message import OutboxMessage

METADATA = MetaData()
MAPPER_REGISTRY = registry(metadata=METADATA)


USERS_TABLE = Table(
    "users",
    MAPPER_REGISTRY.metadata,
    Column("user_id", UUID, primary_key=True),
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


def map_user_table() -> None:
    MAPPER_REGISTRY.map_imperatively(
        User,
        USERS_TABLE,
        properties={
            "_entity_id": USERS_TABLE.c.user_id,
            "_fullname": composite(
                Fullname,
                USERS_TABLE.c.first_name,
                USERS_TABLE.c.last_name,
                USERS_TABLE.c.middle_name,
            ),
            "_birth_date": USERS_TABLE.c.birth_date,
            "_created_at": USERS_TABLE.c.created_at,
        },
    )


def map_outbox_table() -> None:
    MAPPER_REGISTRY.map_imperatively(OutboxMessage, OUTBOX_TABLE)

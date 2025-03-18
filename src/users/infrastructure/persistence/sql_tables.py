from sqlalchemy import (
    UUID,
    BigInteger,
    Column,
    Date,
    DateTime,
    Enum,
    MetaData,
    Table,
    Text,
)

from users.domain.user.roles import UserRole

METADATA = MetaData()

USERS_TABLE = Table(
    "users",
    METADATA,
    Column("user_id", UUID, primary_key=True),
    Column("birth_date", Date, nullable=True),
    Column("email", Text, nullable=True),
    Column("phone_number", BigInteger, nullable=True),
    Column("first_name", Text, nullable=False),
    Column("last_name", Text, nullable=True),
    Column("middle_name", Text, nullable=True),
    Column("user_role", Enum(UserRole), nullable=False, default=UserRole.USER),
    Column("created_at", DateTime, nullable=False),
)

OUTBOX_TABLE = Table(
    "outbox",
    METADATA,
    Column("message_id", UUID, primary_key=True),
    Column("data", Text, nullable=False),
    Column("event_type", Text, nullable=False, default=False),
)

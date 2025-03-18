from dataclasses import dataclass, field

from users.domain.shared.value_object import ValueObject


@dataclass(frozen=True)
class Contacts(ValueObject):
    email: str | None = field(default=None)
    phone_number: int | None = field(default=None)


@dataclass(frozen=True)
class Fullname(ValueObject):
    first_name: str
    last_name: str | None = field(default=None)
    middle_name: str | None = field(default=None)

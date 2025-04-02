from dataclasses import dataclass, field

from profiles.domain.shared.value_object import ValueObject


@dataclass(frozen=True)
class Fullname(ValueObject):
    first_name: str
    last_name: str | None = field(default=None)
    middle_name: str | None = field(default=None)

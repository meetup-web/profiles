from datetime import UTC, datetime

from users.application.ports.time_provider import TimeProvider


class UtcTimeProvider(TimeProvider):
    def provide_current(self) -> datetime:
        return datetime.now(UTC)

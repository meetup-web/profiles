from abc import ABC, abstractmethod

from users.infrastructure.outbox.outbox_message import OutboxMessage


class OutboxPublisher(ABC):
    @abstractmethod
    async def publish(self, message: OutboxMessage) -> None: ...

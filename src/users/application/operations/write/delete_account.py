from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.command import Command
from users.application.ports.context.identity_provider import IdentityProvider
from users.application.ports.time_provider import TimeProvider
from users.domain.user.events import UserDeleted
from users.domain.user.repository import UserRepository


@dataclass(frozen=True)
class DeleteAccount(Command[None]): ...


class DeleteAccountHandler(RequestHandler[DeleteAccount, None]):
    def __init__(
        self,
        user_repository: UserRepository,
        identity_provider: IdentityProvider,
        time_provider: TimeProvider,
    ) -> None:
        self._user_repository = user_repository
        self._identity_provider = identity_provider
        self._time_provider = time_provider

    async def handle(self, request: DeleteAccount) -> None:
        user_id = await self._identity_provider.current_user_id()

        user = await self._user_repository.with_id(user_id)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="User not found"
            )

        event = UserDeleted(
            user_id=user_id, event_date=self._time_provider.provide_current()
        )
        user.add_event(event)

        await self._user_repository.delete(user)

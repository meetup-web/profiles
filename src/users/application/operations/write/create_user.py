from dataclasses import dataclass
from datetime import date

from bazario.asyncio import RequestHandler

from users.application.common.markers.command import Command
from users.application.ports.time_provider import TimeProvider
from users.domain.user.factory import UserFactory
from users.domain.user.repository import UserRepository
from users.domain.user.user_id import UserId
from users.domain.user.value_objects import Fullname


@dataclass(frozen=True)
class CreateUser(Command[UserId]):
    fullname: Fullname
    birth_date: date | None


class CreateUserHandler(RequestHandler[CreateUser, UserId]):
    def __init__(
        self,
        user_factory: UserFactory,
        time_provider: TimeProvider,
        user_repository: UserRepository,
    ) -> None:
        self._user_factory = user_factory
        self._time_provider = time_provider
        self._user_repository = user_repository

    async def handle(self, request: CreateUser) -> UserId:
        user = await self._user_factory.create_user(
            fullname=request.fullname, birth_date=request.birth_date
        )

        self._user_repository.add(user)

        return user.entity_id

from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.query import Query
from users.application.models.user import UserReadModel
from users.application.ports.user_gateway import UserGateway
from users.domain.user.user_id import UserId


@dataclass(frozen=True)
class LoadUserById(Query[UserReadModel]):
    user_id: UserId


class LoadUserByIdHandler(RequestHandler[LoadUserById, UserReadModel]):
    def __init__(self, user_gateway: UserGateway) -> None:
        self._user_gateway = user_gateway

    async def handle(self, request: LoadUserById) -> UserReadModel:
        user = await self._user_gateway.with_user_id(request.user_id)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="User not found"
            )

        return user

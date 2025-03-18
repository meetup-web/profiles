from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.markers.query import Query
from users.application.models.pagination import Pagination
from users.application.models.user import UserReadModel
from users.application.ports.user_gateway import UserGateway


@dataclass(frozen=True)
class LoadAdmins(Query[list[UserReadModel]]):
    pagination: Pagination


class LoadAdminsHandler(RequestHandler[LoadAdmins, list[UserReadModel]]):
    def __init__(self, user_gateway: UserGateway) -> None:
        self._user_gateway = user_gateway

    async def handle(self, request: LoadAdmins) -> list[UserReadModel]:
        admins = await self._user_gateway.load_admins(pagination=request.pagination)

        return admins

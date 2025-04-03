from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from profiles.application.common.markers.query import Query
from profiles.application.models.profile import ProfileReadModel
from profiles.application.ports.profile_gateway import ProfileGateway
from profiles.domain.shared.user_id import UserId


@dataclass(frozen=True)
class LoadProfilesByUserIds(Query[list[ProfileReadModel]]):
    user_ids: list[UserId]


class LoadProfilesByUserIdsHandler(
    RequestHandler[LoadProfilesByUserIds, list[ProfileReadModel]]
):
    def __init__(self, profile_gateway: ProfileGateway) -> None:
        self._profile_gateway = profile_gateway

    async def handle(self, request: LoadProfilesByUserIds) -> list[ProfileReadModel]:
        profiles = await self._profile_gateway.with_user_ids(request.user_ids)
        return profiles

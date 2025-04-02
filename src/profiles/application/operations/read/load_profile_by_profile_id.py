from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from profiles.application.common.application_error import ApplicationError, ErrorType
from profiles.application.common.markers.query import Query
from profiles.application.models.profile import ProfileReadModel
from profiles.application.ports.profile_gateway import ProfileGateway
from profiles.domain.profile.profile_id import ProfileId


@dataclass(frozen=True)
class LoadProfileById(Query[ProfileReadModel]):
    profile_id: ProfileId


class LoadProfileByIdHandler(RequestHandler[LoadProfileById, ProfileReadModel]):
    def __init__(self, profile_gateway: ProfileGateway) -> None:
        self._profile_gateway = profile_gateway

    async def handle(self, request: LoadProfileById) -> ProfileReadModel:
        profile = await self._profile_gateway.with_profile_id(request.profile_id)

        if not profile:
            raise ApplicationError(
                error_type=ErrorType.NOT_FOUND, message="Profile not found"
            )

        return profile

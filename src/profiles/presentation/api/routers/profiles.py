from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND

from profiles.application.common.application_error import ApplicationError
from profiles.application.models.profile import ProfileReadModel
from profiles.application.operations.read.load_profile_by_profile_id import (
    LoadProfileById,
)
from profiles.application.operations.read.load_profile_by_user_id import (
    LoadProfileByUserId,
)
from profiles.application.operations.write.update_info import UpdateInfo
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.shared.user_id import UserId
from profiles.presentation.api.response_models import (
    ErrorResponse,
    SuccessResponse,
)

PROFILE_ROUTER = APIRouter(prefix="/profiles", tags=["Profiles"])


@PROFILE_ROUTER.put(
    "/",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def update_info(
    request: UpdateInfo, *, sender: FromDishka[Sender]
) -> SuccessResponse[None]:
    await sender.send(request)
    return SuccessResponse(result=None, status=HTTP_200_OK)


@PROFILE_ROUTER.get(
    "/user/{user_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[ProfileReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def load_profile_by_user_id(
    user_id: UserId, *, sender: FromDishka[Sender]
) -> SuccessResponse[ProfileReadModel]:
    user = await sender.send(LoadProfileByUserId(user_id=user_id))
    return SuccessResponse(result=user, status=HTTP_200_OK)


@PROFILE_ROUTER.get(
    "/profile/{profile_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[ProfileReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def load_profile_by_profile_id(
    profile_id: ProfileId, *, sender: FromDishka[Sender]
) -> SuccessResponse[ProfileReadModel]:
    user = await sender.send(LoadProfileById(profile_id=profile_id))
    return SuccessResponse(result=user, status=HTTP_200_OK)

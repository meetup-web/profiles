from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from users.application.common.application_error import ApplicationError
from users.application.models.user import UserReadModel
from users.application.operations.read.load_user_by_id import LoadUserById
from users.application.operations.write.create_user import CreateUser
from users.application.operations.write.delete_account import DeleteAccount
from users.application.operations.write.update_info import UpdateInfo
from users.domain.user.user_id import UserId
from users.presentation.api.response_models import (
    ErrorResponse,
    SuccessResponse,
)

USERS_ROUTER = APIRouter(prefix="/users", tags=["users"])


@USERS_ROUTER.post(
    path="/",
    responses={
        HTTP_201_CREATED: {"model": SuccessResponse[UserId]},
    },
    status_code=HTTP_201_CREATED,
)
@inject
async def create_user(
    request: CreateUser, *, sender: FromDishka[Sender]
) -> SuccessResponse[UserId]:
    user_id = await sender.send(request)
    return SuccessResponse(result=user_id, status=HTTP_201_CREATED)


@USERS_ROUTER.delete(
    "/",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def delete_account(*, sender: FromDishka[Sender]) -> SuccessResponse[None]:
    await sender.send(DeleteAccount())
    return SuccessResponse(result=None, status=HTTP_200_OK)


@USERS_ROUTER.put(
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


@USERS_ROUTER.get(
    "/{user_id}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[UserReadModel]},
        HTTP_404_NOT_FOUND: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def load_user_by_id(
    user_id: UserId, *, sender: FromDishka[Sender]
) -> SuccessResponse[UserReadModel]:
    user = await sender.send(LoadUserById(user_id=user_id))
    return SuccessResponse(result=user, status=HTTP_200_OK)

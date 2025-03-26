from typing import Final
from uuid import UUID

from bazario.asyncio import Sender
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette.requests import Request
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.models.user import UserReadModel
from users.application.operations.write.create_user import CreateUser
from users.domain.user.user_id import UserId
from users.infrastructure.auth.session_getter_handlers import (
    GetSessionById,
    GetUserSessions,
)
from users.infrastructure.auth.session_id import SessionId
from users.infrastructure.auth.session_login_handler import Login
from users.infrastructure.auth.session_logout_handler import Logout
from users.infrastructure.auth.session_read_model import SessionReadModel
from users.presentation.api.response_models import (
    ErrorResponse,
    SuccessResponse,
)

COOKIE_NAME: Final[str] = "session_id"
AUTH_ROUTER = APIRouter(prefix="/auth", tags=["Auth"])


@AUTH_ROUTER.post(
    path="/register",
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_409_CONFLICT: {"model": ErrorResponse[ApplicationError]},
        HTTP_201_CREATED: {"model": SuccessResponse[UserId]},
    },
)
@inject
async def regitser_user(
    command: CreateUser, *, sender: FromDishka[Sender]
) -> SuccessResponse[UserId]:
    user_id = await sender.send(command)
    return SuccessResponse(status=HTTP_201_CREATED, result=user_id)


@AUTH_ROUTER.post(
    path="/login",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[UserReadModel]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def login_user(
    command: Login, *, sender: FromDishka[Sender]
) -> SuccessResponse[UserReadModel]:
    user = await sender.send(command)
    return SuccessResponse(status=HTTP_200_OK, result=user)


@AUTH_ROUTER.post(
    path="/logout",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[None]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def logout_user(
    request: Request, *, sender: FromDishka[Sender]
) -> SuccessResponse[None]:
    session_id = request.cookies.get(COOKIE_NAME)

    if not session_id:
        raise ApplicationError(
            error_type=ErrorType.APPLICATION_ERROR, message="session not provided"
        )

    await sender.send(Logout(SessionId(UUID(session_id))))
    return SuccessResponse(result=None, status=HTTP_200_OK)


@AUTH_ROUTER.get(
    path="/my-sessions",
    status_code=HTTP_200_OK,
    responses={HTTP_200_OK: {"model": SuccessResponse[list[SessionReadModel]]}},
)
@inject
async def get_my_sessions(
    sender: FromDishka[Sender],
) -> SuccessResponse[list[SessionReadModel]]:
    sessions = await sender.send(GetUserSessions())
    return SuccessResponse(status=HTTP_200_OK, result=sessions)


@AUTH_ROUTER.get(
    path="/session",
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {"model": SuccessResponse[SessionReadModel]},
        HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[ApplicationError]},
    },
)
@inject
async def get_session(
    request: Request, *, sender: FromDishka[Sender]
) -> SuccessResponse[SessionReadModel]:
    session_id = request.cookies.get(COOKIE_NAME)

    if not session_id:
        raise ApplicationError(
            error_type=ErrorType.AUTHORIZATION_ERROR, message="session not provided"
        )

    session = await sender.send(GetSessionById(SessionId(UUID(session_id))))

    return SuccessResponse(status=HTTP_200_OK, result=session)

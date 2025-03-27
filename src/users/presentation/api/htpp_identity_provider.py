from typing import Final
from uuid import UUID

from fastapi import Request

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.ports.context.identity_provider import IdentityProvider
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId


class HttpIdentityProvider(IdentityProvider):
    _USER_ROLE_HEADER: Final[str] = "X-Auth-User-Role"
    _USER_ID_HEADER: Final[str] = "X-Auth-User-Id"

    def __init__(self, request: Request) -> None:
        self._request = request

    async def current_user_id(self) -> UserId:
        user_id = self._request.headers.get(self._USER_ID_HEADER)

        if not user_id:
            raise ApplicationError(
                message="User not provided", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return UserId(UUID(user_id))

    async def current_user_role(self) -> UserRole:
        user_role = self._request.headers.get(self._USER_ROLE_HEADER)

        if not user_role:
            raise ApplicationError(
                message="User not provided", error_type=ErrorType.AUTHORIZATION_ERROR
            )

        return UserRole(user_role)

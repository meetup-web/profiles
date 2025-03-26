from typing import Final, Literal, cast

from dishka import AsyncContainer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from users.infrastructure.auth.session_provider import SessionRaiser
from users.presentation.api.routers.auth import COOKIE_NAME


class LoginMiddleware(BaseHTTPMiddleware):
    _PATH: Final[str] = "/auth/login"
    _SAMESITE: Final[Literal["lax", "strict", "none"]] = "lax"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._PATH):
            return response

        container = cast(AsyncContainer, request.state.dishka_container)

        async with container() as req_container:
            session_raiser = await req_container.get(SessionRaiser)

        session = session_raiser.raise_session_id()

        if not session:
            return response

        response.set_cookie(
            key=COOKIE_NAME,
            value=str(session.session_id),
            samesite=self._SAMESITE,
            expires=session.expires_at,
        )

        return response


class RegisterMiddleware(BaseHTTPMiddleware):
    _PATH: Final[str] = "/auth/register"
    _SAMESITE: Final[Literal["lax", "strict", "none"]] = "lax"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._PATH):
            return response

        container = cast(AsyncContainer, request.state.dishka_container)

        async with container() as req_container:
            session_raiser = await req_container.get(SessionRaiser)

        session = session_raiser.raise_session_id()

        if not session:
            return response

        response.set_cookie(
            key=COOKIE_NAME,
            value=str(session.session_id),
            samesite=self._SAMESITE,
            expires=session.expires_at,
        )

        return response


class LogoutMiddleware(BaseHTTPMiddleware):
    _PATH: Final[str] = "/auth/logout"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)

        if not request.url.path.startswith(self._PATH):
            return response

        response.delete_cookie(COOKIE_NAME)

        return response

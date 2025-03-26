from dataclasses import dataclass

from bazario.asyncio import RequestHandler

from users.application.common.application_error import ApplicationError, ErrorType
from users.application.common.markers.command import Command
from users.application.models.user import UserReadModel
from users.domain.user.repository import UserRepository
from users.infrastructure.auth.password_managment import PasswordVerifier


@dataclass(frozen=True)
class Login(Command[UserReadModel]):
    email: str
    password: str


class LoginHandler(RequestHandler[Login, UserReadModel]):
    def __init__(
        self, user_repository: UserRepository, password_verifier: PasswordVerifier
    ) -> None:
        self._password_verifier = password_verifier
        self._user_repository = user_repository

    async def handle(self, request: Login) -> UserReadModel:
        user = await self._user_repository.with_email(email=request.email)

        if not user:
            raise ApplicationError(
                error_type=ErrorType.AUTHORIZATION_ERROR,
                message="Invalid email or password",
            )

        if not self._password_verifier.verify_password(
            password=request.password, hashed_password=user.password
        ):
            raise ApplicationError(
                error_type=ErrorType.AUTHORIZATION_ERROR,
                message="Invalid email or password",
            )

        return UserReadModel(
            user_id=user.entity_id,
            fullname=user.fullname,
            email=user.email,
            user_role=user.user_role,
            birth_date=user.birth_date,
            created_at=user.created_at,
        )

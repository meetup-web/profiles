from uuid import UUID

from users.application.ports.context.identity_provider import IdentityProvider
from users.domain.user.roles import UserRole
from users.domain.user.user_id import UserId


class FakeIdentityProvider(IdentityProvider):
    async def current_user_id(self) -> UserId:
        return UserId(UUID("067d9a75-5eda-7934-8000-cf17a9aababe"))

    async def current_user_role(self) -> UserRole:
        return UserRole.ADMIN

from bazario.asyncio import NotificationHandler

from users.domain.user.events import UserDeleted
from users.infrastructure.auth.session_repository import SessionRepository


class SessionDelitingHandler(NotificationHandler[UserDeleted]):
    def __init__(self, session_repository: SessionRepository) -> None:
        self._session_repository = session_repository

    async def handle(self, notification: UserDeleted) -> None:
        user_sessions = await self._session_repository.with_user_id(
            user_id=notification.user_id
        )

        for user_session in user_sessions:
            self._session_repository.delete(user_session)

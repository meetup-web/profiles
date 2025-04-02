from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from profiles.application.models.profile import ProfileReadModel
from profiles.application.ports.profile_gateway import ProfileGateway
from profiles.domain.profile.profile_id import ProfileId
from profiles.domain.profile.value_objects import Fullname
from profiles.domain.shared.user_id import UserId
from profiles.infrastructure.persistence.sql_tables import PROFILES_TABLE


class SqlProfileGateway(ProfileGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._identity_map: dict[ProfileId, ProfileReadModel] = {}

    async def with_user_id(self, user_id: UserId) -> ProfileReadModel | None:
        statement = select(
            PROFILES_TABLE.c.profile_id.label("profile_id"),
            PROFILES_TABLE.c.user_id.label("user_id"),
            PROFILES_TABLE.c.birth_date.label("birth_date"),
            PROFILES_TABLE.c.first_name.label("first_name"),
            PROFILES_TABLE.c.last_name.label("last_name"),
            PROFILES_TABLE.c.middle_name.label("middle_name"),
            PROFILES_TABLE.c.created_at.label("created_at"),
        ).where(PROFILES_TABLE.c.user_id == user_id)
        cursor_result = await self._session.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        profile = self._load(row)
        self._identity_map[profile.profile_id] = profile

        return profile

    async def with_profile_id(self, profile_id: ProfileId) -> ProfileReadModel | None:
        if profile_id in self._identity_map:
            return self._identity_map[profile_id]

        statement = select(
            PROFILES_TABLE.c.profile_id.label("profile_id"),
            PROFILES_TABLE.c.user_id.label("user_id"),
            PROFILES_TABLE.c.birth_date.label("birth_date"),
            PROFILES_TABLE.c.first_name.label("first_name"),
            PROFILES_TABLE.c.last_name.label("last_name"),
            PROFILES_TABLE.c.middle_name.label("middle_name"),
            PROFILES_TABLE.c.created_at.label("created_at"),
        ).where(PROFILES_TABLE.c.profile_id == profile_id)
        cursor_result = await self._session.execute(statement)
        row = cursor_result.fetchone()

        if not row:
            return None

        profile = self._load(row)
        self._identity_map[profile_id] = profile

        return profile

    def _load(self, row: Row) -> ProfileReadModel:
        return ProfileReadModel(
            profile_id=ProfileId(row.profile_id),
            user_id=UserId(row.user_id),
            fullname=Fullname(
                first_name=row.first_name,
                last_name=row.last_name,
                middle_name=row.middle_name,
            ),
            birth_date=row.birth_date,
            created_at=row.created_at,
        )

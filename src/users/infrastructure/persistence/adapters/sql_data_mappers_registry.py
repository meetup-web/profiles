from users.domain.shared.entity import Entity
from users.domain.user.user import User
from users.infrastructure.auth.session import Session
from users.infrastructure.persistence.adapters.sql_session_data_mapper import (
    SqlSessionDataMapper,
)
from users.infrastructure.persistence.adapters.sql_user_data_mapper import (
    SqlUserDataMapper,
)
from users.infrastructure.persistence.data_mapper import DataMapper
from users.infrastructure.persistence.data_mappers_registry import (
    DataMappersRegistry,
)


class SqlDataMappersRegistry(DataMappersRegistry):
    def __init__(
        self,
        user_data_mapper: SqlUserDataMapper,
        session_data_mapper: SqlSessionDataMapper,
    ) -> None:
        self._data_mappers_map: dict[type[Entity], DataMapper] = {
            User: user_data_mapper,
            Session: session_data_mapper,
        }

    def get_mapper[EntityT: Entity](self, entity: type[EntityT]) -> DataMapper[EntityT]:
        mapper = self._data_mappers_map.get(entity)

        if not mapper:
            raise KeyError(f"DataMapper for {entity.__name__!r} not registered")

        return mapper

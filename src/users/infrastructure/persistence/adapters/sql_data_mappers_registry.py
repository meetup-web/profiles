from users.domain.shared.entity import Entity
from users.domain.user.user import User
from users.infrastructure.persistence.adapters.sql_user_data_mapper import (
    SqlUserDataMapper,
)
from users.infrastructure.persistence.data_mapper import DataMapper
from users.infrastructure.persistence.data_mappers_registry import (
    DataMappersRegistry,
)


class SqlDataMappersRegistry(DataMappersRegistry):
    def __init__(self, user_data_mapper: SqlUserDataMapper) -> None:
        self._data_mappers_map: dict[type[Entity], DataMapper] = {User: user_data_mapper}

    def get_mapper[EntityT: Entity](self, entity: type[EntityT]) -> DataMapper[EntityT]:
        mapper = self._data_mappers_map.get(entity)

        if not mapper:
            raise KeyError(f"DataMapper for {entity.__name__!r} not registered")

        return mapper

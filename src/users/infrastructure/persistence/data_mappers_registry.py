from abc import ABC, abstractmethod

from users.domain.shared.entity import Entity
from users.infrastructure.persistence.data_mapper import DataMapper


class DataMappersRegistry(ABC):
    @abstractmethod
    def get_mapper(self, entity: type[Entity]) -> DataMapper: ...

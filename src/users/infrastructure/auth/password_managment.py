from abc import ABC, abstractmethod
from collections.abc import Hashable


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> Hashable: ...


class PasswordVerifier(ABC):
    @abstractmethod
    def verify_password(self, password: str, hashed_password: Hashable) -> bool: ...

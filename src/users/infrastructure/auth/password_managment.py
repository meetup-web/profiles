from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> bytes: ...


class PasswordVerifier(ABC):
    @abstractmethod
    def verify_password(self, password: str, hashed_password: bytes) -> bool: ...

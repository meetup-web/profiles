from typing import Final

from bcrypt import checkpw, gensalt, hashpw

from users.infrastructure.auth.password_managment import PasswordHasher, PasswordVerifier


class CryptoPasswordHasher(PasswordHasher):
    _ENCODING: Final[str] = "utf-8"

    def hash_password(self, password: str) -> bytes:
        hashed_bytes = hashpw(password=password.encode(self._ENCODING), salt=gensalt())

        return hashed_bytes


class CryptoPasswordVerifier(PasswordVerifier):
    _ENCODING: Final[str] = "utf-8"

    def verify_password(self, password: str, hashed_password: bytes) -> bool:
        decision = checkpw(
            password=password.encode(self._ENCODING),
            hashed_password=hashed_password,
        )
        return decision

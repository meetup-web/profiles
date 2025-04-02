from abc import ABC, abstractmethod

from profiles.domain.shared.user_id import UserId


class IdentityProvider(ABC):
    @abstractmethod
    def current_user_id(self) -> UserId: ...

from abc import abstractmethod
from typing import TypeVar, Generic
from app.shared.idempotency.schemas import IdempotencyRecord

T = TypeVar("T")

class IdempotencyRepository(Generic[T]):

    @abstractmethod
    def get(self, key: str) -> IdempotencyRecord[T] | None:
        pass

    @abstractmethod
    def save(self, key: str, response: T):
        pass
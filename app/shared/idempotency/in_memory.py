from app.shared.idempotency.repository import IdempotencyRepository
from app.shared.idempotency.schemas import IdempotencyRecord
from typing import TypeVar

T = TypeVar("T")

class InMemoryIdempotencyRepository(IdempotencyRepository[T]):
    def __init__(self):
        super().__init__()
        self._keys: dict[str, IdempotencyRecord[T]] = {}

    def get(self, key) -> IdempotencyRecord[T]:
        return self._keys.get(key)

    def save(self, key, response: T) -> None:
        self._keys[key] = IdempotencyRecord(response=response)

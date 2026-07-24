from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class IdempotencyRecord(Generic[T]):
    response: T
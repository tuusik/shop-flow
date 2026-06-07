from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SPaginated(BaseSchema, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

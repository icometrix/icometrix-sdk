from pydantic import BaseModel
from typing import Dict, Generic, TypeVar, List, Optional

T = TypeVar("T")


class BackendEntity(BaseModel):
    id: str
    uri: Optional[str] = None
    update_timestamp: str
    creation_timestamp: str


class PaginatedResultSet(BaseModel):
    count: int
    offset: int
    limit: int


class PaginatedMetaData(BaseModel):
    result_set: PaginatedResultSet


class PaginatedResponse(BaseModel, Generic[T]):
    meta_data: PaginatedMetaData
    results: List[T]

    def has_next(self):
        result_set = self.meta_data.result_set
        return int(result_set.count) > (int(result_set.offset) + int(result_set.limit))


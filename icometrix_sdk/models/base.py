from pydantic import BaseModel
from typing import Generic, TypeVar, List, Optional, Iterator

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
    _itr_index: int

    def has_next(self) -> bool:
        """
        Returns True if there is a next page in the backend

        :return: bool
        """
        result_set = self.meta_data.result_set
        return int(result_set.count) > (int(result_set.offset) + int(result_set.limit))

    def __iter__(self) -> Iterator[T]:
        return iter(self.results)

    def __getitem__(self, index) -> T:
        return self.results[index]

    def __next__(self) -> T:
        if len(self.results) < self._itr_index:
            raise StopIteration

        item: T = self.results[self._itr_index]
        self._itr_index += 1
        return item

    def __len__(self) -> int:
        return len(self.results)

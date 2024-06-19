from datetime import datetime, timezone
from typing import Generic, TypeVar, List, Optional, Iterator, Literal

from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated

T = TypeVar("T")

DicomModality = Literal[
    "CR", "CT", "MR", "US", "OT", "BI", "CD", "DD", "DG", "ES", "LS", "PT", "RG", "ST", "TG", "XA",
    "RF", "HC", "DX", "NM", "MG", "IO", "PX", "GM", "SM", "XC", "PR", "AU", "EPS", "HD", "SR", "OP",
    "IVUS", "SMR", "RTIMAGE", "RTDOSE", "RTSTRUCT", "RTPLAN", "RTRECORD"]


def utc_datetime_parser(v: str | datetime | None) -> datetime | None:
    if not v:
        return None
    if isinstance(v, datetime):
        return v.replace(tzinfo=timezone.utc)

    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"
    input_datetime = datetime.strptime(v, datetime_format)
    return input_datetime.replace(tzinfo=timezone.utc)


# Does not work without the None
utc_datetime = Annotated[
    datetime | None,
    BeforeValidator(utc_datetime_parser),
]


class BackendEntity(BaseModel):
    id: str
    uri: Optional[str] = None
    update_timestamp: utc_datetime
    creation_timestamp: utc_datetime


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


class TestEntity(BaseModel):
    update_timestamp: Optional[utc_datetime] = None


test = TestEntity(update_timestamp='')
print(test)

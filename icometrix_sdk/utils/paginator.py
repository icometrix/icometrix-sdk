from inspect import signature
from typing import Callable, Generic, TypeVar, Optional, List

from icometrix_sdk.models.base import PaginatedResponse

T = TypeVar("T")


def can_paginate(func: Callable):
    """
    Checks if a function is iterable
    """
    sig = signature(func)
    return issubclass(sig.return_annotation, PaginatedResponse)


class PageIterator(Generic[T]):
    """
    An iterable object to iterate over paginated api responses
    """

    _current_page: Optional[PaginatedResponse[T]] = None

    def __init__(self, func: Callable, op_kwargs, page_size: int = 50, starting_index=0):
        self._func = func
        self._op_kwargs = op_kwargs
        self._page_size = page_size
        self._starting_index = starting_index
        self._page_index = starting_index
        self._params = {"pageIndex": self._page_index, "pageSize": self._page_size}

    def __iter__(self):
        self._page_index = self._starting_index
        self._params = {"pageIndex": self._page_index, "pageSize": self._page_size}
        return self

    def __next__(self) -> List[T]:
        if not self._current_page:
            self._fetch_current_page()
            return self._current_page.results
        if not self._current_page.has_next():
            raise StopIteration

        self._page_index = self._page_index + 1
        self._fetch_current_page()
        return self._current_page.results

    def _fetch_current_page(self):
        self._params = {"pageIndex": self._page_index, "pageSize": self._page_size}
        self._current_page = self._func(**self._op_kwargs, params=self._params)


def get_paginator(func: Callable, **kwargs):
    """
    Create paginator object for an operation.

    This returns an iterable object. Iterating over
    this object will yield a single page of a response
    at a time.
    """
    if not can_paginate(func):
        raise ValueError(f"Function '{func.__name__}' can't be paginated")

    sig = signature(func)
    return iter(PageIterator[sig.return_annotation](func, op_kwargs=kwargs))

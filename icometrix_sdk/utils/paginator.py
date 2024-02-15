from inspect import signature
from typing import Callable, Generic, TypeVar, Optional, Iterable, Any, ParamSpec

from icometrix_sdk.models.base import PaginatedResponse

T = TypeVar("T")
P = ParamSpec("P")


def can_paginate(func: Callable):
    """
    Checks if a function is iterable
    """
    sig = signature(func)
    return issubclass(sig.return_annotation, PaginatedResponse)


class PageIterator(Generic[T], Iterable):
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

    def __next__(self) -> PaginatedResponse[T]:
        if self._current_page is None:
            self._current_page = self._fetch_current_page()
            self._page_index = self._page_index + 1
            return self._current_page
        if not self._current_page.has_next():
            raise StopIteration

        self._page_index = self._page_index + 1
        self._current_page = self._fetch_current_page()
        return self._current_page

    def _fetch_current_page(self) -> PaginatedResponse[T]:
        self._params = {"pageIndex": self._page_index, "pageSize": self._page_size}
        if "params" in self._op_kwargs:
            self._op_kwargs["params"].update(self._params)
        else:
            self._op_kwargs["params"] = self._params
        return self._func(**self._op_kwargs)


def get_paginator(func: Callable[..., PaginatedResponse[T]],
                  page_size: Optional[int] = 50,
                  starting_index: Optional[int] = 0, **kwargs) -> PageIterator[T]:
    """
    Create paginator object for an operation.

    This returns an iterable object. Iterating over
    this object will yield a single page of a response
    at a time.

    :param func:
        The function that needs to be paginated. (The function needs
         to return a :class:`~icometrix_sdk.models.base.PaginatedResponse`)
    :param page_size:
        The size of the pages
    :param starting_index:
        The starting page
    :returns: A PageIterator
    """
    if not can_paginate(func):
        raise ValueError(f"Function '{func.__name__}' can't be paginated")

    # sig = signature(func)
    return PageIterator[T](func, op_kwargs=kwargs, page_size=page_size,
                           starting_index=starting_index)

from time import sleep
from typing import Callable, TypeVar

from icometrix_sdk.exceptions import WaitTimeoutException

T = TypeVar('T')


def wait_for(func: Callable[..., T], condition: Callable[[T], bool], timeout: int, **kwargs) -> T:
    pol = 5
    duration = 0
    val = func(**kwargs)
    while not condition(val):
        if timeout >= duration:
            WaitTimeoutException("The function took to long to complete")
        duration += pol
        sleep(pol)
        val = func(**kwargs)
    return val

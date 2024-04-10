from dataclasses import dataclass
from typing import Literal, get_args

Action = Literal["keep", "remove", "replace", "hash", "round"]
HashAlgo = Literal["sha3", "md5", "short_md5"]


@dataclass
class TagPolicy:
    """Class for defining a DICOM tag anonymization policy"""
    action: Action
    description: str
    value: int | str = None


Policy = dict[int, TagPolicy]

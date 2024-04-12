from dataclasses import dataclass
from typing import Literal, Callable
from pydicom import DataElement, Dataset

Action = Literal["keep", "empty", "remove", "replace", "hash", "round"]
HashAlgo = Literal["sha3", "md5", "short_md5"]
ReplaceFn = Callable[[DataElement, Dataset], None]


@dataclass
class TagPolicy:
    """
     represents a DICOM tag anonymization policy, defining how individual tags or groups should be anonymized.

    :param: Action to be performed on the tag (keep, remove, replace, hash, round)
    :param: Description of the tag anonymization policy.
    :param: Replace Function to be used when the action is "replace" (optional).

    Actions:
    - keep: Keep the original tag value.
    - remove: Remove the tag from the DICOM dataset.
    - replace: Replace the tag value with a specified :attr:`~icometrix_sdk.anonymizer.models.TagPolicy.value`.
    - hash: Hash the tag value using a specified algorithm.
    - round: Round the tag value to the nearest value. (currently only dates VRs are supported)

    """
    action: Action
    description: str

    # value: int | str = None
    replace_fn: ReplaceFn = None


Policy = dict[int, TagPolicy]

from pydicom import Dataset, DataElement

from icometrix_sdk.anonymizer.config import PATIENT_IDENTITY_REMOVED_TAG, DE_IDENTIFICATION_METHOD_TAG, \
    PRIVATE_ICOMETRIX_GROUPS
from icometrix_sdk.anonymizer.utils import _is_pixel_data


def _ignore_tag(tag: int) -> bool:
    # Tags that can be ignored during testing

    return ((_is_pixel_data(tag)
             or tag in (PATIENT_IDENTITY_REMOVED_TAG, DE_IDENTIFICATION_METHOD_TAG))
            or (tag >> 16 in PRIVATE_ICOMETRIX_GROUPS))


def _split_group_tags(dataset: Dataset, group: int) -> tuple[list[DataElement], list[DataElement]]:
    # A helper function to separate elements in a group, and not in a group (often needed for testing)
    in_group: list[DataElement] = []
    outside_group: list[DataElement] = []
    for element in dataset:
        tag = element.tag
        if tag.group == group:
            in_group.append(element)
        else:
            outside_group.append(element)
    return in_group, outside_group


def replace_by_value(value: str | int):
    def replace_vl(el: DataElement, _):
        el.value = value

    return replace_vl

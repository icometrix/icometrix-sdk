import pytest
from pydicom import DataElement, Dataset

from icometrix_sdk.anonymizer.tests.utils import replace_by_value
from icometrix_sdk.anonymizer.utils import replace_tag


def test_replace_existing_value():
    expected = "John^Doe"
    elem1 = DataElement(0x00100010, "PN", "Jane^Doe")
    replace_tag(elem1, Dataset(), replace_by_value(expected))

    assert elem1.value == expected


def test_replace_empty_value():
    expected = "072603.066406"
    elem1 = DataElement(0x00080050, "SH", "4753014.1")
    replace_tag(elem1, Dataset(), replace_by_value(expected))

    assert elem1.value == expected


def test_replace_with_to_long_value():
    expected = "072603.066406.to.long.value"
    elem1 = DataElement(0x00080050, "SH", "4753014.1")
    with pytest.raises(ValueError):
        replace_tag(elem1, Dataset(), replace_by_value(expected))


def test_replace_with_invalid_type_value():
    expected = 19
    elem1 = DataElement(0x00080020, "DA", "19700101")
    with pytest.raises(ValueError):
        replace_tag(elem1, Dataset(), replace_by_value(expected))

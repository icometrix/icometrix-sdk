import pytest
from pydicom import DataElement

from icometrix_sdk.anonymizer.utils import round_tag


# DA VR
def test_round_da_value():
    expected = "20180101"
    elem1 = DataElement(0x00080012, "DA", "20180629")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_empty_da_value():
    expected = ""
    elem1 = DataElement(0x00080012, "DA", "")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_invalid_short_da_value():
    expected = "1720"
    elem1 = DataElement(0x00080012, "DA", "1720")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_invalid_long_da_value():
    expected = "2500445566"
    elem1 = DataElement(0x00080012, "DA", "2500445566")
    round_tag(elem1)

    assert elem1.value == expected


# DT VR
def test_round_dt_value():
    expected = "20180101000000.000000"
    elem1 = DataElement(0x0008002A, "DT", "20180629072603.066406")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_empty_dt_value():
    expected = ""
    elem1 = DataElement(0x00080012, "DT", "")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_invalid_short_dt_value():
    expected = "17200101000000.000000"
    elem1 = DataElement(0x00080012, "DT", "17200204")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_invalid_long_dt_value():
    expected = "20180101000000.000000"
    elem1 = DataElement(0x00080012, "DT", "20180629072603.066406984135")
    round_tag(elem1)

    assert elem1.value == expected


# Numbers...
def test_round_int_value():
    expected = "20180101"
    elem1 = DataElement(0x00080012, "DA", "20180629")
    round_tag(elem1)

    assert elem1.value == expected


def test_round_unsupported_vr():
    elem1 = DataElement(0x00081000, "LO", "Model")
    with pytest.raises(ValueError):
        round_tag(elem1)

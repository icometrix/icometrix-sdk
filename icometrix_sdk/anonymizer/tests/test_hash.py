import pytest
from pydicom import DataElement
from pydicom.valuerep import MAX_VALUE_LEN

from icometrix_sdk.anonymizer.hash_factory import HashFactory, HashMethod
from icometrix_sdk.anonymizer.utils import hash_tag
from icometrix_sdk.anonymizer.utils import _cut_max_length


@pytest.fixture(scope="module")
def hash_algo() -> HashMethod:
    return HashFactory.create_hash_method("md5")


def test_hash_long_value(hash_algo: HashMethod):
    value = "Head"
    max_len = MAX_VALUE_LEN["LO"]

    expected = _cut_max_length(hash_algo.calculate_hash(value), max_len)

    elem1 = DataElement(0x00080013, "LO", value)
    hash_tag(elem1, hash_algo)

    assert elem1.value == expected


def test_hash_short_value(hash_algo: HashMethod):
    value = "4753014.1"
    max_len = MAX_VALUE_LEN["SH"]

    expected = _cut_max_length(hash_algo.calculate_hash(value), max_len)

    elem1 = DataElement(0x00080050, "SH", value)
    hash_tag(elem1, hash_algo)

    assert elem1.value == expected


def test_hash_number_value(hash_algo: HashMethod):
    elem1 = DataElement(0x00020000, "UL", 210)
    with pytest.raises(ValueError):
        hash_tag(elem1, hash_algo)


def test_hash_ui_value(hash_algo: HashMethod):
    value = "1.2.826.0.1.3680043.9.5542.5114248473116471214116117310121520961"
    expected = "1.2.826.0.1.3680043.9.5542.2676173402192025550109336474686546713"
    elem1 = DataElement(0x0020000D, "UI", value)
    hash_tag(elem1, hash_algo)
    assert elem1.value == expected

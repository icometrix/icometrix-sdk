from copy import deepcopy

import pydicom
import pytest
from pydicom import Dataset
from pydicom.data import get_testdata_file

from icometrix_sdk.anonymizer.anonymizer import Anonymizer
from icometrix_sdk.anonymizer.hash_factory import HashMethod, HashFactory
from icometrix_sdk.anonymizer.models import Policy, TagPolicy
from icometrix_sdk.anonymizer.tests.utils import _ignore_tag, _split_group_tags, replace_by_value


@pytest.fixture(scope="module")
def hash_algo() -> HashMethod:
    return HashFactory.create_hash_method("md5")


@pytest.fixture(scope="function")
def test_dataset() -> Dataset:
    dataset = pydicom.read_file(get_testdata_file("MR_small.dcm"))
    dataset.PatientBirthDate = "19930831"
    return dataset


keep_group: Policy = {
    0x0018: TagPolicy("keep", "Group18"),
}


def test_keep_group_policy(hash_algo: HashMethod, test_dataset: Dataset):
    original = deepcopy(test_dataset)
    anon = Anonymizer({}, keep_group, hash_algo)
    anon.anonymize(test_dataset)
    in_group, outside_group = _split_group_tags(test_dataset, 0x0018)
    for element in in_group:
        assert element.value == original[element.tag].value

    for element in outside_group:
        if _ignore_tag(element.tag):
            continue
        assert element.value in (0, 0.0, "")


hash_group: Policy = {
    0x0008: TagPolicy("hash", "HashGroup"),
}


def test_hash_policy(hash_algo: HashMethod, test_dataset: Dataset):
    original = deepcopy(test_dataset)
    anon = Anonymizer({}, hash_group, hash_algo)
    anon.anonymize(test_dataset)
    in_group, outside_group = _split_group_tags(test_dataset, 0x0008)

    un_hashable_vrs = ["CS", "DA", "TM"]
    for element in in_group:
        if not element.value or element.VR in un_hashable_vrs:
            continue
        assert element.value != original[element.tag].value

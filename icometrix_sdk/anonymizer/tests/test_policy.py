from copy import deepcopy

import pydicom
import pytest
from pydicom import Dataset
from pydicom.data import get_testdata_file

from icometrix_sdk.anonymizer.anonymizer import Anonymizer
from icometrix_sdk.anonymizer.constants import PATIENT_IDENTITY_REMOVED_TAG, DE_IDENTIFICATION_METHOD_TAG
from icometrix_sdk.anonymizer.hash_factory import HashMethod, HashFactory
from icometrix_sdk.anonymizer.models import Policy, TagPolicy
from icometrix_sdk.anonymizer.tests.utils import _ignore_tag
from icometrix_sdk.anonymizer.utils import _is_pixel_data


@pytest.fixture(scope="module")
def hash_algo() -> HashMethod:
    return HashFactory.create_hash_method("md5")


@pytest.fixture(scope="function")
def test_dataset() -> Dataset:
    dataset = pydicom.read_file(get_testdata_file("MR_small.dcm"))
    dataset.PatientBirthDate = "19930831"
    return dataset


remove_all: Policy = {}


def test_remove_all_policy(hash_algo: HashMethod, test_dataset: Dataset):
    anon = Anonymizer(remove_all, remove_all, hash_algo)
    anon.anonymize(test_dataset)
    for element in test_dataset:
        if _ignore_tag(element.tag):
            continue

        assert element.value in (0, 0.0, "")


keep_values: Policy = {
    0x00180081: TagPolicy("keep", "EchoTime"),
    0x00100040: TagPolicy("keep", "PatientsSex"),
}


def test_keep_policy(hash_algo: HashMethod, test_dataset: Dataset):
    original = deepcopy(test_dataset)
    anon = Anonymizer(keep_values, {}, hash_algo)
    anon.anonymize(test_dataset)
    for tag in keep_values:
        assert test_dataset[tag].value == original[tag].value


hash_values: Policy = {
    0x00080018: TagPolicy("hash", "SOPInstanceUID"),
    0x0020000e: TagPolicy("hash", "SeriesInstanceUID"),
    0x00100020: TagPolicy("hash", "PatientId"),
}


def test_hash_policy(hash_algo: HashMethod, test_dataset: Dataset):
    original = deepcopy(test_dataset)
    anon = Anonymizer(hash_values, {}, hash_algo)
    anon.anonymize(test_dataset)
    for tag in hash_values:
        assert test_dataset[tag].value != original[tag].value


replace_values: Policy = {
    0x00100010: TagPolicy("replace", "PatientName", "Doe^John"),
    0x00080080: TagPolicy("replace", "InstitutionName", "Mordor"),
}


def test_replace_policy(hash_algo: HashMethod, test_dataset: Dataset):
    anon = Anonymizer(replace_values, {}, hash_algo)
    anon.anonymize(test_dataset)
    for tag in replace_values:
        assert test_dataset[tag].value == replace_values[tag].value


def test_invalid_replace_policy(hash_algo: HashMethod, test_dataset: Dataset):
    with pytest.raises(ValueError):
        anon = Anonymizer({0x00100010: TagPolicy("replace", "PatientName", 10)}, {}, hash_algo)
        anon.anonymize(test_dataset)

    with pytest.raises(ValueError):
        anon2 = Anonymizer({0x00080080: TagPolicy("replace", "InstitutionName")}, {}, hash_algo)
        anon2.anonymize(test_dataset)


round_values: Policy = {
    0x00100030: TagPolicy("round", "PatientBirthDate"),
}


def test_round_policy(hash_algo: HashMethod, test_dataset: Dataset):
    anon = Anonymizer(round_values, {}, hash_algo)
    anon.anonymize(test_dataset)
    for tag in round_values:
        assert test_dataset[tag].value.endswith("0101")

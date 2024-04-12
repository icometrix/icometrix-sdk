import copy

import pydicom
import pytest

from icometrix_sdk.anonymizer.anonymizer import Anonymizer
from icometrix_sdk.anonymizer.exceptions import PolicyException
from icometrix_sdk.anonymizer.hash_factory import HashMethod, HashFactory
from icometrix_sdk.anonymizer.models import Policy, TagPolicy
from icometrix_sdk.anonymizer.policy import policy_sha, policy_md5, group_policy
from icometrix_sdk.anonymizer.tests.utils import _ignore_tag


@pytest.fixture(scope="module")
def hash_algo() -> HashMethod:
    return HashFactory.create_hash_method("md5")


tags: Policy = {
    0x00180081: TagPolicy("keep", "EchoTime"),
}

groups: Policy = {
    0x0018: TagPolicy("keep", "Group 18"),
}


def test_valid_constructor(hash_algo: HashMethod):
    Anonymizer(tags, groups, hash_algo)


def test_invalid_constructor(hash_algo: HashMethod):
    with pytest.raises(PolicyException):
        Anonymizer(groups, groups, hash_algo)

    with pytest.raises(PolicyException):
        Anonymizer(tags, tags, hash_algo)


def test_full_md5(hash_algo: HashMethod):
    anonymizer = Anonymizer(policy_md5, group_policy, hash_algo)

    original_ds = pydicom.dcmread(f"datasets/original.dcm")
    expected_ds = pydicom.dcmread(f"datasets/anonymized_md5.dcm")

    anonymized_ds = anonymizer.anonymize(copy.deepcopy(original_ds))

    for element in anonymized_ds:
        tag = element.tag
        if element.VR == "SQ" or _ignore_tag(tag):
            continue

        assert anonymized_ds[tag].value == expected_ds[tag].value


def test_full_sha3(hash_algo: HashMethod):
    anonymizer = Anonymizer(policy_sha, group_policy, hash_algo)

    original_ds = pydicom.dcmread(f"datasets/original.dcm")
    expected_ds = pydicom.dcmread(f"datasets/anonymized_sha3.dcm")

    anonymized_ds = anonymizer.anonymize(copy.deepcopy(original_ds))

    for element in anonymized_ds:
        tag = element.tag
        if element.VR == "SQ" or _ignore_tag(tag):
            continue

        assert anonymized_ds[tag].value == expected_ds[tag].value

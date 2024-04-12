from pathlib import Path

import pydicom
from pydicom.config import WARN
from pydicom.data import get_testdata_files

from icometrix_sdk.anonymizer.anonymizer import Anonymizer
from icometrix_sdk.anonymizer.hash_factory import HashFactory
from icometrix_sdk.anonymizer.policy import policy_sha, group_policy

# set env VALIDATION_MODE to 1 or 0, there are some invalid DICOMs in this set

# These files are included in the pydicom test dataset to test failed dcmread
INVALID_FILES = [
    "ExplVR_BigEndNoMeta.dcm",
    "ExplVR_LitEndNoMeta.dcm",
    "no_meta.dcm",
    "rtstruct.dcm",
    "OT-PAL-8-face.dcm",
]


def get_dicom_test_files():
    all_files = get_testdata_files("*.dcm")
    return [x for x in all_files if Path(x).name not in INVALID_FILES]


hash_algo = HashFactory.create_hash_method("md5")
anon = Anonymizer(policy_sha, group_policy, hash_algo)

for file_path in get_dicom_test_files():
    dataset = pydicom.dcmread(f"{file_path}")
    anon.anonymize(dataset).save_as(f"out/anon-{Path(file_path).name}")

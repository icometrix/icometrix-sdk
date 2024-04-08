import os

import pydicom

from icometrix_sdk.anonymizer.anonymizer import Anonymizer
from icometrix_sdk.anonymizer.hash_factory import HashFactory
from icometrix_sdk.anonymizer.policy import policy, group_policy

file_paths = os.listdir("<data_dir>")

hash_algo = HashFactory.create_hash_method("ico_md5")
anon = Anonymizer(policy, group_policy, hash_algo)

for file_path in file_paths:
    dataset = pydicom.dcmread(f"out/{file_path}")
    anon.anonymize(dataset).save_as(f"out/anon-{file_path}")

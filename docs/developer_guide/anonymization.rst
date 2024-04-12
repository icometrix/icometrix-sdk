Anonymization
=============

The :class:`~icometrix_sdk.anonymizer.anonymizer.Anonymizer` provides functionality for anonymizing DICOM datasets
according to specified policies.


Policies
--------

A Policy is a dictionary with the key bing a DICOM tag and the value a :class:`~icometrix_sdk.anonymizer.models.TagPolicy`
This defines how individual tags or groups should be anonymized.

.. code-block:: python

    from icometrix_sdk.anonymizer.models import TagPolicy, Policy
    from icometrix_sdk.anonymizer.hash_factory import SHA3

    def replace_vl(el: DataElement, _):
        el.value = "Jane^Doe"

    def sha3_hash(element: DataElement, _):
        element.value = SHA3(size=512).calculate_hash(element.value)[:64]

    # A policy defining how tags should be anonymized
    policy: Policy = {
        0x00080020: TagPolicy("keep", "StudyDate"), # Don't change the StudyDate
        0x0020000d: TagPolicy("hash", "StudyInstanceUID"), # Hash the StudyInstanceUID by the default hash function
        0x00100010: TagPolicy("replace", "PatientName", replace_fn=replace_vl), # Replace the PatientName by "Jane^Doe"
        0x00100020: TagPolicy("replace", "PatientID", replace_fn=sha3_hash), # Replace the PatientID by a sha3 hash of the PatientID
        0x00100030: TagPolicy("round", "PatientBirthday"), # Round the PatientBirthday to YYYY0101
    }

    # A policy defining how groups should be anonymized
    group_policy: Policy = {
        0x0018: TagPolicy("keep", "Acquisition: mage acquisition device and imaging procedure"),
        0x5200: TagPolicy("keep", "Multi-frame Functional Groups"),
    }

Anonymizer
----------

The :class:`~icometrix_sdk.anonymizer.anonymizer.Anonymizer` requires 3 parameters:

- policy: a Policy for DICOM tags
- group_policy: a Policy for DICOM groups
- hash_algo: The hash algorithm you want to use when using a hash :attr:`~icometrix_sdk.anonymizer.models.TagPolicy.action`


.. code-block:: python

    from icometrix_sdk.anonymizer.anonymizer import Anonymizer
    from icometrix_sdk.anonymizer.hash_factory import HashFactory
    from pydicom.data import get_testdata_file

    hash_algo = HashFactory.create_hash_method("md5")

    # You can use the policy examples above, make your own or import one:
    # from icometrix_sdk.anonymizer.policy import policy, group_policy
    anonymizer = Anonymizer(policy, group_policy, hash_algo)

    dataset = pydicom.read_file(get_testdata_file("MR_small.dcm"))

    anonymizer.anonymize(dataset).save_as("anonymized_MR_small.dcm")


Settings
--------
Some default behaviour can be overwritten by setting environment variables:

- ROOT_UID: The root of UID used when hashing DICOM tags with the VR UI (https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_B.html)
- VALIDATION_MODE: and int defining how validation should be done (0: ignore, 1:warn, 2: raise),

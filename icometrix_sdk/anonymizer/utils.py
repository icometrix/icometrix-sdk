from pydicom import DataElement, Dataset
from pydicom.valuerep import INT_VR, FLOAT_VR, validate_value, MAX_VALUE_LEN

from icometrix_sdk.anonymizer.config import ROOT_UID, PATIENT_IDENTITY_REMOVED_TAG, DE_IDENTIFICATION_METHOD_TAG, \
    VALIDATION_MODE
from icometrix_sdk.anonymizer.hash_factory import ShortMD5, SHA3
from icometrix_sdk.anonymizer.models import ReplaceFn


def is_group(tag: int) -> bool:
    # Will fail on 0x00000000, but this does not exist in DICOM...
    return (tag >> 16) == 0


def is_tag(tag: int) -> bool:
    # Same as is group will fail on 0x00000000, but this does not exist in DICOM...
    return (tag >> 16) != 0


def _is_pixel_data(tag: int) -> bool:
    return tag == 0x7fe00010


def _is_numeric_vr(vr: str) -> bool:
    return vr in FLOAT_VR or vr in INT_VR


def empty_tag(element: DataElement):
    """
    Empties the value of the DICOM element.
    For numeric VRs, sets the value to 0.
    For other VRs, sets the value to an empty string.
    """

    if _is_numeric_vr(element.VR):
        element.value = 0
    else:
        element.value = ""


def remove_tag(element: DataElement, dataset: Dataset):
    """
    Removes the tag from a dataset
    """
    tag = element.tag
    if tag in dataset:
        del dataset[tag]


def replace_tag(element: DataElement, dataset: Dataset, replace_fn: ReplaceFn):
    """
    Replaces the value of the DICOM element with a new value.
    Raises an ValueError Exception if the new value is not compatible with the VR of the DICOM element.

    value: The new value to replace the current value of the DICOM element.
    """
    if replace_fn is None:
        raise ValueError("No Replace function provided to the policy")
    replace_fn(element, dataset)
    validate_value(element.VR, element.value, validation_mode=VALIDATION_MODE)


def _hash_uid(element: DataElement, hash_method):
    """
    Calculates the hash of the value of the DICOM UID element
    """
    max_len = 64
    hashed = hash_method.calculate_hash(element.value)
    # Convert hash in hexadecimal format to decimal format
    # Requirement of DICOM UIDs that they only exist of digits
    # See https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_9.html
    hashed = str(int(hashed, base=16))

    # Dicom 9.1: The first digit of each component shall not be zero,
    # unless the component is a single digit.
    # See https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_9.html
    extra = ""
    if hashed[0] == "0":
        extra = "9"
    new_value = f"{ROOT_UID}.{extra}{hashed}"

    # DICOM 9.1: UIDs, shall not exceed 64 total characters
    return _cut_max_length(new_value, max_len)


def _cut_max_length(value: str, max_len: int) -> str:
    if max_len and len(value) > max_len:
        value = value[:max_len]
    return value


def hash_tag(element: DataElement, hash_method):
    """
    Calculates the hash of the value of the DICOM element
    """

    if _is_numeric_vr(element.VR):
        raise ValueError(f"Cant hash VR {element.VR}")

    if element.VR == "UI":
        hashed = _hash_uid(element, hash_method)
    else:
        hashed = hash_method.calculate_hash(element.value)
        if element.VR in MAX_VALUE_LEN:
            hashed = _cut_max_length(hashed, MAX_VALUE_LEN[element.VR])

    validate_value(element.VR, hashed, validation_mode=VALIDATION_MODE)
    element.value = hashed


def _round_da(element: DataElement):
    """
    The structure of a DA is YYYYMMDD
    This will be rounded to YYYY0101
    """
    if len(element.value) != 8:
        return
    element.value = element.value[:4] + "0101"


def _round_dt(element: DataElement):
    """
    The structure of a DT is  YYYYMMDDHHMMSS.FFFFFF&ZZXX (&ZZXX is an optional suffix for offset from UTC)
    This will be rounded to YYYY01010000.000000
    """
    if not element.value:
        return
    element.value = element.value[:4] + "0101000000.000000"


def _round_tm(element: DataElement):
    """
    The structure of a DT is  YYYYMMDDHHMMSS.FFFFFF&ZZXX (&ZZXX is an optional suffix for offset from UTC)
    This will be rounded to YYYY01010000.000000
    """
    if not element.value:
        return
    element.value = "000001.00000"


def round_tag(element: DataElement):
    if element.VR == "DA":
        _round_da(element)
    elif element.VR == "DT":
        _round_dt(element)
    elif element.VR == "TM":
        _round_tm(element)
    else:
        raise ValueError(f"Cant round VR {element.VR}")


def add_de_identification_tags(dataset: Dataset) -> Dataset:
    # Field "PatientIdentityRemoved"
    # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120062
    dataset.add_new(PATIENT_IDENTITY_REMOVED_TAG, "LT", "YES")

    # Field "De-identification method"
    # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120063
    dataset.add_new(DE_IDENTIFICATION_METHOD_TAG, "LT",
                    "Python based, HIPAA compliant, based on DICOM PS3.15 AnnexE.")
    return dataset


def short_md5_hash(element: DataElement, _):
    value = element.value
    if len(value) % 2 != 0:
        value += " "
    element.value = ShortMD5().calculate_hash(value)


def short_sha3_hash(element: DataElement, _):
    value = str(element.value)
    if len(value) % 2 != 0:
        value += " "
    element.value = SHA3(size=512).calculate_hash(value)[:10]


def remove_if_birthday(element: DataElement, ds: Dataset):
    if ds[0x00100030].value:
        del ds[element.tag]

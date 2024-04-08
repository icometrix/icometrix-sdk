from pydicom import DataElement, Dataset
from pydicom.valuerep import INT_VR, FLOAT_VR, validate_value

from icometrix_sdk.anonymizer.constants import ROOT_UID, PATIENT_IDENTITY_REMOVED_TAG, DE_IDENTIFICATION_METHOD_TAG


def _is_pixel_data(tag: int) -> bool:
    return tag == 0x7fe00010


def _is_numeric_vr(vr: str) -> bool:
    return vr in FLOAT_VR or vr in INT_VR


def _is_in_group(tag: int, group: int):
    lower_bound = group * 0x10000
    upper_bound = group * 0x10000 + 0xffff
    return lower_bound <= tag <= upper_bound


def remove_tag(element: DataElement):
    """
    Empties the value of the DICOM element.
    For numeric VRs, sets the value to 0.
    For other VRs, sets the value to an empty string.
    """

    if _is_numeric_vr(element.VR):
        element.value = 0
    else:
        element.value = ""


def replace_tag(element: DataElement, value: any):
    """
    Replaces the value of the DICOM element with a new value.
    Raises an ValueError Exception if the new value is not compatible with the VR of the DICOM element.

    new_value: The new value to replace the current value of the DICOM element.
    """
    validate_value(element.VR, value, validation_mode=2)
    element.value = value


def _hash_ui(element: DataElement, hash_method):
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
    if len(new_value) > max_len:
        new_value = new_value[:max_len]
    return new_value


def hash_tag(element: DataElement, hash_method):
    """
    Calculates the hash of the value of the DICOM element
    """

    if _is_numeric_vr(element.VR):
        raise Exception(f"Cant hash VR {element.VR}")

    if element.VR == "UI":
        hashed = _hash_ui(element, hash_method)
    elif element.VR == "SH":
        hashed = hash_method.calculate_hash(element.value)

        max_len = 16
        if max_len and len(hashed) > max_len:
            hashed = hashed[:max_len]
    else:
        hashed = hash_method.calculate_hash(element.value)

    element.value = hashed


def round_tag(element: DataElement):
    if _is_numeric_vr(element.VR):
        rounded = round(element.value / 10) * 10
    elif element.VR == "DA":
        rounded = element.value[:4] + "0101"
    else:
        raise Exception(f"Cant round VR {element.VR}")

    element.value = rounded


def add_de_identification_tags(dataset: Dataset) -> Dataset:
    # Field "PatientIdentityRemoved"
    # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120062
    dataset.add_new(PATIENT_IDENTITY_REMOVED_TAG, "LT", "YES")

    # Field "Deidentification method"
    # See https://dicom.innolitics.com/ciods/rt-plan/patient/00120063
    dataset.add_new(DE_IDENTIFICATION_METHOD_TAG, "LT",
                    "Python based, HIPAA compliant, based on DICOM PS3.15 AnnexE.")
    return dataset

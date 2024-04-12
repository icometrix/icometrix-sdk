import os
from pydicom.config import RAISE

# Organization root, default to icometrix (https://dicom.nema.org/dicom/2013/output/chtml/part05/chapter_B.html)
ROOT_UID: str = os.getenv("ROOT_UID", "1.2.826.0.1.3680043.9.5542")
VALIDATION_MODE: int = int(os.getenv("VALIDATION_MODE", RAISE))

PATIENT_IDENTITY_REMOVED_TAG: int = 0x00120062
DE_IDENTIFICATION_METHOD_TAG: int = 0x00120063
PRIVATE_ICOMETRIX_GROUPS: list[int] = [0x0009, 0x0015, 0x0017]

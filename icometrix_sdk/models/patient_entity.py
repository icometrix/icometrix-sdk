from typing import Optional, Union
from icometrix_sdk.models.base import BackendEntity


class PatientEntity(BackendEntity):
    icon: Optional[str] = None
    alias: Optional[str] = None
    label: Optional[str] = None
    cohort: Optional[str] = None
    country: Optional[str] = None
    hospital: Optional[str] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    birth_year: Optional[Union[str, int]] = None
    patient_id: str
    project_id: str
    invite_code: Optional[str] = None
    patient_sex: Optional[str] = None
    patient_name: str
    project_name: Optional[str] = None
    trial_excluded: Optional[Union[str, bool]] = None
    project_country: Optional[str] = None
    msbase_patient_id: Optional[str] = None
    unique_patient_id: Optional[str] = None
    imported_timestamp: Optional[str] = None
    patient_birth_date: str
    patient_handedness: Optional[str] = None
    encrypted_patient_id: Optional[str] = None
    encrypted_patient_name: Optional[str] = None
    encrypted_patient_birth_date: Optional[str] = None

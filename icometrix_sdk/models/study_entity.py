import datetime
from typing import Optional, Union

from pydantic import field_validator

from icometrix_sdk.exceptions import IcometrixInvalidInputDataException
from icometrix_sdk.models.base import BackendEntity, DicomModality


class StudyEntity(BackendEntity):
    modality: DicomModality
    patient_id: str
    project_id: str

    study_date: str  # DICOM formatted study date, e.g. 20100513
    study_note: Optional[str] = None
    study_time: str  # DICOM formatted study time
    patient_age: Optional[Union[int, str]] = None  # Can be something like 035Y
    manufacturer: Optional[str] = None
    accession_number: Optional[str] = None
    institution_name: Optional[str] = None
    study_description: Optional[str] = None
    study_instance_uid: Optional[str] = None
    scheduled_timestamp: Optional[str] = None
    device_serial_number: Optional[str] = None
    icobrain_report_type: Optional[str] = None
    magnetic_field_strength: Optional[str] = None
    manufacturer_model_name: Optional[str] = None
    imported_timestamp: Optional[datetime.datetime] = None

    @field_validator("study_date")
    def is_valid_study_date(cls, value):
        if value.isdigit() and int(value) > 0 and len(value) == 8:
            return value
        else:
            raise IcometrixInvalidInputDataException(
                "Study date does not follow DICOM format (e.g. 20220117)")

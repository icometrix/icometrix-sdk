from typing import Optional, Union, List
from pydantic import BaseModel
from icometrix_sdk.models.base import BackendEntity


class CustomerReportFile(BaseModel):
    uri: str
    name: str
    type: str


class CustomerReportEntity(BackendEntity):
    cost: Optional[Union[str, float]] = None
    status: str
    study_id: str
    upload_id: Optional[str] = None
    patient_id: str
    project_id: str
    study_date: Optional[str] = None
    report_type: Optional[str] = None
    patient_name: Optional[str] = None
    project_name: str
    report_files: List[CustomerReportFile]
    report_status: Optional[str] = None
    project_country: str
    accession_number: Optional[str] = None
    dicom_patient_id: Optional[str] = None
    customer_result_id: Optional[str] = None
    pipeline_result_id: Optional[str] = None
    study_instance_uid: str
    icobrain_report_type: str
    report_translated_remarks: Optional[str] = None

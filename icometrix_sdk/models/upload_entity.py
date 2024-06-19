from typing import Optional, List, Union, Literal

from pydantic import BaseModel

from icometrix_sdk.models.base import BackendEntity


class StartUploadDto(BaseModel):
    icobrain_report_type: Literal['icobrain_ms', 'icobrain_dm']


class UploadEntity(BackendEntity):
    status: Optional[str] = None
    folder_uri: str
    type: str
    compressed: Optional[Union[str, bool]] = None
    logs: List[str]
    errors: List[str]
    icobrain_report_type: str
    retry_count: Optional[Union[str, int]] = None
    project_id: str

    def __str__(self):
        latest_log = self.logs[-1] if self.logs else '-'
        log_message = (
            f"Upload ID: {self.id[:8]} | "
            f"Status: {self.status} | "
            f"Logs: {latest_log}"
        )
        return log_message

    def __repr__(self):
        return str(self)


class StudyUploadEntity(BackendEntity):
    project_id: str
    patient_id: str
    study_id: str
    upload_id: str


class UploadEntityFiles(BaseModel):
    files: List[str]

from typing import Optional, List, Union, Literal

from pydantic import BaseModel

from icometrix_sdk.models.base import BackendEntity


class StartUploadDto(BaseModel):
    icobrain_report_type: Literal['icobrain_ms', 'icobrain_dm']


class UploadEntity(BackendEntity):
    status: str
    folder_uri: str
    type: str
    compressed: Optional[Union[str, bool]] = None
    logs: List[str]
    errors: List
    icobrain_report_type: str
    retry_count: Optional[Union[str, int]] = None
    id: str
    project_id: str
    creation_timestamp: str
    update_timestamp: str
    file_name: str
    uri: str


class UploadEntityFiles(BaseModel):
    files: List[str]

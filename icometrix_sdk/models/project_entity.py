from typing import Optional

from icometrix_sdk.models.base import BackendEntity


class ProjectEntity(BackendEntity):
    name: str
    state: Optional[str] = None
    abbrev: str
    country: str
    description: Optional[str] = None
    display_name: Optional[str] = None
    project_type: Optional[str] = None
    processing_type: Optional[str] = None
    imported_timestamp: Optional[str] = None

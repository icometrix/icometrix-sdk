from pydantic import BaseModel
from typing_extensions import Optional

from icometrix_sdk.models.base import BackendEntity


class CustomerResultPipelineResults(BaseModel):
    pipeline_results_id: Optional[str] = None


class CustomerResultEntity(BackendEntity):
    uri: str
    job_id: str
    study_id: str
    patient_id: str
    project_id: str
    qc_result_id: str
    pipeline_results: CustomerResultPipelineResults

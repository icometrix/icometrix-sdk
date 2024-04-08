from typing import Optional, Literal, Union

from icometrix_sdk.models.base import BackendEntity

PipelineResultType = Literal[
    "unusable_finalization",
    "icobrain_mr_cross",
    "icobrain_ctp_cross",
    "icobrain_mt",
    "icobrain_ct_cross",
    "protocol_validation",
    "icobrain_preprocessing",
    "harmonization_constants",
    "icobrain_diffusion",
    "pdf2dicom",
    "icolung",
    "icobrain_mr_cross_research",
    "icobrain_mr_cross_manual_corrections",
    "icospine_cross",
    "icobrain_mt_cross",
]
PipelineResultJobType = Literal[
    "overread",
    "corrected",
    "curated",
    "initial",
]


class PipelineResultEntity(BackendEntity):
    image: str
    job_id: str
    results: any
    job_mode: Optional[Union[PipelineResultJobType, str]] = None
    pipeline: Union[PipelineResultType, str]
    study_id: str
    patient_id: str
    project_id: str
    run_parameters: dict
    automatic_qc_results: Optional[dict] = None
    software_version_data: dict

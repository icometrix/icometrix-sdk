from datetime import timedelta
from typing import Literal, Optional

from pydantic import BaseModel

from icometrix_sdk.models.base import BackendEntity, utc_datetime
from icometrix_sdk.utils.time_diff import time_difference


class JobParameters(BaseModel):
    pipeline_json_file: str
    pipeline_parameters_json_file: str
    run_parameters_json_string: str
    docker_image: str


class JobEntity(BackendEntity):
    status: str
    parameters: JobParameters
    comment: str
    # console_log: str
    job_type: str  # Optional[Literal['cross_processsing', 'long_processsing', 'preprocessing']] = None
    finished_timestamp: Optional[utc_datetime] = None
    reschedule_counter: Optional[str | int] = None
    job_mode: Optional[str] = None
    study_ids: list[str]
    project_id: str
    patient_id: str
    operator_id: str
    reference_job_id: Optional[str] = None

    def running_time(self) -> timedelta:
        if not self.finished_timestamp:
            return time_difference(self.creation_timestamp)
        return self.finished_timestamp - self.creation_timestamp

    def __str__(self):
        return (
            f"Job ID: {self.id[:8]} | "
            f"Status: {self.status} | "
            f"Job Type: {self.job_type} | "
            f"Running Time: {self.running_time()}"
        )

    def __repr__(self):
        return str(self)


class StartPreProcessing(BaseModel):
    # patient_id: str
    # project_id: str
    # study_id: str
    # study_uri: str
    # docker_image: str
    icobrain_report_type: Literal['icobrain_ms', 'icobrain_dm']
    icobrain_report_language: Optional[str] = None
    # report_languages: list[str]
    force_reprocessing: Optional[bool] = False
    disable_quality_control: Optional[bool] = False
    # type: str


class StartCrossProcessing(BaseModel):
    # patient_id: str
    # project_id: str
    # study_id: str
    # study_uri: str
    t1_uri: Optional[str] = None
    t1_post_uri: Optional[str] = None
    flair_uri: Optional[str] = None
    ct_uri: Optional[str] = None
    t2star_uri: Optional[str] = None
    t2_uri: Optional[str] = None
    pd_uri: Optional[str] = None
    swi_uri: Optional[str] = None
    mt_on_uri: Optional[str] = None
    mt_off_uri: Optional[str] = None
    dmri_uri: Optional[str] = None
    t1_contrast_enhanced: Optional[str] = None
    # comment: Optional[str]
    # docker_image: str
    # resource_requirements: Resourcerequirements;
    icobrain_report_type: Literal['icobrain_ms', 'icobrain_dm']
    icobrain_report_language: Optional[str] = None
    # report_languages: list[str]
    force_reprocessing: Optional[bool] = False
    disable_quality_control: Optional[bool] = False
    # type: str
    # quality_control_options: Resourcerequirements;
    # scientific_options: Resourcerequirements;
    # job_mode: str

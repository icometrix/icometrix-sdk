import logging

from icometrix_sdk.logger import logger_name
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.pipeline_result_entity import PipelineResultEntity
from icometrix_sdk.utils.paginator import get_paginator
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(logger_name)


class PipelineResults:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all_for_study(self, study_uri: str, **kwargs) -> PaginatedResponse[PipelineResultEntity]:
        """
        Get al pipeline reports for a project

        :param study_uri: The uri of a study
        :return: A Paginated response containing pipeline-results
        """

        study_uri = study_uri.replace("/v1/", "/v2/")
        page = self._api.get(f"{study_uri}/pipeline-results", **kwargs)
        return PaginatedResponse[PipelineResultEntity](**page)

    def get_one_for_job(self, study_uri: str, job_id: str) -> PipelineResultEntity | None:
        """
        Get a pipeline result for a job

        :param study_uri: The uri of a study
        :param job_id: The id of the job
        """
        page = get_paginator(self.get_all_for_study, study_uri=study_uri)
        for pipeline_results in page:
            for pipeline_result in pipeline_results:
                if pipeline_result.job_id == job_id:
                    return pipeline_result

    def get_one(self, pipeline_result_uri: str) -> PipelineResultEntity:
        """
        Get a single customer-result based on the customer-result uri

        :param pipeline_result_uri: the uri of the pipeline-result
        :return: A single pipeline-result or 404
        """
        resp = self._api.get(pipeline_result_uri)
        return PipelineResultEntity(**resp)

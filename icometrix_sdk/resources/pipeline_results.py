import logging

from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.pipeline_result_entity import PipelineResultEntity
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(__name__)


class PipelineResults:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all_for_study(self, study_uri: str, **kwargs) -> PaginatedResponse[PipelineResultEntity]:
        """
        Get al pipeline reports for a project

        :param study_uri: The uri of a study
        :return: A Paginated response containing pipeline-results
        """

        page = self._api.get(f"{study_uri}/pipeline-results", **kwargs)
        return PaginatedResponse[PipelineResultEntity](**page)

    def get_one(self, pipeline_result_uri: str) -> PipelineResultEntity:
        """
        Get a single customer-result based on the customer-result uri

        :param pipeline_result_uri: the uri of the pipeline-result
        :return: A single pipeline-result or 404
        """
        resp = self._api.get(pipeline_result_uri)
        return PipelineResultEntity(**resp)


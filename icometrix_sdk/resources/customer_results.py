import logging

from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.customer_result_entity import CustomerResultEntity
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(__name__)


class CustomerResults:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all_for_study(self, study_uri: str, **kwargs) -> PaginatedResponse[CustomerResultEntity]:
        """
        Get al customer reports for a project

        :param study_uri: The uri of a study
        :return: A Paginated response containing customer-results
        """

        page = self._api.get(f"{study_uri}/customer-results", **kwargs)
        return PaginatedResponse[CustomerResultEntity](**page)

    def get_all_for_pipeline_result(self, pipeline_result_uri: str, **kwargs) -> \
            PaginatedResponse[CustomerResultEntity]:
        """
        Get al customer reports for a pipeline-result

        :param pipeline_result_uri: The uri of a pipeline-result
        :return: A Paginated response containing customer-results
        """

        page = self._api.get(f"{pipeline_result_uri}/customer-results", **kwargs)
        return PaginatedResponse[CustomerResultEntity](**page)

    def get_one(self, customer_result_uri: str) -> CustomerResultEntity:
        """
        Get a single customer-result based on the customer-result uri

        :param customer_result_uri: the uri of the customer-result
        :return: A single customer-result or 404
        """
        resp = self._api.get(customer_result_uri)
        return CustomerResultEntity(**resp)

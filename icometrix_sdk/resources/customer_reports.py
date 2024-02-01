from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.customer_report_entity import CustomerReportEntity
from icometrix_sdk.utils.api_client import ApiClient


class CustomerReports:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all(self, project_id: str, **kwargs) -> PaginatedResponse[CustomerReportEntity]:
        """
        Get al customer reports for a project

        :param project_id: The ID of the project you want to fetch the customer-reports from
        :return: A Paginated response containing customer-reports
        """

        page = self._api.get(f"/customer-reports-service/api/v2/projects/{project_id}/customer-reports", **kwargs)
        return PaginatedResponse[CustomerReportEntity](**page)

    def get_one(self, customer_report_uri: str) -> CustomerReportEntity:
        """
        Get a single customer-report based on the customer-report uri

        :param customer_report_uri: the uri of the customer-report
        :return: A single customer-report or 404
        """
        resp = self._api.get(customer_report_uri)
        return CustomerReportEntity(**resp)

    def delete(self, customer_report_uri: str, **kwargs):
        """
        Delete a customer-report

        :param customer_report_uri: The uri of the customer-resport you want to delete
        :return:
        """

        self._api.delete(customer_report_uri, **kwargs)

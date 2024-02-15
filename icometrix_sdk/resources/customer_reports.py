import logging
from time import sleep
from typing import Optional, Dict, List

from icometrix_sdk.exceptions import IcometrixDataImportException
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.customer_report_entity import CustomerReportEntity, CustomerReportFile
from icometrix_sdk.utils.paginator import get_paginator
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(__name__)


class CustomerReports:
    def __init__(self, api: ApiClient, polling_interval=2):
        self._api = api
        self.polling_interval = polling_interval

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

    def download_customer_report_files(self, customer_report: CustomerReportEntity, out_path: Optional[str] = None):
        """
        Download all files created by icobrain for a customer_report

        :param customer_report: The customer report you want to download the files from
        :param out_path: A folder path to write the files to
        :return:
        """
        for report_file in customer_report.report_files:
            out_path_file = f"{out_path}/{report_file.name}"
            self.download_customer_report_file(report_file, out_path_file)

    def download_customer_report_file(self, customer_report_file: CustomerReportFile, out_path: Optional[str] = None):
        """
        Download a file created by icobrain for a customer_report

        :param customer_report_file: The file entity you want to download
        :param out_path: A path to write the file to
        :return:
        """
        if not out_path:
            out_path = customer_report_file.name
        logger.info(f"Downloading {out_path}")
        self._api.stream_file(customer_report_file.uri, out_path)

    def wait_for_customer_report_for_study(self, project_id: str,
                                           study_instance_uid: str,
                                           report_type: str) -> CustomerReportEntity:
        """
        After data has been imported a customer report will be created

        :param project_id: The ID of the project you want to search under
        :param study_instance_uid: The study instance UID from the DICOM
        :param report_type: The requested report type
        :return:
        """
        max_wait = 20  # sec (approx...)
        max_count = round(max_wait / self.polling_interval)
        count = 0
        while True:
            count += 1
            logger.info(f"Searching {report_type} report for {study_instance_uid} in {project_id}")
            params = {"study_instance_uid": study_instance_uid}
            for page in get_paginator(self.get_all, project_id=project_id, params=params):
                for report in page:
                    if report.icobrain_report_type == report_type:
                        return report
            if count >= max_count:
                raise IcometrixDataImportException(f"Failed to find a CustomerReport for {study_instance_uid}")
            sleep(self.polling_interval)

    def wait_for_results(self, customer_report_uris: List[str]) -> List[CustomerReportEntity]:
        """
        Wait until processing has finished and the result files are available on the customer report

        :param customer_report_uris: A list of customer uris
        :return:
        """

        finished_customer_reports: Dict[str, CustomerReportEntity] = {}
        while len(finished_customer_reports) != len(customer_report_uris):
            for customer_report_uri in customer_report_uris:
                if customer_report_uri in finished_customer_reports:
                    continue

                report = self.get_one(customer_report_uri)
                if report.status != "Finished":
                    print(f"Waiting for {report.study_instance_uid} to complete: {report.status}")
                    continue

                print(f"Finished {report.study_instance_uid}")
                finished_customer_reports[report.uri] = report
            sleep(self.polling_interval)
        return [value for value in finished_customer_reports.values()]

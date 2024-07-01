"""A library that provides a Python interface to the Icometrix API"""
import os
from typing import Optional

from icometrix_sdk.authentication import PasswordAuthentication, AuthenticationMethod, get_auth_method
from icometrix_sdk.exceptions import IcometrixConfigException
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.upload_entity import StartUploadDto
from icometrix_sdk.resources.customer_reports import CustomerReports
from icometrix_sdk.resources.customer_results import CustomerResults
from icometrix_sdk.resources.patients import Patients
from icometrix_sdk.resources.pipeline_results import PipelineResults
from icometrix_sdk.resources.profile import Profile
from icometrix_sdk.resources.projects import Projects
from icometrix_sdk.resources.series import Series
from icometrix_sdk.resources.studies import Studies
from icometrix_sdk.resources.uploads import Uploads
from icometrix_sdk.utils.api_client import ApiClient
from icometrix_sdk.utils.regions import Region
from icometrix_sdk.utils.requests_api_client import RequestsApiClient


def get_api_client() -> RequestsApiClient:
    """
    Create an RequestsApiClient with the 'API_HOST' environment variable as server
    """

    region = os.getenv("REGION")
    if region in Region:
        api_host = Region[region].value
    else:
        api_host = os.getenv("API_HOST")

    if not api_host:
        raise IcometrixConfigException("Please set the 'API_HOST' environment variable")

    auth_method = get_auth_method()
    return RequestsApiClient(api_host, auth_method)


class IcometrixApi:
    """
    A Python interface for the icometrix API.

    :param api_client:
        An instance of an ApiClient
    """

    profile: Profile
    projects: Projects
    patients: Patients
    studies: Studies
    series: Series
    uploads: Uploads
    customer_results: CustomerResults
    customer_reports: CustomerReports

    _api_client: ApiClient

    def __init__(self, api_client: Optional[ApiClient] = None):
        self._api_client = api_client
        if not self._api_client:
            self._api_client = get_api_client()

        self.profile = Profile(self._api_client)
        self.projects = Projects(self._api_client)
        self.patients = Patients(self._api_client)
        self.studies = Studies(self._api_client)
        self.series = Series(self._api_client)
        self.uploads = Uploads(self._api_client)
        self.pipeline_results = PipelineResults(self._api_client)
        self.customer_results = CustomerResults(self._api_client)
        self.customer_reports = CustomerReports(self._api_client)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass
        # todo force logout
        # if self._api_client.auth:
        #     self._api_client.auth.disconnect(self._api_client)

    #         """
    #         Download a file created by icobrain for a customer_report
    #
    #         :param customer_report_file: The file entity you want to download
    #         :param out_path: A path to write the file to
    #         :return:
    #         """

    def process_dicom_directory(self, project_id: str, input_dir: str, out_dir: str, params: StartUploadDto):
        """
        The process_dicom_directory function provides a high-level interface for handling the complete workflow of
        processing DICOM files and downloading the results.

        :param project_id (str): The UUID of the project to which the DICOM files belong.
        :param input_dir (str): The path to the directory containing the DICOM files to be processed.
        :param out_dir (str): The path to the directory where output data will be stored.
        :param params (StartUploadDto): An instance of StartUploadDto containing parameters for the upload.
        :return:
        """
        # Get the project, to make sure its there (will throw a 404 in case the project is not found)
        project = self.projects.get_one_by_id(project_id)

        # Upload a directory of DICOMs
        upload = self.uploads.upload_dicom_dir(project.id, input_dir, params)

        # Wait for data to be imported
        upload = self.uploads.wait_for_data_import(upload.folder_uri)

        # e.g. No DICOMs found in the upload
        if upload.errors:
            raise Exception(f"Upload failed: {', '.join(upload.errors)}")

        # Get imported studies
        studies_in_upload = self.uploads.get_studies_for_upload(upload_folder_uri=upload.folder_uri)
        if not studies_in_upload:
            raise Exception("No valid studies uploaded.")

        for study_in_upload in studies_in_upload:

            # Find the study
            study = self.studies.get_one(study_in_upload.project_id,
                                         study_in_upload.patient_id,
                                         study_in_upload.study_id)

            # Get reports for this study
            customer_reports = self.customer_reports.get_all_for_study(study_uri=study.uri)

            # Wait for the reports to finish and download the results
            finished_customer_reports = self.customer_reports.wait_for_results(list(customer_reports))
            for customer_report in finished_customer_reports:
                out_path = os.path.join(out_dir, customer_report.id)
                self.customer_reports.download_customer_report_files(customer_report, out_path)

"""A library that provides a Python interface to the Icometrix API"""
import os
from typing import Optional

from icometrix_sdk.authentication import PasswordAuthentication, AuthenticationMethod, get_auth_method
from icometrix_sdk.exceptions import IcometrixConfigException
from icometrix_sdk.resources.customer_reports import CustomerReports
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.resources.patients import Patients
from icometrix_sdk.resources.profile import Profile
from icometrix_sdk.resources.projects import Projects
from icometrix_sdk.resources.uploads import Uploads
from icometrix_sdk.utils.requests_api_client import RequestsApiClient
from icometrix_sdk.utils.api_client import ApiClient


def get_api_client() -> RequestsApiClient:
    """
    Create an RequestsApiClient with the 'API_HOST' environment variable as server
    """
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
    uploads: Uploads
    customer_reports: CustomerReports

    _api_client: ApiClient

    def __init__(self, api_client: Optional[ApiClient] = None):
        self._api_client = api_client
        if not self._api_client:
            self._api_client = get_api_client()

        self.profile = Profile(self._api_client)
        self.projects = Projects(self._api_client)
        self.patients = Patients(self._api_client)
        self.uploads = Uploads(self._api_client)
        self.customer_reports = CustomerReports(self._api_client)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

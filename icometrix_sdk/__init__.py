"""A library that provides a Python interface to the Icometrix API"""
from typing import Optional

from icometrix_sdk.authentication import PasswordAuthentication, AuthenticationMethod, get_auth_method
from icometrix_sdk.resources.customer_reports import CustomerReports
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.resources.patients import Patients
from icometrix_sdk.resources.profile import Profile
from icometrix_sdk.resources.projects import Projects
from icometrix_sdk.resources.uploads import Uploads
from icometrix_sdk.utils.api_client import ApiClient


class IcometrixApi:
    """
    A Python interface for the icometrix API.

    :param server:
        An icometrix server endpoint (icobrain-eu.icometrix.com, icobrain-us.icometrix.com...)
    :param auth:
        An authentication method
    """

    profile: Profile
    projects: Projects
    patients: Patients
    uploads: Uploads
    customer_reports: CustomerReports

    _auth: Optional[AuthenticationMethod]

    def __init__(self, server: str, auth: Optional[AuthenticationMethod] = None):
        self.server = server

        self._auth = auth
        if not self._auth:
            self._auth = get_auth_method()

        self._api_client = ApiClient(self.server)
        self.authenticate()

        self.profile = Profile(self._api_client)
        self.projects = Projects(self._api_client)
        self.patients = Patients(self._api_client)
        self.uploads = Uploads(self._api_client)
        self.customer_reports = CustomerReports(self._api_client)

    def __enter__(self):
        self.authenticate()
        return self

    def __exit__(self, *args, **kwargs):
        if self._auth:
            self._auth.disconnect(self._api_client)

    def authenticate(self):
        if self._auth:
            self._auth.connect(self._api_client)

from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.patient_entity import PatientEntity
from icometrix_sdk.utils.api_client import ApiClient


class Patients:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all(self, project_uri: str, **kwargs) -> PaginatedResponse[PatientEntity]:
        """
        List all patients within a project

        :param: The uri of the project
        :return: A Paginated response containing patients
        """
        page = self._api.get(f"{project_uri}/patients", **kwargs)
        return PaginatedResponse[PatientEntity](**page)

    def get_one(self, patient_uri: str) -> PatientEntity:
        """
        Get a single patient based on the patient uri

        :param patient_uri: the uri of the patient
        :return: A single patient or 404
        """
        resp = self._api.get(patient_uri)
        return PatientEntity(**resp)

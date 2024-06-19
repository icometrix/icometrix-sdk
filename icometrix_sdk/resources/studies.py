import logging

from icometrix_sdk.logger import logger_name
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.study_entity import StudyEntity
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(logger_name)


class Studies:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_one(self, project_id: str, patient_id: str, study_id: str) -> StudyEntity:
        """
        Get a single upload entry based on the upload uri

        :param project_id: the ID of the project
        :param patient_id: the ID of the patient
        :param study_id: the ID of the study
        :return: A single study or 404
        """
        resp = self._api.get(f"/storage-service/api/v1/projects/{project_id}/patients/{patient_id}/studies/{study_id}")
        return StudyEntity(**resp)

    def get_all_for_patient(self, patient_uri: str, **kwargs) -> PaginatedResponse[StudyEntity]:
        """
        List all studies for a patient

        :param: The uri of the patient
        :return: A Paginated response containing studies
        """
        page = self._api.get(f"{patient_uri}/patients", **kwargs)
        return PaginatedResponse[StudyEntity](**page)

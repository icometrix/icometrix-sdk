from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.project_entity import ProjectEntity
from icometrix_sdk.utils.api_client import ApiClient


class Projects:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all(self, **kwargs) -> PaginatedResponse[ProjectEntity]:
        """
        List projects that the current user has access to

        :return: A Paginated response containing projects
        """
        page = self._api.get("/storage-service/api/v2/projects", **kwargs)
        return PaginatedResponse[ProjectEntity](**page)

    def get_one(self, project_uri: str) -> ProjectEntity:
        """
        Get a single project based on the project uri

        :param project_uri: the uri of the project
        :return: A single project or 404
        """
        resp = self._api.get(project_uri)
        return ProjectEntity(**resp)

    def get_one_by_id(self, project_id: str) -> ProjectEntity:
        """
        Get a single project based on the project ID

        :param project_id: the ID of the project
        :return: A single project or 404
        """
        resp = self._api.get(f"/storage-service/api/v1/projects/{project_id}")
        return ProjectEntity(**resp)

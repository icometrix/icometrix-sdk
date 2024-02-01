from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.project_entity import ProjectEntity
from icometrix_sdk.models.user_entity import User
from icometrix_sdk.utils.api_client import ApiClient


class Profile:
    def __init__(self, api: ApiClient):
        self._api = api

    def who_am_i(self) -> User:
        """
        see the currently logged-in user

        :return: The current User or 401
        """
        resp = self._api.get(f"/authentication-service/api/v1/loginstatus")
        return User(**resp)

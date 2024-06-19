import logging

from icometrix_sdk.logger import logger_name
from icometrix_sdk.models.base import PaginatedResponse
from icometrix_sdk.models.series_entity import SeriesEntity
from icometrix_sdk.utils.requests_api_client import ApiClient

logger = logging.getLogger(logger_name)


class Series:
    def __init__(self, api: ApiClient):
        self._api = api

    def get_all_for_study(self, study_uri: str, **kwargs) -> PaginatedResponse[SeriesEntity]:
        """
        List all series for a study

        :param study_uri: the uri of the study
        :return: A Paginated response containing series
        """
        page = self._api.get(f"{study_uri}/series", **kwargs)
        return PaginatedResponse[SeriesEntity](**page)

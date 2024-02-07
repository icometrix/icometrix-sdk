import json
import logging
import os
import threading
import uuid
from functools import lru_cache
from typing import Optional, Type, Dict
from urllib.parse import urljoin

import requests
from requests import Response, HTTPError, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from icometrix_sdk._version import __version__
from icometrix_sdk.authentication import AuthenticationMethod
from icometrix_sdk.exceptions import IcometrixHttpException, IcometrixParseException, IcometrixConfigException, \
    IcometrixAuthException
from icometrix_sdk.utils.api_client import ApiClient
from icometrix_sdk.utils.file_upload import create_multipart

HTTP_TIMEOUT = os.getenv("HTTP_TIMEOUT", 120)

logger = logging.getLogger(__name__)


class RequestsApiClient(ApiClient):
    """
    An implementation of the API client using the requests library

    Dev Note: Try not the expose requests logic, we might want to swap this later on
    """

    _auth_attempts = 0

    _session: Session
    _auth: Optional[AuthenticationMethod]

    def __init__(self, server: str, auth: Optional[AuthenticationMethod] = None):
        self.base_headers = {
            "User-Agent": "Python SDK v{}".format(__version__),
            "x-sdk-type": "Python",
            "x-sdk-version": __version__,
            "x-sdk-contextId": str(uuid.uuid4()),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.server = server
        self._auth = auth

        if not server:
            raise IcometrixConfigException("Server is required")

        self._session = self._create_session()
        self._authenticate()

    def _authenticate(self):
        if self._auth:
            logger.info("Authenticating")
            self._auth_attempts += 1
            self._auth.connect(self)
            self._auth_attempts = 0

    def refresh_token(self, resp: Response):
        if self._auth_attempts > 0:
            raise IcometrixAuthException("Failed to authenticate")
        if resp.status_code == 401:
            logger.info("Fetching new token as the previous token expired")
            self._authenticate()

    def _create_session(self) -> Session:
        """
        Create a new session
        """
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 502, 503, 504],
        )
        session.mount('https://', HTTPAdapter(max_retries=retries))
        session.headers.update(self.base_headers)
        return session

    def _make_request(self,
                      method=Type[str],
                      url=Type[str],
                      data: Optional[any] = None,
                      headers: Optional[dict] = None,
                      params: Optional[dict] = None,
                      files=None,
                      cookies=None) -> Response:
        """
        private function to abstract most of the HTTP request logic

        :param method: GET, POST, PUT, PATCH, DELETE...
        :param url: A relative URL to specify the API endpoint
        :param data: Dict containing data for the request body
        :param headers: Dict containing additional request headers.
        :param params: Dict containing query parameters.
        :param files: (optional) Dict of ``'filename': file-like-objects`` for multipart encoding upload.
        :param cookies: (optional) Dict or CookieJar object to send with the
        :return:
        """

        full_url = urljoin(self.server, url)
        try:
            response = self._session.request(
                method=method,
                url=full_url,
                data=data,
                headers=headers,
                params=params,
                files=files,
                timeout=HTTP_TIMEOUT,
                cookies=cookies
            )
            response.raise_for_status()
        except HTTPError as e:
            message = "Exception received when sending an HTTP request"
            logger.exception(message)
            raise IcometrixHttpException(e)

        return response

    def get(self, uri: str, params: Optional[dict] = None, **kwargs) -> dict:
        """
        Submit a GET request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param params: A dictionary containing query parameters.
        :returns: The API response as a dictionary.
        """

        resp = self._make_request(
            method="GET",
            url=uri,
            params=params,
            **kwargs
        )
        return response_to_dict(resp)

    def post(self, uri: str, data: dict, headers: Optional[dict] = None, **kwargs) -> dict:
        """
        Submit a POST request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param data: A dictionary containing data for the request body
        :param headers: A dictionary containing additional request headers.
        :returns: The API response as a dictionary.

        """

        resp = self._make_request(
            method="POST",
            url=uri,
            data=json.dumps(data),
            headers=headers,
            **kwargs
        )
        return response_to_dict(resp)

    def put(self, uri: str, data: dict, **kwargs) -> dict:
        """
        Submit a PUT request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param data: A dictionary containing data for the request body
        :returns: The API response as a dictionary.

        """

        resp = self._make_request(
            method="PUT",
            url=uri,
            data=json.dumps(data),
            **kwargs
        )
        return response_to_dict(resp)

    def delete(self, uri: str, **kwargs):
        """
        Submit a DELETE request to the API.

        :param uri: A relative URL to specify the API endpoint
        :returns: void

        """
        self._make_request(
            method="DELETE",
            url=uri,
            **kwargs
        )

    def put_file(self, uri: str, fields, **kwargs):
        """
        Submit a PUT request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param fields: Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        :returns:

        """

        data, headers = create_multipart(fields)
        self._make_request(
            method="PUT",
            url=uri,
            data=data,
            headers=headers,
            **kwargs
        )


def response_to_dict(response: Response) -> dict:
    content = response.content
    try:
        return json.loads(content)
    except ValueError as e:
        raise IcometrixParseException("Failed to parse response to json: {}".format(e.args[0]))

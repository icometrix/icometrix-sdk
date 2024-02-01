import json
import os
from typing import Optional, Type
import requests
import uuid
from requests import Session, Response, HTTPError
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from icometrix_sdk._version import __version__
from icometrix_sdk.exceptions import IcometrixAPIException
from icometrix_sdk.utils.file_upload import create_multipart

HTTP_TIMEOUT = os.getenv("HTTP_TIMEOUT", 120)


class ApiClient:
    """
    The API client is used to make calls to the icometrix API
    """

    def __init__(self, server: str, session: Optional[Session] = None):
        self.base_headers = {
            "User-Agent": "Python SDK v{}".format(__version__),
            "x-sdk-type": "Python",
            "x-sdk-version": __version__,
            "x-sdk-contextId": str(uuid.uuid4()),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.server = server
        self.session = session
        if not session:
            default_session = requests.Session()
            self.session = default_session
            retries = Retry(
                total=3,
                backoff_factor=0.5,
                status_forcelist=[502, 503, 504],
            )
            self.session.mount('https://', HTTPAdapter(max_retries=retries))

        self.session.headers.update(self.base_headers)

    def _make_request(self,
                      method=Type[str],
                      url=Type[str],
                      data: Optional[any] = None,
                      headers: Optional[dict] = None,
                      params: Optional[dict] = None,
                      files=None) -> Response:
        """
        private function to abstract most of the HTTP request logic

        :param method: GET, POST, PUT, PATCH, DELETE...
        :param url: A relative URL to specify the API endpoint
        :param data: A dictionary containing data for the request body
        :param headers: A dictionary containing additional request headers.
        :param params: A dictionary containing query parameters.
        :param files: (optional) Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :return:
        """

        full_url = urljoin(self.server, url)
        try:
            response = self.session.request(
                method=method,
                url=full_url,
                data=data,
                headers=headers,
                params=params,
                files=files,
                timeout=HTTP_TIMEOUT
            )
            response.raise_for_status()
        except HTTPError as e:
            raise IcometrixAPIException(e)

        return response

    def get(self, uri: str, params: Optional[dict] = None) -> dict:
        """
        Submit a GET request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param params: A dictionary containing query parameters.
        :returns: The API response as a dictionary.
        """

        resp = self._make_request(
            method="GET",
            url=uri,
            params=params
        )
        return response_to_dict(resp)

    def post(self, uri: str, data: dict, headers: Optional[dict] = None) -> dict:
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
            headers=headers
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

    def put_file(self, uri: str, fields, **kwargs) -> Response:
        """
        Submit a PUT request to the API.

        :param uri: A relative URL to specify the API endpoint
        :param fields: Dictionary of fields or list of (key, :class:`~urllib3.fields.RequestField`).
        :returns: request.Response.

        """

        data, headers = create_multipart(fields)

        return self._make_request(
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
        raise IcometrixAPIException("Failed to parse response to json: {}".format(e.args[0]))

import os
from abc import ABC, abstractmethod
from typing import Optional

from icometrix_sdk.exceptions import IcometrixConfigException
from icometrix_sdk.utils.api_client import ApiClient

TOKEN_URI = "/authentication-service/api/v1/token-sessions"
SESSION_URI = "/authentication-service/api/v1/sessions"


class AuthenticationMethod(ABC):
    """
    Interface for authentication methods
    """

    @abstractmethod
    def connect(self, api: ApiClient):
        pass

    @abstractmethod
    def disconnect(self, api: ApiClient):
        pass


class PasswordAuthentication(AuthenticationMethod):
    """
    Email/Password authentication method
    """

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def connect(self, api: ApiClient):
        data = {"email": self.email, "password": self.password}
        api.post(SESSION_URI, data=data)

    def disconnect(self, api: ApiClient):
        if api:
            api.delete(SESSION_URI)


class TokenAuthentication(AuthenticationMethod):
    """
    Token authentication method
    """

    def __init__(self, token: str):
        self.token = token

    def connect(self, api: ApiClient):
        data = {"key": self.token}
        api.post(TOKEN_URI, data=data)

    def disconnect(self, api: ApiClient):
        if api:
            api.delete(SESSION_URI)


def get_auth_method() -> Optional[AuthenticationMethod]:
    """
    Find an authentication method based on the 'AUTH_METHOD' environment variable
    """
    auth_method = os.getenv("AUTH_METHOD")
    if auth_method is None:
        if os.getenv("TOKEN"):
            auth_method = "token"
        elif os.getenv("EMAIL") and os.getenv("PASSWORD"):
            auth_method = "basic"

    if auth_method == "basic":
        return PasswordAuthentication(os.environ["EMAIL"], os.environ["PASSWORD"])
    elif auth_method == "token":
        return TokenAuthentication(os.environ["TOKEN"])

    raise IcometrixConfigException("Please set an 'AUTH_METHOD' (basic OR token)")

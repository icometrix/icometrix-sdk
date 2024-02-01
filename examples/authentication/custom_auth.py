"""
An example on how to implement custom authentication logic
"""

from icometrix_sdk import IcometrixApi, AuthenticationMethod
from icometrix_sdk.utils.api_client import ApiClient

SERVER = "https://icobrain-test.icometrix.com"


class FileAuth(AuthenticationMethod):
    def __init__(self, secret_password_file_path: str):
        self.secret_password_file_path = secret_password_file_path

    def connect(self, api: ApiClient):
        with open(self.secret_password_file_path) as secret:
            email = secret.readlines()[0],
            password = secret.readlines()[1]
            data = {"email": email, "password": password}
        api.post("/authentication-service/api/v1/sessions", data=data)

    def disconnect(self, api: ApiClient):
        pass


auth = FileAuth("/mount/secret.txt")
ico_api = IcometrixApi(SERVER, auth)

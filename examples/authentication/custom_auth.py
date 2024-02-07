"""
An example on how to implement custom authentication logic
"""

from icometrix_sdk import IcometrixApi, AuthenticationMethod
from icometrix_sdk.utils.requests_api_client import RequestsApiClient

SERVER = "https://icobrain-test.icometrix.com"


class FileAuth(AuthenticationMethod):
    def __init__(self, secret_password_file_path: str):
        self.secret_password_file_path = secret_password_file_path

    def connect(self, api: RequestsApiClient):
        with open(self.secret_password_file_path) as secret:
            email = secret.readlines()[0],
            password = secret.readlines()[1]
            data = {"email": email, "password": password}
        api.post("/authentication-service/api/v1/sessions", data=data)

    def disconnect(self, api: RequestsApiClient):
        pass


if __name__ == '__main__':
    auth = FileAuth("/mount/secret.txt")
    client = RequestsApiClient(SERVER, auth)
    ico_api = IcometrixApi(client)

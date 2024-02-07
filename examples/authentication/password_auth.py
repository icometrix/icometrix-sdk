"""
An example on how to authenticate using an email address and password
"""

import os

from icometrix_sdk import IcometrixApi, PasswordAuthentication
from icometrix_sdk.utils.requests_api_client import RequestsApiClient

if __name__ == '__main__':
    SERVER = "https://icobrain-test.icometrix.com"

    auth = PasswordAuthentication("example@company.com", os.environ["PASSWORD"])
    client = RequestsApiClient(SERVER, auth)

    ico_api = IcometrixApi(client)

    me = ico_api.profile.who_am_i()

    print(me.email)

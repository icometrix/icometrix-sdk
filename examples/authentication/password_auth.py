"""
An example on how to authenticate using an email address and password
"""

import os

from icometrix_sdk import IcometrixApi, PasswordAuthentication
from icometrix_sdk.utils.api_client import ApiClient

SERVER = "https://icobrain-test.icometrix.com"
client = ApiClient(SERVER)

auth = PasswordAuthentication(os.environ["EMAIL"], os.environ["PASSWORD"])
ico_api = IcometrixApi(client, auth)
ico_api.authenticate()

resp = ico_api.profile.who_am_i()

print(resp.email)

"""
An example on how to do authentication based on an 'AUTH_METHOD' set as environment variable
"""

from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.api_client import ApiClient

SERVER = "https://icobrain-test.icometrix.com"
client = ApiClient(SERVER)

ico_api = IcometrixApi(client)
ico_api.authenticate()

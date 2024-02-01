"""
An example on how to authenticate using an email address and password
"""

import os

from icometrix_sdk import IcometrixApi, PasswordAuthentication

SERVER = "https://icobrain-test.icometrix.com"

auth = PasswordAuthentication("jeroen.pinxten@icometrix.comd", os.environ["PASSWORD"])
ico_api = IcometrixApi(SERVER, auth)
resp = ico_api.profile.who_am_i()

print(resp.email)

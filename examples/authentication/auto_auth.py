"""
An example on how to do authentication based on an 'AUTH_METHOD' set as environment variable
"""
import os

from icometrix_sdk import IcometrixApi

if __name__ == '__main__':
    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    ico_api = IcometrixApi()

    print(ico_api.profile.who_am_i().email)

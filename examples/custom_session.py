import requests

from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.api_client import ApiClient
from icometrix_sdk.utils.paginator import get_paginator


def print_url(r, *args, **kwargs):
    print(r.url)


s = requests.Session()
s.hooks["response"].append(print_url)

SERVER = "https://icobrain-test.icometrix.com"
client = ApiClient(SERVER, session=s)

with IcometrixApi(client) as ico_api:
    for projects in get_paginator(ico_api.projects.get_all):
        pass

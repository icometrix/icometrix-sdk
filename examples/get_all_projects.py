from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.api_client import ApiClient
from icometrix_sdk.utils.paginator import get_paginator

SERVER = "https://icobrain-test.icometrix.com"
client = ApiClient(SERVER)

with IcometrixApi(client) as ico_api:
    for projects in get_paginator(ico_api.projects.get_all):
        for project in projects:
            print(project.name)

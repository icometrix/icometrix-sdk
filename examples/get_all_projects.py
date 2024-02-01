from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.paginator import get_paginator

SERVER = "https://icobrain-test.icometrix.com"

with IcometrixApi(SERVER) as ico_api:

    for projects in get_paginator(ico_api.projects.get_all):
        for project in projects:
            print(project.name)

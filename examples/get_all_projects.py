import logging
import os

from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.paginator import get_paginator

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    with IcometrixApi() as ico_api:
        for projects in get_paginator(ico_api.projects.get_all):
            for project in projects:
                print(project.name)

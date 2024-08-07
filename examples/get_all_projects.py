import logging
import os

from icometrix_sdk import IcometrixApi, Region
from icometrix_sdk.utils.paginator import get_paginator

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    os.environ["API_HOST"] = Region.EU.value

    ico_api = IcometrixApi()

    for projects in get_paginator(ico_api.projects.get_all, page_size=5):
        for project in projects:
            print(project.name)

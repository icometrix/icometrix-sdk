import logging

from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.paginator import get_paginator

logging.basicConfig(level=logging.INFO)

STUDY_URI = "/storage-service/api/v1/projects/20c9e829-bc24-42bb-ac02-6527db61f4c5/patients/7d1cfc1e-a272-4c18-b24f-6f1a4393254a/studies/5fa896f5-37cd-48a7-9f2e-116453325bb2"

if __name__ == '__main__':
    ico_api = IcometrixApi()

    for cr_results in get_paginator(ico_api.customer_results.get_all_for_study, study_uri=STUDY_URI):
        for cr_result in cr_results:
            print(cr_result.uri)

import os

from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.paginator import get_paginator

PROJECT_ID = "uuid"
DICOM_DIR_PATH = "<path>"

if __name__ == '__main__':
    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    customer_reports = ico_api.customer_reports.get_all(PROJECT_ID)

    for reports in get_paginator(ico_api.customer_reports.get_all, project_id=PROJECT_ID):
        for report in reports:
            if report.status == "Finished":
                print(report.study_instance_uid, report.report_status)

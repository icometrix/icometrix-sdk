from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.paginator import get_paginator

PROJECT_ID = "20c9e829-bc24-42bb-ac02-6527db61f4c5"
SERVER = "https://icobrain-test.icometrix.com"
DICOM_DIR_PATH = "/Users/jpinxten/Downloads/LD_20111222"

# Initialize the icometrix API
ico_api = IcometrixApi(SERVER)

customer_reports = ico_api.customer_reports.get_all(PROJECT_ID)

for reports in get_paginator(ico_api.customer_reports.get_all, project_id=PROJECT_ID):
    for report in reports:
        if report.status == "Finished":
            print(report.study_instance_uid, report.report_status)

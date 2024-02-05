from icometrix_sdk import IcometrixApi
from icometrix_sdk.utils.api_client import ApiClient
from icometrix_sdk.utils.paginator import get_paginator

PROJECT_ID = "uuid"
DICOM_DIR_PATH = "<path>"

SERVER = "https://icobrain-test.icometrix.com"
client = ApiClient(SERVER)

# Initialize the icometrix API
ico_api = IcometrixApi(client)

customer_reports = ico_api.customer_reports.get_all(PROJECT_ID)

for reports in get_paginator(ico_api.customer_reports.get_all, project_id=PROJECT_ID):
    for report in reports:
        if report.status == "Finished":
            print(report.study_instance_uid, report.report_status)

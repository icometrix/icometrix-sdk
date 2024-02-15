import logging
import os
from pathlib import Path
from typing import List

import pydicom
from pydicom.errors import InvalidDicomError

from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "<uuid>"
REPORT_TYPE = "icobrain_ms"

# A directory containing a T1 and FLAIR scan, as required for icobrain_ms for more info see HCP manual
DICOM_DIR_PATH = "<path>"

logging.basicConfig(level=logging.INFO)


def extract_unique_studies(folder_path: str) -> List[str]:
    """
    Extract all study_instance_uids from DICOMS in a (sub)folder(s)

    :param folder_path: The root path to start searching
    :return:
    """
    study_uids: List[str] = []
    for path, _, files in os.walk(folder_path):
        for name in files:

            file_path = os.path.join(path, name)
            try:
                ds = pydicom.dcmread(file_path)
            except InvalidDicomError:
                continue

            if ds.StudyInstanceUID in study_uids:
                continue
            study_uids.append(ds.StudyInstanceUID)
    return study_uids


if __name__ == '__main__':
    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    # Get the project, to make sure its there (will throw a 404 in case the project is not found)
    project = ico_api.projects.get_one_by_id(PROJECT_ID)

    # Get the study instance UIDs we will need them to poll for the results
    study_instance_uids = extract_unique_studies(DICOM_DIR_PATH)

    # Upload a directory of DICOMs
    data = StartUploadDto(icobrain_report_type=REPORT_TYPE)
    upload = ico_api.uploads.upload_dicom_dir(PROJECT_ID, DICOM_DIR_PATH, data)

    # Wait for data to be imported
    upload = ico_api.uploads.wait_for_data_import(upload.folder_uri)

    # Find reports for studies
    customer_reports = []
    for study_instance_uid in study_instance_uids:
        csr = ico_api.customer_reports.wait_for_customer_report_for_study(PROJECT_ID, study_instance_uid, REPORT_TYPE)
        customer_reports.append(csr)

    # Wait for the reports to finish
    customer_report_uris = [customer_report.uri for customer_report in customer_reports]
    customer_reports = ico_api.customer_reports.wait_for_results(customer_report_uris)

    # Download icobrain report files
    for customer_report in customer_reports:
        out_path = f"out/{customer_report.study_instance_uid}"
        Path(out_path).mkdir(parents=True, exist_ok=True)
        ico_api.customer_reports.download_customer_report_files(customer_report, out_path)

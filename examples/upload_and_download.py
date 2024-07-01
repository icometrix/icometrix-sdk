import logging
import os
from icometrix_sdk import IcometrixApi, Region
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "uuid"
REPORT_TYPE = "icobrain_ms"

# A directory containing a T1 and FLAIR scan, as required for icobrain_ms for more info see HCP manual
DICOM_DIR_PATH = "<dir_path>"

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    os.environ["API_HOST"] = Region.EU.value

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    # Get the project, to make sure its there (will throw a 404 in case the project is not found)
    project = ico_api.projects.get_one_by_id(PROJECT_ID)

    # Upload a directory of DICOMs
    data = StartUploadDto(icobrain_report_type=REPORT_TYPE)
    upload = ico_api.uploads.upload_dicom_dir(PROJECT_ID, DICOM_DIR_PATH, data)

    # Wait for data to be imported
    upload = ico_api.uploads.wait_for_data_import(upload.folder_uri)

    # e.g. No DICOMs found in the upload
    if upload.errors:
        raise Exception(f"Upload failed: {', '.join(upload.errors)}")

    # Get imported studies
    studies_in_upload = ico_api.uploads.get_studies_for_upload(upload_folder_uri=upload.folder_uri)
    if not studies_in_upload:
        raise Exception("No valid studies uploaded.")

    # For the demo we just use a single study
    study_in_upload = studies_in_upload[0]
    study = ico_api.studies.get_one(study_in_upload.project_id, study_in_upload.patient_id, study_in_upload.study_id)

    # Get reports for this study
    customer_reports = ico_api.customer_reports.get_all_for_study(study_uri=study.uri)

    # Wait for the reports to finish and download the results
    finished_customer_reports = ico_api.customer_reports.wait_for_results(list(customer_reports))
    for customer_report in finished_customer_reports:
        ico_api.customer_reports.download_customer_report_files(customer_report, f"./{customer_report.id}")

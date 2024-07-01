import logging
import os

from icometrix_sdk import IcometrixApi, Region
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "pid"

# A directory containing a T1 and FLAIR scan, as required for icobrain_ms for more info see HCP manual
DICOM_DIR_PATH = "..."

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    os.environ["API_HOST"] = Region.EU.value

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    # Get the project, to make sure its there (will throw a 404 in case the project is not found)
    project = ico_api.projects.get_one_by_id(PROJECT_ID)

    # Upload a directory of DICOMs
    data = StartUploadDto(icobrain_report_type="icobrain_ms")
    upload = ico_api.uploads.upload_dicom_dir(PROJECT_ID, DICOM_DIR_PATH, data)

    # Wait for data to be imported
    upload = ico_api.uploads.wait_for_data_import(upload.folder_uri)

    # Get imported studies
    studies_in_upload = ico_api.uploads.get_studies_for_upload(upload_folder_uri=upload.folder_uri)

    for uploaded_study in studies_in_upload:
        study = ico_api.studies.get_one(uploaded_study.project_id, uploaded_study.patient_id, uploaded_study.study_id)

        # Add some validation logic for each study e.g. find series
        series = ico_api.series.get_all_for_study(study.uri)
        # ...

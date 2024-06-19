import os

from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "uuid"
DICOM_DIR_PATH = "<dir_path>"

if __name__ == '__main__':
    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    # Get the project, to make sure its there (will throw a 404 in case the project is not found)
    project = ico_api.projects.get_one_by_id(PROJECT_ID)

    # Upload a directory of DICOMs
    data = StartUploadDto(icobrain_report_type="icobrain_ms")
    upload = ico_api.uploads.start_upload(PROJECT_ID, data)
    ico_api.uploads.upload_dicom_dir(upload.uri, DICOM_DIR_PATH)

    # Wait for data to be imported
    upload = ico_api.uploads.wait_for_data_import(upload.folder_uri)

    # Get imported studies
    for uploaded_study in ico_api.uploads.get_studies_for_upload(upload_folder_uri=upload.folder_uri):
        print(uploaded_study.study_id)

import os

from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "uuid"
DICOM_DIR_PATH = "<dir_path>"

if __name__ == '__main__':
    os.environ["API_HOST"] = "https://icobrain-{region}.icometrix.com"

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    # Get the project, to make sure its there (will throw a 404 in case the project is not found)
    project = ico_api.projects.get_one_by_id(PROJECT_ID)

    # Start an upload
    data = StartUploadDto(icobrain_report_type="icobrain_ms")
    upload = ico_api.uploads.start_upload(PROJECT_ID, data)

    # Will walk through all files/subdirectories and upload all files
    ico_api.uploads.upload_all_files_in_dir(upload.uri, DICOM_DIR_PATH)

    # Once all files have been uploaded, signal that they are all there and start the import/processing
    upload = ico_api.uploads.complete_upload(upload.uri)
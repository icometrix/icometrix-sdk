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
    upload = ico_api.uploads.start_upload(PROJECT_ID, data)
    count = ico_api.uploads.upload_all_files_in_dir(upload.uri, DICOM_DIR_PATH)

    # add validation logic here
    file_uploads = ico_api.uploads.get_uploaded_files(upload.folder_uri)
    if len(file_uploads.files) != count:
        raise Exception("Not all files uploaded")

    # Once all files have been uploaded, signal that they are all there and start the import/processing
    upload = ico_api.uploads.complete_upload(upload.uri)

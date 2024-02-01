import os

from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "5461177d-c34b-467e-8610-9ba71cbb3eb4"
SERVER = "https://icobrain-test.icometrix.com"
DICOM_DIR_PATH = "/Users/jpinxten/Downloads/LD_20111222"

# Initialize the icometrix API
ico_api = IcometrixApi(SERVER)

# Get the project, to make sure its there (will throw a 404 in case the project is not found)
project = ico_api.projects.get_one_by_id(PROJECT_ID)

# Upload a directory of DICOMs
data = StartUploadDto(icobrain_report_type="icobrain_ms")
upload = ico_api.uploads.start_upload(PROJECT_ID, data)

# Loop over all files in a DIR and upload them to the before created upload entry
for path, subdirs, files in os.walk(DICOM_DIR_PATH):
    for name in files:
        if name.startswith("."):
            continue
        ico_api.uploads.upload_dicom_path(upload.uri, os.path.join(path, name))

file_list = ico_api.uploads.get_uploaded_files(upload.folder_uri)




from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "5461177d-c34b-467e-8610-9ba71cbb3eb4"
SERVER = "https://icobrain-test.icometrix.com"
DICOM_PATHS = [
    "/Users/jpinxten/Downloads/LD_20111222/Long_Demo/Ld_20111222 - 377700362/HEAD_SET_201/IM-0001-0001.dcm"
    "/Users/jpinxten/Downloads/LD_20111222/Long_Demo/Ld_20111222 - 377700362/HEAD_SET_201/IM-0001-0002.dcm"
]

# Initialize the icometrix API
ico_api = IcometrixApi(SERVER)

# Get the project, to make sure its there (will throw a 404 in case the project is not found)
project = ico_api.projects.get_one_by_id(PROJECT_ID)

# prepare an upload entry, this entry can be used to push a block of files to (which is typical in DICOM)
# Some options can be passed, for all available options please have a look at the StartUploadDto
data = StartUploadDto(icobrain_report_type="icobrain_ms")
upload = ico_api.uploads.start_upload(PROJECT_ID, data)

# Loop over all files and upload them to the before created upload entry
for dicom_path in DICOM_PATHS:
    ico_api.uploads.upload_dicom_path(upload.uri, dicom_path)

# Once all files have been uploaded, signal that they are all there and start the import/processing
upload = ico_api.uploads.complete_upload(upload.uri)

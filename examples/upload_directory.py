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
upload = ico_api.uploads.upload_dicom_dir(PROJECT_ID, DICOM_DIR_PATH, data)

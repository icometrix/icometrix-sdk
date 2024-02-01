import os
from io import BytesIO

import pydicom
from pydicom import FileDataset
from pydicom.errors import InvalidDicomError

from icometrix_sdk import IcometrixApi
from icometrix_sdk.models.upload_entity import StartUploadDto
from icometrix_sdk.utils.anonymizer import Anonymizer
from icometrix_sdk.utils.hash_factory import SHA3

PROJECT_ID = "5461177d-c34b-467e-8610-9ba71cbb3eb4"
SERVER = "https://icobrain-test.icometrix.com"
DICOM_DIR_PATH = "/Users/jpinxten/Downloads/LD_20111222"

hash_method = SHA3(size=512)
anonymizer = Anonymizer(hash_method)

# Initialize the icometrix API
ico_api = IcometrixApi(SERVER)

# Get the project, to make sure its there (will throw a 404 in case the project is not found)
project = ico_api.projects.get_one_by_id(PROJECT_ID)

# prepare an upload entry, this entry can be used to push a block of files to (which is typical in DICOM)
# Some options can be passed, for all available options please have a look at the StartUploadDto
data = StartUploadDto(icobrain_report_type="icobrain_ms")
upload = ico_api.uploads.start_upload(PROJECT_ID, data)

# Loop over all files in a DIR and upload them to the before created upload entry
for path, subdirs, files in os.walk(DICOM_DIR_PATH):
    for name in files:

        file_path = os.path.join(path, name)
        try:
            dicom_file = pydicom.dcmread(file_path)
        except InvalidDicomError:
            continue

        anonymized_dicom: FileDataset = anonymizer.anonymize(dicom_file)
        buffer = BytesIO()
        anonymized_dicom.save_as(buffer)
        buffer.seek(0)
        fields = {"file": (file_path, buffer.read(), "application/octet-stream")}
        ico_api.uploads.upload_dicom(upload.uri, fields=fields)

# Once all files have been uploaded, signal that they are all there and start the import/processing
upload = ico_api.uploads.complete_upload(upload.uri)

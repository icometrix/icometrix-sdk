import logging
import os
from icometrix_sdk import IcometrixApi, Region
from icometrix_sdk.models.upload_entity import StartUploadDto

PROJECT_ID = "<project_uuid>"
REPORT_TYPE = "<report_type>"

# A directory containing a T1 and FLAIR scan, as required for icobrain_ms for more info see HCP manual
DICOM_DIR_PATH = "<input_dir_path>"
OUTPUT_DIR = "<output_dir_path>"

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    os.environ["API_HOST"] = ""

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    processing_data = StartUploadDto(icobrain_report_type=REPORT_TYPE)
    ico_api.process_dicom_directory(PROJECT_ID, DICOM_DIR_PATH, OUTPUT_DIR, processing_data)
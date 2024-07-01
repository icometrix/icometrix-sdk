Data Processing Flow
====================

This page gives a high level overview, but there are ofc more internal pieces than written here. But this documentation
should give you sufficient information to understand the stages of processing and allow you to understand and
troubleshoot errors.

The data processing flow in our system involves several key steps:
*Uploading, Importing, Processing, QualityControl (optional), and Finished*.
Below is an overview of each step in the process.

Step 1: Uploading
^^^^^^^^^^^^^^^^^

The first step is to upload your DICOM files to the system. This involves starting an upload, uploading the files, and
completing the upload to signal that all files have been transferred. For more details see: :doc:`upload`

Step 2: Importing
^^^^^^^^^^^^^^^^^

Once the upload is completed, the files are imported into the system. This step involves importing the files into
our system and preparing them for processing.

Step 3: Processing
^^^^^^^^^^^^^^^^^^

In the processing step the DICOMS will first be checked for completeness (No missing slices, Required series are uploaded..)
and validity (Required DICOM tags are present and valid...) and processed according to the specified report type.

Step 4: QualityControl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The QualityControl step is not always triggered but can be used for ensuring the accuracy and quality of the processed data.
During this step, the results are reviewed and validated to ensure they meet the required standards.

Step 5: Finished
^^^^^^^^^^^^^^^^

The final step is marking the data as finished. At this point, the processed results are made available for the customer.

Example Code Snippet
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    import logging
    import os
    from icometrix_sdk import IcometrixApi, Region
    from icometrix_sdk.models.upload_entity import StartUploadDto

    PROJECT_ID = "<>"
    REPORT_TYPE = "icobrain_ms"

    # A directory containing a T1 and FLAIR scan, as required for icobrain_ms for more info see HCP manual
    DICOM_DIR_PATH = "<>"


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


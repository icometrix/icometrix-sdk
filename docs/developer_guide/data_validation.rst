Data validation
===============

When working with DICOM files, ensuring that all necessary files have been correctly uploaded is crucial for
maintaining data integrity and avoiding potential issues in subsequent processing.

Our SDK provides two methods for validating the completeness of your uploads:
**pre-import** validation and **post-import** validation. Each method has its own advantages depending on the stage of the process you are in.

Pre-import validation
---------------------

Pre-import validation allows you to check that all files within a single upload block are accounted for before
they are imported into the system.
This method is useful for catching any missing files early in the process, potentially saving time by identifying
issues before the import step.

How to Perform Pre-Import Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To perform pre-import validation, you can list all the files within a given upload and verify that the expected files are present.

.. caution::

    This has to be done **before completing the upload**. Reference :meth:`~icometrix_sdk.resources.uploads.Uploads.complete_upload`

.. code-block:: python

    import logging
    import os

    from icometrix_sdk import IcometrixApi
    from icometrix_sdk.models.upload_entity import StartUploadDto

    PROJECT_ID = "<your-project-uuid>"

    # A directory containing a T1 and FLAIR scan, as required for icobrain_ms. For more info, see HCP manual
    DICOM_DIR_PATH = "..."

    if __name__ == '__main__':
        os.environ["API_HOST"] = "https://icobrain-{region}.icometrix.com"

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


Post-import validation
----------------------

Post-import validation occurs after the DICOM files have been imported into the system. This method ensures that all
hierarchical :doc:`models` (Patients, Studies, Series, and individual DICOM files) have been correctly imported.

How to Perform Post-Import Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To perform post-import validation, you can query the system for the imported entities and verify that all expected
Patients, Studies, Series, and DICOM files are present.

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    PROJECT_ID = "<your-project-uuid>"

    # A directory containing your DICOM files
    DICOM_DIR_PATH = "..."

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

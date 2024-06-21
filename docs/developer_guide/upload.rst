How to Upload
=============

Uploading DICOM files using our Python SDK is a straightforward process that involves three main steps:

1. **starting the upload**

2. **uploading the files**

3. **completing the upload**.

You can choose to upload files one by one or use a higher-level function to upload all files in a directory.
Below, we outline these steps and provide example code to help you get started.

Upload All Files in a Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To simplify the process, you can use the :meth:`~icometrix_sdk.resources.uploads.Uploads.upload_all_files_in_dir` method, which will walk through all files and
subdirectories within a specified directory and upload each file.

.. code-block:: python

    import os
    from icometrix_sdk import IcometrixApi
    from icometrix_sdk.models.upload_entity import StartUploadDto

    PROJECT_ID = "uuid"
    DICOM_DIR_PATH = "<dir_path>"

    if __name__ == '__main__':
        os.environ["API_HOST"] = "https://icobrain-{region}.icometrix.com"

        # Initialize the icometrix API
        ico_api = IcometrixApi()

        # Get the project, to make sure it's there (will throw a 404 in case the project is not found)
        project = ico_api.projects.get_one_by_id(PROJECT_ID)

        # Start an upload
        data = StartUploadDto(icobrain_report_type="icobrain_ms")
        upload = ico_api.uploads.start_upload(PROJECT_ID, data)

        # Will walk through all files/subdirectories and upload all files
        ico_api.uploads.upload_all_files_in_dir(upload.uri, DICOM_DIR_PATH)

        # Once all files have been uploaded, signal that they are all there and start the import/processing
        upload = ico_api.uploads.complete_upload(upload.uri)


Upload Files Individually
^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer to upload files one by one, you can use the upload_file method.
This method requires the upload URI and the file path for each file you wish to upload.

.. code-block:: python

    ico_api.uploads.upload_dicom_path(upload.uri, dicom_path)


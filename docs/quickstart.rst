Quickstart
==========

.. currentmodule:: icometrix_sdk

Installing
----------

icometrix_sdk can be installed with `pip <https://pip.pypa.io>`_

.. code-block:: bash

  $ python -m pip install icometrix_sdk


Authentication
---------------

First things first, import the IcometrixApi:

.. code-block:: python

    from icometrix_sdk import IcometrixApi


Next thing is to set the correct server region (icobrain-eu.icometrix.com, icobrain-us.icometrix.com...):

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    SERVER = "https://icobrain-{region}.icometrix.com"

By default the icometrix_sdk will try to auto detect the authentication method. But we can
also force a method e.g. password authentication. To do this import the PasswordAuthentication
method and pass it as a parameter to the IcometrixApi.

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    SERVER = "https://icobrain-{region}.icometrix.com"

    auth = PasswordAuthentication("example@company.com", os.environ["PASSWORD"])
    client = RequestsApiClient(SERVER, auth)

    ico_api = IcometrixApi(client)

You can use :meth:`~icometrix_sdk.resources.profile.Profile.who_am_i` function to verify your connection

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    SERVER = "https://icobrain-{region}.icometrix.com"

    auth = PasswordAuthentication("example@company.com", os.environ["PASSWORD"])
    client = RequestsApiClient(SERVER, auth)

    ico_api = IcometrixApi(client)

    # Will raise an exception if the authentication failed.
    me = ico_api.profile.who_am_i()

    print(me.email)
    # "example@company.com"


This quickstart guide will help you get up and running with the `process_dicom_directory` function, which provides a
high-level interface for processing DICOM files from a specified directory.

In this example:

- Replace `"<project_uuid>"` with your project ID.
- Replace `"<input_dir_path>"` with the path to your input directory containing DICOM files.
- Replace `"<output_dir_path>"` with the path to your desired output directory.
- Replace `"<report_type>"` with the appropriate report type for your use case.

.. code-block:: python

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
        os.environ["API_HOST"] = Region.<REGION>.value

        # Initialize the icometrix API
        ico_api = IcometrixApi()

        processing_data = StartUploadDto(icobrain_report_type=REPORT_TYPE)
        ico_api.process_dicom_directory(PROJECT_ID, DICOM_DIR_PATH, OUTPUT_DIR, processing_data)
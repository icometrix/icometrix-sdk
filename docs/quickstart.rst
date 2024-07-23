Quickstart
==========

.. currentmodule:: icometrix_sdk

Installing
----------

icometrix_sdk can be installed with `pip <https://pip.pypa.io>`_

.. code-block:: bash

  $ python -m pip install icometrix_sdk


First steps
-----------

First things first, import the IcometrixApi:

.. code-block:: python

    from icometrix_sdk import IcometrixApi


Next thing is to set the correct server region (see regions below), you can do this by setting the `REGION` environment
variable or, for illustrative purposes, using python code:

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    os.environ["REGION"] = "<region>"

Authentication
--------------

By default the icometrix_sdk will try to auto detect the authentication method. The preferred way is using an API TOKEN.
You can use this my setting the `TOKEN` environment variable or, for illustrative purposes, using python code:

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    os.environ["TOKEN"] = "<token>"

We can also force a method e.g. password authentication. To do this import the PasswordAuthentication
method and pass it as a parameter to the IcometrixApi.

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    os.environ["REGION"] = "<region>"

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

Regions
-------
Icometrix hosts servers across various geographic regions including the European Union (EU),
the United States (US), Australia (AU), and Canada (CA).

You have the flexibility to select the region where your data will reside by specifying the desired region as
the `REGION` environment variable. This ensures that your data is processed and stored in compliance with local
data residency requirements.

Projects
--------

A project serves as a top-level isolation entity within our system, typically representing a single hospital or
medical facility. Each project is designed to prevent patient data collisions and ensure the segregation of
configurations, billing, and other operational aspects.

Projects are region-specific and are not replicated across different regions. This means you can have access to
projects in one or multiple regions, depending on your needs, but each project will remain isolated within its designated region.

To retrieve all your projects within the EU region, you can use the following example:

.. code-block:: python

    import os
    from icometrix_sdk import IcometrixApi
    from icometrix_sdk.utils.paginator import get_paginator

    os.environ["REGION"] = "EU"

    ico_api = IcometrixApi()

    for projects in get_paginator(ico_api.projects.get_all, page_size=5):
        for project in projects:
            print(project.name)

Processing data
---------------

This quickstart guide will help you get up and running with the `process_dicom_directory` function, which provides a
high-level interface for processing DICOM files from a specified directory.

In this example:

- Replace `"<project_uuid>"` with your project ID.
- Replace `"<input_dir_path>"` with the path to your input directory containing DICOM files.
- Replace `"<output_dir_path>"` with the path to your desired output directory.
- Replace `"<report_type>"` with the appropriate report type for your use case. (e.g. icobrain_ms, icobrain_dm...)

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
        os.environ["REGION"] = <REGION>

        # Initialize the icometrix API
        ico_api = IcometrixApi()

        processing_data = StartUploadDto(icobrain_report_type=REPORT_TYPE)
        ico_api.process_dicom_directory(PROJECT_ID, DICOM_DIR_PATH, OUTPUT_DIR, processing_data)
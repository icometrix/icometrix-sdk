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

    SERVER = "https://icobrain-test.icometrix.com"

By default the icometrix_sdk will try to auto detect the authentication method. But we can
also force a method e.g. password authentication. To do this import the PasswordAuthentication
method and pass it as a parameter to the IcometrixApi.

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    SERVER = "https://icobrain-test.icometrix.com"

    auth = PasswordAuthentication("example@company.com", os.environ["PASSWORD"])
    ico_api = IcometrixApi(SERVER, auth)

You can use :meth:`~IcometrixApi.profile.who_am_i` function to verify your connection

.. code-block:: python

    from icometrix_sdk import IcometrixApi

    SERVER = "https://icobrain-test.icometrix.com"

    auth = PasswordAuthentication("example@company.com", os.environ["PASSWORD"])
    ico_api = IcometrixApi(SERVER, auth)

    # Will raise an exception if the authentication failed.
    me = ico_api.profile.who_am_i()

    print(me.email)
    # "example@company.com"
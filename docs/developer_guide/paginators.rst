Paginators
==========

Some API operations may return incomplete results that require multiple requests to retrieve the entire
dataset. This process of fetching subsequent pages is known as pagination. Pagination is a crucial aspect when dealing
with large datasets to ensure efficient data retrieval.

Using Paginators
----------------

Sometimes it is needed to loop over all items in a collection, the SDK has a helper
:meth:`~icometrix_sdk.utils.paginator.get_paginator` function can simplify the process of iterating over the
:class:`~icometrix_sdk.models.base.PaginatedResponse` of a truncated API operation.

.. code-block:: python

    import os

    from icometrix_sdk import IcometrixApi
    from icometrix_sdk.utils.paginator import get_paginator

    PROJECT_ID = "<a-project-uuid>"

    os.environ["API_HOST"] = "https://icobrain-test.icometrix.com"

    # Initialize the icometrix API
    ico_api = IcometrixApi()

    for reports in get_paginator(ico_api.customer_reports.get_all, page_size=20, project_id=PROJECT_ID):
        for report in reports:
            print(report.study_instance_uid, report.report_status)




Models
======

Some API operations may return incomplete results that require multiple requests to retrieve the entire
dataset. This process of fetching subsequent pages is known as pagination. Pagination is a crucial aspect when dealing
with large datasets to ensure efficient data retrieval.

Base model
----------

All entities that are returned by the icometrix API extend the :class:`~icometrix_sdk.models.base.BackendEntity` entity.
The BaseEntity always has the following properties:

- :attr:`~icometrix_sdk.models.base.BackendEntity.id`: The unique identifier (uuid)
- :attr:`~icometrix_sdk.models.base.BackendEntity.update_timestamp`: The timestamp of the last update
- :attr:`~icometrix_sdk.models.base.BackendEntity.creation_timestamp`: The creation timestamp
- :attr:`~icometrix_sdk.models.base.BackendEntity.uri`: The uri to point to the location of the object

Collections
-----------

When fetching a collection of models from the API; you will always get a subset of that collection in combination with
some extra meta data. See: :doc:`paginators`

Relations
---------

High level overview of the relations between the available entities

.. mermaid:: model_relations.mmd


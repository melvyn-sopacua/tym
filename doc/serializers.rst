.. py:currentmodule:: ll2addr.serializers

Serializers
===========
The serializers module provides the DRF serializer, the
data model as a standard object and an adapter. The data
model is already described in the index and is a simple
python object with attributes. This may become a full-fledged
Django model or be reduced to a named tuple.

The serializer is a standard DRF serializer mapping the
object attributes to DRF fields.

The Adapter is described here.

.. autoclass:: AddressAdapter
    :members:

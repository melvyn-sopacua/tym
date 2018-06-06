.. include:: ../README.rst

Usage
-----
The API has one endpoint available at `/api/address`.
It requires lon and lat parameters via the query string in the request.
The data returned is the address associated with the coordinates or a
404 (Not Found) if no address information is available.

Address data
^^^^^^^^^^^^
The data returned is a JSON object with the following fields:

display
    The full address as formatted by the geocoding provider.



Further reading (API docs)
--------------------------

.. toctree::
    :maxdepth: 2

    serializers
    views

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

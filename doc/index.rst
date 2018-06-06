.. include:: ../README.rst

Usage
-----
The API has one endpoint available at ``/api/address``.
It requires lon and lat parameters via the query string in the request.
The data returned is the address associated with the coordinates or a
404 (Not Found) if no address information is available.

Address data
^^^^^^^^^^^^
The data returned is a JSON object with the following fields:

display
    The full address as formatted by the geocoding provider.

house_nr
    The house number part of the address

street
    The street part of the address

city
    The city the address is part of

postal_code
    Postal code or zip associated with the address

province
    Province, state or similar administrative region that is the first
    divider of a country.

country
    The country associated with the address

    NOTE: The language this country field is given in is by default the
    native language of the country, but this may vary. It can even be an
    abbreviation. This may be normalized in the future or the data may
    be extended with a ``country_code`` field.

address_type
    The type of address. At present this can be 'building' or 'place',
    but this may be extended and normalized in the future.


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

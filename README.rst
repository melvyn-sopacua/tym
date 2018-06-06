Test project for 3YourMind
==========================

This is a test project for 3YourMind, part of the hiring
process.
It implements a reverse geocoder, with pluggable cache and
pluggable geocoder backend.
Well, the pluggability of the cache is in fact Django's, but
we're not mentioning that :).

Installation
------------

The project can be installed by downloading the repository
and running the setup program::

    $ git clone https://github.com/melvyn-sopacua/tym.git
    $ cd tym
    $ ./setup.sh
    $ source .venv/bin/activate

The setup script creates a virtual environment with the
required dependencies. It assumed a ``python3`` is in the
PATH.

If one wants to build the documentation into HTML files,
``sphinx`` and ``sphinx_rtd_theme`` are needed::

    $ pip install sphinx spinx_rtd_theme
    $ cd doc
    $ make html

Then view the result with a browser in the ``_build`` directory.

Configuration
-------------

The project misses a ``SECRET_KEY`` and the ``ALLOWED_HOSTS``
from it's settings. These should be added to a file called
``local_settings.py`` in the ``tym`` directory.

How to setup a production level Django server is beyond the
scope of this document. However, to see if the project is
functional, first run the migrations, create the cache table
and then start the built-in webserver::

    $ python manage.py migrate
    $ python manage.py createcachetable
    $ python manage.py runserver

To verify if the server is working, open
`the following link <http://localhost:8000/api/address?lon=-1.81602098644987&lat=52.5487429714954>`_.


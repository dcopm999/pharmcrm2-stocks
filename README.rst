=============================
PharmCRM2: Stocks
=============================

.. image:: https://badge.fury.io/py/pharmcrm2-stocks.svg
    :target: https://badge.fury.io/py/pharmcrm2-stocks

.. image:: https://travis-ci.org/dcopm999/pharmcrm2-stocks.svg?branch=master
    :target: https://travis-ci.org/dcopm999/pharmcrm2-stocks

.. image:: https://codecov.io/gh/dcopm999/pharmcrm2-stocks/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/dcopm999/pharmcrm2-stocks

Stocks

Documentation
-------------

The full documentation is at https://pharmcrm2-stocks.readthedocs.io.

Quickstart
----------

Install PharmCRM2: Stocks::

    pip install pharmcrm2-stocks

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stocks',
        ...
    )

Add PharmCRM2: Stocks's URL patterns:

.. code-block:: python

    from stocks import urls as stocks_urls


    urlpatterns = [
        ...
        path('stocks/', include('stocks.urls')),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

=====
Usage
=====

To use PharmCRM2: Stocks in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'stocks.apps.StocksConfig',
        ...
    )

Add PharmCRM2: Stocks's URL patterns:

.. code-block:: python

    from stocks import urls as stocks_urls


    urlpatterns = [
        ...
        url(r'^', include(stocks_urls)),
        ...
    ]

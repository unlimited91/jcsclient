========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        | |codecov|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/client/badge/?style=flat
    :target: https://readthedocs.org/projects/client
    :alt: Documentation Status

.. |codecov| image:: https://codecov.io/github/jiocloudservices/client/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/jiocloudservices/client

.. |version| image:: https://img.shields.io/pypi/v/client.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/client

.. |downloads| image:: https://img.shields.io/pypi/dm/client.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/client

.. |wheel| image:: https://img.shields.io/pypi/wheel/client.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/client

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/client.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/client

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/client.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/client


.. end-badges

Client library for JCS

* Free software: BSD license

Installation
============

::

    pip install client

Documentation
=============

https://client.readthedocs.org/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

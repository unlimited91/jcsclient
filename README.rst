========
Overview
========

.. .. start-badges
..
.. .. list-table::
..     :stub-columns: 1
..
..     * - docs
..       - |docs|
..     * - tests
..       - |
..         | |codecov|
..     * - package
..       - |version| |downloads| |wheel| |supported-versions| |supported-implementations|
..
.. .. |docs| image:: https://readthedocs.org/projects/client/badge/?style=flat
..     :target: https://readthedocs.org/projects/client
..     :alt: Documentation Status
..
.. .. |codecov| image:: https://codecov.io/github/jiocloudservices/client/coverage.svg?branch=master
..     :alt: Coverage Status
..     :target: https://codecov.io/github/jiocloudservices/client
..
.. .. |version| image:: https://img.shields.io/pypi/v/client.svg?style=flat
..     :alt: PyPI Package latest release
..     :target: https://pypi.python.org/pypi/client
..
.. .. |downloads| image:: https://img.shields.io/pypi/dm/client.svg?style=flat
..     :alt: PyPI Package monthly downloads
..     :target: https://pypi.python.org/pypi/client
..
.. .. |wheel| image:: https://img.shields.io/pypi/wheel/client.svg?style=flat
..     :alt: PyPI Wheel
..     :target: https://pypi.python.org/pypi/client
..
.. .. |supported-versions| image:: https://img.shields.io/pypi/pyversions/client.svg?style=flat
..     :alt: Supported versions
..     :target: https://pypi.python.org/pypi/client
..
.. .. |supported-implementations| image:: https://img.shields.io/pypi/implementation/client.svg?style=flat
..     :alt: Supported implementations
..     :target: https://pypi.python.org/pypi/client
..
..
.. .. end-badges

Client library for JCS

* Free software: BSD license

Installation
============

.. pip install client

::

    git clone https://gitlab.com/jiocloudservices/common.git
    cd common
    sudo pip install -r requirements.txt   # Can use virtual environment too
    sudo python setup.py develop

Configuration
=============

Edit the src/client/config.py to include your credentials.

If you are from your local machine, you might need to add entries to `/etc/hosts` file to map an IP to the endpoint. No need to do the same if you are using this library from a staging machien.

**NOTE**: Never ever commit your access and secret keys and push to a public repository. You have been warned.


.. Documentation
.. =============
..
.. https://client.readthedocs.org/

CLI
===

You can use CLI to make an API request, or just get the input which you can use with 'curl' command.

::

    $ jcs compute Action=DescribeInstances          # Make an API call
    
    $ jcs --prettyprint compute Action=DescribeInstances # Make API call and pretty-print dictionary
    
    $ jcs --curl compute Action=DescribeInstances   # Get the curl input URL


Python Client
=============

Once you have installed this library in your computer (systemwide or in a virtual environment), you can import the module and start using the associated Python functions. For example, the following file will list all your instances:

::

    from client import cloud
    print cloud.describe_instances()



.. To run the all tests run::
..
..     tox
..
.. Note, to combine the coverage data from all the tox environments run:
..
.. .. list-table::
..     :widths: 10 90
..     :stub-columns: 1
..
..     - - Windows
..       - ::
..
..             set PYTEST_ADDOPTS=--cov-append
..             tox
..
..     - - Other
..       - ::
..
..             PYTEST_ADDOPTS=--cov-append tox

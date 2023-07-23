trino-query-parser
==================

|pypi| |python|

.. |pypi| image:: https://img.shields.io/pypi/v/trino-query-parser
  :alt: PyPI

.. |python| image:: https://img.shields.io/pypi/pyversions/trino-query-parser
  :alt: PyPI - Python Version

|

The package provides a parser for trino queries.

Install
-------

To install the package run:

.. code-block:: bash

    pip install trino-query-parser

Example
-------

.. code-block:: python3

    >>> from trino_query_parser import parse_statement
    >>> parse_statement('select * from x.y')
    [['SELECT', '*', 'FROM', ['X', '.', 'Y']], '<EOF>']

Details
-------

:code:`trino-query-parser` uses `trino antlr4 grammar <https://raw.githubusercontent.com/trinodb/trino/405/core/trino-parser/src/main/antlr4/io/trino/sql/parser/SqlBase.g4>`_ to generate python parser code.

If you care about specific version of :code:`trino`, install the corresponding version of :code:`trino-query-parser`.

For example, for :code:`trino-405` run:

.. code-block:: bash

    pip install trino-query-parser~=0.405.0

If there is no such version, feel free to open an issue.

.. warning::

    Be careful, API is not stable, it might change in new versions

Development
-----------

To install development dependencies run:

.. code-block:: bash

    pip install -e .[test,dev]

To generate antlr4 parser code run:

.. code-block:: bash

    make generate-code

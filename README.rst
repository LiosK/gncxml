gncxml
======

gncxml - extract entries from GnuCash data file to pandas.DataFrame

Installation
------------

.. code:: bash

    pip install gncxml

Usage (Command Line)
--------------------

::

    usage: gncxml [-h] [-l] [--csv] TYPE [FILE]

    gncxml - print entries in GnuCash data file as data frame

    positional arguments:
      TYPE        type of entries to print (account | commodity | price | split |
                  transaction)
      FILE        GnuCash data file (gzipped XML format)

    optional arguments:
      -h, --help  show this help message and exit
      -l, --long  list in long format
      --csv       print in csv format

Usage (Python Module)
---------------------

.. code:: python

    import sys
    import gncxml

    try:
        book = gncxml.Book("mybook.gnucash")
    except OSError as err:
        sys.exit(err)

    # Extract splits as pandas.DataFrame
    df = book.list_splits()
    print(df[df["trn_date"] >= "2017-10-01"].to_csv())

See also: `examples/module_usage.ipynb`_

.. _examples/module_usage.ipynb: https://github.com/LiosK/gncxml/blob/master/examples/module_usage.ipynb

License
-------

Copyright 2017 LiosK

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

See Also
--------

- `gncxml - Python Package Index`_

.. _gncxml - Python Package Index: https://pypi.python.org/pypi/gncxml

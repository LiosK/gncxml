gncxml
======

gncxml - extract entries in GnuCash data file as pandas.DataFrame

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

`The MIT License`_:

Copyright 2017 LiosK.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

.. _The MIT License: https://opensource.org/licenses/MIT

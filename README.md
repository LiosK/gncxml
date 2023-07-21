# gncxml

[![PyPI](https://img.shields.io/pypi/v/gncxml)](https://pypi.org/project/gncxml/)

gncxml - extract entries from GnuCash data file to pandas.DataFrame

## Installation

```bash
pip install gncxml
```

## Usage (Command Line)

```
usage: gncxml [-h] [-l] [--csv] TYPE [FILE]

gncxml - print entries in GnuCash data file as data frame

positional arguments:
  TYPE        type of entries to print (account | commodity | price | split |
              transaction)
  FILE        GnuCash data file (XML format)

optional arguments:
  -h, --help  show this help message and exit
  -l, --long  list in long format
  --csv       print in csv format
```

## Usage (Python Module)

```python
import sys
import gncxml

try:
    book = gncxml.Book("mybook.gnucash")
except OSError as err:
    sys.exit(err)

# Extract splits as pandas.DataFrame
df = book.list_splits()
print(df[df["trn_date"] >= "2023-07-01"].to_csv())
```

See also: [examples/module_usage.ipynb](https://github.com/LiosK/gncxml/blob/master/examples/module_usage.ipynb)

## License

Copyright 2017-2022 LiosK

Licensed under the Apache License, Version 2.0.

# gncxml: extract entries from GnuCash data file

## Installation

```bash
pip install git+https://github.com/LiosK/gncxml.git
```

## Usage (Command Line)

```
usage: gncxml [-h] [-l] [--csv] TYPE [FILE]

Extract entries from GnuCash data file.

positional arguments:
  TYPE        type of data to extract (account | commodity | price | split |
              transaction)
  FILE        GnuCash data file (gzipped XML format)

optional arguments:
  -h, --help  show this help message and exit
  -l, --long  list in long format
  --csv       output in csv format
```

## Usage (Python Module)

```python
import gzip
import gncxml

filename = "mybook.gnucash"
with gzip.open(filename) as xml:
    book = gncxml.Book(xml)

# Extract splits as pandas.DataFrame
df = book.list_splits()
print(df[df["trn_date"] >= "2017-10-01"].to_csv())
```

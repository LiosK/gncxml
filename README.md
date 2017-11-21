# gncxml: extract entries from GnuCash data file

## Installation

```bash
pip install git+https://github.com/LiosK/gncxml.git
```

## Usage

```
usage: gncxml [-h] [-l] TYPE [FILE]

Extract entries from GnuCash data file.

positional arguments:
  TYPE        type of data to extract (account|commodity|transaction|split)
  FILE        GnuCash data file (gzipped XML format)

optional arguments:
  -h, --help  show this help message and exit
  -l, --long  list in long format
```

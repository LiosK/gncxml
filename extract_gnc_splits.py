#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

import os
import sys
import gzip
import pandas as pd

import gncxml

def main():
    if len(sys.argv) <= 1:
        print("Usage: {0} GNC_XML".format(sys.argv[0]), file=sys.stderr)
        sys.exit(os.EX_USAGE)

    try:
        with gzip.open(sys.argv[1]) as f:
            book = gncxml.Book(f)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        sys.exit(os.EX_NOINPUT)

    splits = book.list_splits()
    csv = pd.DataFrame(splits, columns=[
        "tr_date",
        "tr_desc",
        "tr_cmsp",
        "tr_cmid",
        "sp_top",
        "sp_act",
        "sp_memo",
        "sp_cmsp",
        "sp_cmid",
        "quantity",
        "value",
        ]).to_csv()
    print(csv)


if __name__ == "__main__":
    main()

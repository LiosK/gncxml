#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

import os
import sys
import gzip

import gncxml

def main():
    if len(sys.argv) <= 1:
        print("Usage: {0} FILE".format(sys.argv[0]), file=sys.stderr)
        sys.exit(os.EX_USAGE)

    try:
        with gzip.open(sys.argv[1]) as f:
            book = gncxml.Book(f)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        sys.exit(os.EX_NOINPUT)

    splits = book.list_splits().reset_index()
    print(splits[[
        'trn_date',
        'trn_description',
        'trn_cmd_space',
        'trn_cmd_id',
        'trn_cmd_name',
        'act_path',
        'act_toplevel',
        'act_type',
        'act_code',
        'act_cmd_space',
        'act_cmd_id',
        'act_cmd_name',
        'memo',
        'reconciled',
        'quantity',
        'value',
        ]].to_csv(index=False))


if __name__ == "__main__":
    main()

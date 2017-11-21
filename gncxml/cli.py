# vim: set fileencoding=utf-8 :

import argparse
import gzip
import sys

import gncxml

def main(prog="gncxml"):
    args = build_argparser(prog).parse_args()

    try:
        with gzip.open(args.file) as f:
            book = gncxml.Book(f)
    except OSError as err:
        sys.exit("error: {0} '{1}'".format(err, args.file.name))

    df = None
    if args.type in {"account", "act"}:
        df = book.list_accounts().reset_index()
        if not args.long:
            df = df[["path", "toplevel", "code", "description", "cmd_space", "cmd_id"]]
    elif args.type in {"commodity", "cmdty"}:
        df = book.list_commodities().reset_index()
    elif args.type in {"transaction", "trn"}:
        df = book.list_transactions().reset_index()
        if not args.long:
            df = df[["date", "description", "cmd_space", "cmd_id"]]
    elif args.type in {"split", "sp"}:
        df = book.list_splits().reset_index()
        if not args.long:
            df = df[[
                'trn_date', 'trn_description', 'trn_cmd_space', 'trn_cmd_id',
                'act_path', 'act_toplevel', 'act_code', 'act_cmd_space', 'act_cmd_id',
                'memo', 'reconciled', 'quantity', 'value',
                ]]

    print(df.to_csv(index=False), end="")


def build_argparser(prog):
    parser = argparse.ArgumentParser(
            prog=prog,
            description="Extract entries from GnuCash data file."
            )
    parser.add_argument(
            "type",
            choices=["account", "commodity", "transaction", "split", "act", "cmdty", "trn", "sp"],
            help="type of data to extract (account|commodity|transaction|split)",
            metavar="TYPE"
            )
    parser.add_argument(
            "file",
            nargs="?",
            default=sys.stdin.buffer,
            type=argparse.FileType("rb"),
            help="GnuCash data file (gzipped XML format)",
            metavar="FILE"
            )
    parser.add_argument("-l", "--long", action="store_true", help="list in long format")
    return parser

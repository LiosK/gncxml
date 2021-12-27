# vim: set fileencoding=utf-8 :

import argparse
import sys

import gncxml


def main():
    """Run command line interface."""
    args = _build_argparser().parse_args()

    try:
        book = gncxml.Book(args.file)
    except OSError as err:
        return err

    tp = None
    df = None
    if args.type in {"account", "act"}:
        tp = "account"
        df = book.list_accounts()
    elif args.type in {"commodity", "cmdty"}:
        tp = "commodity"
        df = book.list_commodities()
    elif args.type in {"price"}:
        tp = "price"
        df = book.list_prices()
    elif args.type in {"split", "sp"}:
        tp = "split"
        df = book.list_splits()
    elif args.type in {"transaction", "trn"}:
        tp = "transaction"
        df = book.list_transactions()

    df.reset_index(inplace=True)
    if not args.long:
        df = df[_get_select_cols(tp)]

    if args.csv:
        print(df.to_csv(index=False), end="")
    else:
        print(df.to_string(index=False))


def _build_argparser():
    parser = argparse.ArgumentParser(
        description="gncxml - print entries in GnuCash data file as data frame"
    )
    parser.add_argument(
        "type",
        choices=[
            "account",
            "act",
            "commodity",
            "cmdty",
            "price",
            "split",
            "sp",
            "transaction",
            "trn",
        ],
        help="type of entries to print (account | commodity | price | split | transaction)",
        metavar="TYPE",
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=sys.stdin.buffer,
        type=argparse.FileType("rb"),
        help="GnuCash data file (XML format)",
        metavar="FILE",
    )
    parser.add_argument("-l", "--long", action="store_true", help="list in long format")
    parser.add_argument("--csv", action="store_true", help="print in csv format")
    return parser


def _get_select_cols(tp):
    return {
        "account": [
            "path",
            "toplevel",
            "code",
            "description",
            "cmd_space",
            "cmd_id",
        ],
        "commodity": ["space", "id", "name", "xcode", "exponent"],
        "price": [
            "time",
            "cmd_space",
            "cmd_id",
            "crncy_space",
            "crncy_id",
            "source",
            "type",
            "value",
        ],
        "split": [
            "trn_date",
            "trn_description",
            "trn_crncy_space",
            "trn_crncy_id",
            "act_path",
            "act_toplevel",
            "act_code",
            "act_cmd_space",
            "act_cmd_id",
            "memo",
            "reconciled",
            "quantity",
            "value",
        ],
        "transaction": ["date", "description", "crncy_space", "crncy_id"],
    }[tp]

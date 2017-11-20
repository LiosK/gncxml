#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :

import sys
import gzip
import decimal
import xml.etree.ElementTree as ET
import pandas as pd

def main():
    import os
    if len(sys.argv) <= 1:
        print("Usage: {0} GNC_XML".format(sys.argv[0]), file=sys.stderr)
        sys.exit(os.EX_USAGE)

    try:
        with gzip.open(sys.argv[1]) as f:
            tree = ET.parse(f)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        sys.exit(os.EX_NOINPUT)

    accounts = build_account_map(tree)
    splits = list_splits(tree, accounts)
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


def build_account_map(tree):
    """Build account dictionary"""
    ns = get_namespaces()
    def tx(elem, path, default=None, namespaces=ns):
        return elem.findtext(path, default, namespaces)

    accounts = {}
    for e in tree.findall("./gnc:book/gnc:account", ns):
        act = accounts[tx(e, "./act:id")] = {
                "name": tx(e, "./act:name"),
                "parent": accounts.get(tx(e, "./act:parent"), None), # XXX assuming order
                "cmdty:space": tx(e, "./act:commodity/cmdty:space"),
                "cmdty:id": tx(e, "./act:commodity/cmdty:id"),
                }
        is_root = act["parent"] is None
        if not is_root:
            is_toplevel = act["parent"]["parent"] is None
            if is_toplevel:
                act["path"] = act["toplevel"] = act["name"]
            else:
                act["path"] = act["parent"]["path"] + ":" + act["name"]
                act["toplevel"] = act["parent"]["toplevel"]

    return accounts


def list_splits(tree, accounts):
    """ Build list of split records """
    ns = get_namespaces()
    def tx(elem, path, default=None, namespaces=ns):
        return elem.findtext(path, default, namespaces)
    def frac2decimal(frac):
        (num, den) = frac.split("/")
        return decimal.Decimal(num) / decimal.Decimal(den)

    splits = []
    for trn in tree.findall("./gnc:book/gnc:transaction", ns):
        header = {
                "tr_date": tx(trn, "./trn:date-posted/ts:date").split(" ")[0],
                "tr_desc": tx(trn, "./trn:description"),
                "tr_cmsp": tx(trn, "./trn:currency/cmdty:space"),
                "tr_cmid": tx(trn, "./trn:currency/cmdty:id"),
                }

        for sp in trn.findall("./trn:splits/trn:split", ns):
            act = accounts[tx(sp, "./split:account")]
            splits.append({
                **header,
                "sp_memo": tx(sp, "./split:memo", ""),
                "sp_act": act["path"],
                "sp_top": act["toplevel"],
                "sp_cmsp": act["cmdty:space"],
                "sp_cmid": act["cmdty:id"],
                "quantity": frac2decimal(tx(sp, "./split:quantity")),
                "value": frac2decimal(tx(sp, "./split:value")),
                })

    return splits


def get_namespaces():
    return {
            "act": "http://www.gnucash.org/XML/act",
            "cmdty": "http://www.gnucash.org/XML/cmdty",
            "gnc": "http://www.gnucash.org/XML/gnc",
            "split": "http://www.gnucash.org/XML/split",
            "trn": "http://www.gnucash.org/XML/trn",
            "ts": "http://www.gnucash.org/XML/ts",
            }


if __name__ == "__main__":
    main()

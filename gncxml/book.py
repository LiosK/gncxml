# vim: set fileencoding=utf-8 :

from decimal import Decimal
from fractions import Fraction
import collections
import gzip
import re
import xml.etree.ElementTree as ET

import pandas as pd

import gncxml.iso4217 as iso4217

class Book:

    def __init__(self, gncfile):
        """
        gncfile : file name or file object
            Gzipped GnuCash XML data file
        """
        with gzip.open(gncfile) as source:
            self._tree = ET.parse(source)

        self._ns = {
                "act": "http://www.gnucash.org/XML/act",
                "cmdty": "http://www.gnucash.org/XML/cmdty",
                "gnc": "http://www.gnucash.org/XML/gnc",
                "price": "http://www.gnucash.org/XML/price",
                "split": "http://www.gnucash.org/XML/split",
                "trn": "http://www.gnucash.org/XML/trn",
                "ts": "http://www.gnucash.org/XML/ts",
                }


    def commodities(self):
        """Return commodity data frame."""
        tx = self._findtext_wrapper(self._ns)

        items = []
        dec = re.compile(r"^10*$")
        for e in self._tree.findall("./gnc:book/gnc:commodity", self._ns):
            space = tx(e, "./cmdty:space", "")
            cmdid = tx(e, "./cmdty:id")
            crncy = {"name": None, "fraction": None}
            if space == "ISO4217":
                crncy = iso4217.get(cmdid, crncy)
            item = {
                    "space": space,
                    "id": cmdid,
                    "name": tx(e, "./cmdty:name", crncy["name"]),
                    "xcode": tx(e, "./cmdty:xcode"),
                    "fraction": tx(e, "./cmdty:fraction", crncy["fraction"]),
                    "exponent": None,
                    "quote_source": tx(e, "./cmdty:quote_source"),
                    }
            if dec.match(item["fraction"] or ""):
                item["exponent"] = len(item["fraction"]) - 1.0  # float to treat NaN
            items.append(item)

        return pd.DataFrame(items, columns=[
            "space",
            "id",
            "name",
            "xcode",
            "fraction",
            "exponent",
            "quote_source",
            ]).set_index(["space", "id"])


    def list_commodities(self):
        """Return commodity data frame as flatten list."""
        return self.commodities()


    def accounts(self):
        """Return account data frame."""
        tx = self._findtext_wrapper(self._ns)

        items = collections.OrderedDict()
        for e in self._tree.findall("./gnc:book/gnc:account", self._ns):
            cur = e.find("./act:id", self._ns)
            cur_key = (cur_idtype, cur_id) = (cur.attrib.get("type", ""), cur.text)
            parent = e.find("./act:parent", self._ns)
            if parent is not None:
                parent = (parent.attrib.get("type", ""), parent.text)
            items[cur_key] = {
                    "idtype": cur_idtype,
                    "id": cur_id,
                    "name": tx(e, "./act:name"),
                    "type": tx(e, "./act:type"),
                    "code": tx(e, "./act:code"),
                    "description": tx(e, "./act:description"),
                    "cmd_space": tx(e, "./act:commodity/cmdty:space", ""),
                    "cmd_id": tx(e, "./act:commodity/cmdty:id"),
                    "parent": parent,
                    }

        def retrieve_path(e):
            if "toplevel" in e: # already set
                return e
            if e["parent"] is None: # root
                e["path"] = e["toplevel"] = None
                return e
            parent = retrieve_path(items[e["parent"]])
            if parent["toplevel"] is None: # toplevel
                e["path"] = e["toplevel"] = e["name"]
            else:
                e["path"] = parent["path"] + ":" + e["name"]
                e["toplevel"] = parent["toplevel"]
            return e

        return pd.DataFrame([retrieve_path(e) for e in items.values()], columns=[
            "idtype",
            "id",
            "path",
            "toplevel",
            "type",
            "code",
            "description",
            "cmd_space",
            "cmd_id",
            # "name",
            # "parent",
            ]).set_index(["idtype", "id"])


    def list_accounts(self):
        """Return account data frame as flatten list."""
        cmds = self.commodities().add_prefix("cmd_")
        return self.accounts().join(cmds, ["cmd_space", "cmd_id"])

    def prices(self):
        """Return price data frame."""
        tx = self._findtext_wrapper(self._ns)

        items = []
        for e in self._tree.findall("./gnc:book/gnc:pricedb/price", self._ns):
            val = Fraction(tx(e, "./price:value"))
            items.append({
                "time": pd.Timestamp(tx(e, "./price:time/ts:date")),
                "cmd_space": tx(e, "./price:commodity/cmdty:space", ""),
                "cmd_id": tx(e, "./price:commodity/cmdty:id"),
                "crncy_space": tx(e, "./price:currency/cmdty:space", ""),
                "crncy_id": tx(e, "./price:currency/cmdty:id"),
                "source": tx(e, "./price:source"),
                "type": tx(e, "./price:type", "unknown"),
                "value": Decimal(val.numerator) / Decimal(val.denominator),
                "value_frac": val,
                })

        return pd.DataFrame(items, columns=[
                "time",
                "cmd_space",
                "cmd_id",
                "crncy_space",
                "crncy_id",
                "source",
                "type",
                "value",
                "value_frac",
            ])


    def list_prices(self):
        """Return price data frame as flatten list."""
        cmds = self.commodities()
        return self.prices().join(
                cmds.add_prefix("cmd_"), ["cmd_space", "cmd_id"]
                ).join(cmds.add_prefix("crncy_"), ["crncy_space", "crncy_id"])


    def transactions(self):
        """Return transaction data frame."""
        tx = self._findtext_wrapper(self._ns)

        items = []
        for e in self._tree.findall("./gnc:book/gnc:transaction", self._ns):
            trnid = e.find("./trn:id", self._ns)
            items.append({
                "idtype": trnid.attrib.get("type", ""),
                "id": trnid.text,
                "date": pd.Timestamp(tx(e, "./trn:date-posted/ts:date").split(" ")[0]),
                "description": tx(e, "./trn:description"),
                "crncy_space": tx(e, "./trn:currency/cmdty:space", ""),
                "crncy_id": tx(e, "./trn:currency/cmdty:id"),
                })

        return pd.DataFrame(items, columns=[
            "idtype",
            "id",
            "date",
            "description",
            "crncy_space",
            "crncy_id",
            ]).set_index(["idtype", "id"])


    def list_transactions(self):
        """Return transaction data frame as flatten list."""
        cmds = self.commodities().add_prefix("crncy_")
        return self.transactions().join(cmds, ["crncy_space", "crncy_id"])


    def splits(self):
        """Return split data frame."""
        tx = self._findtext_wrapper(self._ns)

        items = []
        for e in self._tree.findall("./gnc:book/gnc:transaction", self._ns):
            trnid = e.find("./trn:id", self._ns)
            header = {
                    "trn_idtype": trnid.attrib.get("type", ""),
                    "trn_id": trnid.text,
                    }
            for sp in e.findall("./trn:splits/trn:split", self._ns):
                spid = sp.find("./split:id", self._ns)
                actid = sp.find("./split:account", self._ns)
                val = Fraction(tx(sp, "./split:value"))
                qty = Fraction(tx(sp, "./split:quantity"))
                items.append({
                    "idtype": spid.attrib.get("type", ""),
                    "id": spid.text,
                    "memo": tx(sp, "./split:memo", ""),
                    "reconciled": tx(sp, "./split:reconciled-state", ""),
                    "value": Decimal(val.numerator) / Decimal(val.denominator),
                    "value_frac": val,
                    "quantity": Decimal(qty.numerator) / Decimal(qty.denominator),
                    "quantity_frac": qty,
                    "act_idtype": actid.attrib.get("type", ""),
                    "act_id": actid.text,
                    **header,
                    })

        return pd.DataFrame(items, columns=[
            "idtype",
            "id",
            "memo",
            "reconciled",
            "value",
            "value_frac",
            "quantity",
            "quantity_frac",
            "act_idtype",
            "act_id",
            "trn_idtype",
            "trn_id",
            ]).set_index(["idtype", "id"])


    def list_splits(self):
        """Return split data frame as flatten list."""
        acts = self.list_accounts().add_prefix("act_")
        trns = self.list_transactions().add_prefix("trn_")
        return self.splits().join(acts, ["act_idtype", "act_id"]).join(trns, ["trn_idtype", "trn_id"])


    def _findtext_wrapper(self, ns):
        return lambda elem, path, default=None: elem.findtext(path, default, ns)

# vim: set fileencoding=utf-8 :

import decimal
import xml.etree.ElementTree as ET

class Book:

    def __init__(self, source):
        """
        source : file object
            Gunzipped GnuCash XML data
        """
        self._tree = ET.parse(source)
        self._ns = {
                "act": "http://www.gnucash.org/XML/act",
                "cmdty": "http://www.gnucash.org/XML/cmdty",
                "gnc": "http://www.gnucash.org/XML/gnc",
                "split": "http://www.gnucash.org/XML/split",
                "trn": "http://www.gnucash.org/XML/trn",
                "ts": "http://www.gnucash.org/XML/ts",
                }


    def accounts(self):
        """Build account dictionary."""
        tx = self._findtext_wrapper(self._ns)

        accounts = {}
        for e in self._tree.findall("./gnc:book/gnc:account", self._ns):
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

    def commodities(self):
        pass

    def list_transactions(self):
        pass

    def list_splits(self):
        """Build list of split records."""
        tx = self._findtext_wrapper(self._ns)
        def frac2decimal(frac):
            (num, den) = frac.split("/")
            return decimal.Decimal(num) / decimal.Decimal(den)

        accounts = self.accounts()
        splits = []
        for trn in self._tree.findall("./gnc:book/gnc:transaction", self._ns):
            header = {
                    "tr_date": tx(trn, "./trn:date-posted/ts:date").split(" ")[0],
                    "tr_desc": tx(trn, "./trn:description"),
                    "tr_cmsp": tx(trn, "./trn:currency/cmdty:space"),
                    "tr_cmid": tx(trn, "./trn:currency/cmdty:id"),
                    }

            for sp in trn.findall("./trn:splits/trn:split", self._ns):
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


    def _findtext_wrapper(self, ns):
        return lambda elem, path, default=None: elem.findtext(path, default, ns)

# vim: set fileencoding=utf-8 :

import collections
import decimal
import xml.etree.ElementTree as ET

import pandas as pd

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


    def commodities(self):
        """Return commodity data frame."""
        tx = self._findtext_wrapper(self._ns)

        cmds = []
        for e in self._tree.findall("./gnc:book/gnc:commodity", self._ns):
            cmdid = tx(e, "./cmdty:id")
            cmds.append({
                "space": tx(e, "./cmdty:space", ""),
                "id": cmdid,
                "name": tx(e, "./cmdty:name", cmdid),
                "quote_source": tx(e, "./cmdty:quote_source", "NA"),
                })

        return pd.DataFrame(cmds, columns=[
            "space",
            "id",
            "name",
            "quote_source",
            ]).set_index(["space", "id"])


    def list_commodities(self):
        """Return commodity data frame as flatten list."""
        return self.commodities()


    def accounts(self):
        """Return account data frame."""
        tx = self._findtext_wrapper(self._ns)

        accounts = collections.OrderedDict()
        for e in self._tree.findall("./gnc:book/gnc:account", self._ns):
            cur = e.find("./act:id", self._ns)
            cur_key = (cur_idtype, cur_id) = (cur.attrib.get("type", ""), cur.text)
            parent = e.find("./act:parent", self._ns)
            if parent is not None:
                parent = (parent.attrib.get("type", ""), parent.text)
            accounts[cur_key] = {
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
            parent = retrieve_path(accounts[e["parent"]])
            if parent["toplevel"] is None: # toplevel
                e["path"] = e["toplevel"] = e["name"]
            else:
                e["path"] = parent["path"] + ":" + e["name"]
                e["toplevel"] = parent["toplevel"]
            return e

        return pd.DataFrame([retrieve_path(e) for e in accounts.values()], columns=[
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


    def transactions(self):
        """Return transaction data frame."""
        tx = self._findtext_wrapper(self._ns)

        trns = []
        for e in self._tree.findall("./gnc:book/gnc:transaction", self._ns):
            trnid = e.find("./trn:id", self._ns)
            trns.append({
                "idtype": trnid.attrib.get("type", ""),
                "id": trnid.text,
                "date": pd.Timestamp(tx(e, "./trn:date-posted/ts:date").split(" ")[0]),
                "description": tx(e, "./trn:description"),
                "cmd_space": tx(e, "./trn:currency/cmdty:space", ""),
                "cmd_id": tx(e, "./trn:currency/cmdty:id"),
                })

        return pd.DataFrame(trns, columns=[
            "idtype",
            "id",
            "date",
            "description",
            "cmd_space",
            "cmd_id",
            ]).set_index(["idtype", "id"])


    def list_transactions(self):
        """Return transaction data frame as flatten list."""
        cmds = self.commodities().add_prefix("cmd_")
        return self.transactions().join(cmds, ["cmd_space", "cmd_id"])


    def splits(self):
        """Return split data frame."""
        tx = self._findtext_wrapper(self._ns)

        def parse_num(strfrac):
            (num, den) = strfrac.split("/")
            return decimal.Decimal(num) / decimal.Decimal(den)

        sps = []
        for e in self._tree.findall("./gnc:book/gnc:transaction", self._ns):
            trnid = e.find("./trn:id", self._ns)
            header = {
                    "trn_idtype": trnid.attrib.get("type", ""),
                    "trn_id": trnid.text,
                    }
            for sp in e.findall("./trn:splits/trn:split", self._ns):
                spid = sp.find("./split:id", self._ns)
                actid = sp.find("./split:account", self._ns)
                sps.append({
                    "idtype": spid.attrib.get("type", ""),
                    "id": spid.text,
                    "memo": tx(sp, "./split:memo", ""),
                    "reconciled": tx(sp, "./split:reconciled-state", ""),
                    "value": parse_num(tx(sp, "./split:value")),
                    "quantity": parse_num(tx(sp, "./split:quantity")),
                    "act_idtype": actid.attrib.get("type", ""),
                    "act_id": actid.text,
                    **header,
                    })

        return pd.DataFrame(sps, columns=[
            "idtype",
            "id",
            "memo",
            "reconciled",
            "value",
            "quantity",
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

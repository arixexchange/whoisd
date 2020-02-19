# database.py

import pymongo
import hashlib

class ARIXDatabase:
    def __init__(self, mongo_uri="mongodb://localhost"):
        self._client = pymongo.MongoClient(mongo_uri)
        self._db = self._client["arix"]

        # Collections
        self._mntner = self._db["mntner"]
        self._autnum = self._db["aut-num"]
        self._route = self._db["route"]
        self._route6 = self._db["route6"]

    def add_mntner(self, callsign, password):
        return str(self._mntner.insert_one({
            "mntner": callsign + "-MNT",
            "auth": str(hashlib.sha512(password.encode()).hexdigest())
        }).inserted_id)

    def get_mntner(self, mntner):
        out = self._mntner.find_one({"mntner": str(mntner)})
        if out:
            del out["_id"]
            out["auth"] = "# Filtered"
        return out

    def add_aut_num(self, callsign):
        return str(self._autnum.insert_one({
            "aut-num": self._autnum.find().sort("aut-num", pymongo.DESCENDING)[0]["aut-num"] + 1,
            "as-name": callsign + "-AS",
            "mnt-by": callsign + "-MNT"
        }).inserted_id)

    def get_aut_num(self, asn):
        out = self._autnum.find_one({"aut-num": int(asn)})
        if out:
            del out["_id"]
        return out

    def add_route(self, cidr, asn):
        aut_num = self._autnum.find_one({"aut-num": int(asn)})
        if aut_num == None:
            print("Cannot find ASN " + str(asn))
        else:
            return str(self._route.insert_one({
                "route": cidr,
                "origin": "AS" + str(asn),
                "mnt-by": aut_num["mnt-by"]
            }).inserted_id)

    def get_route(self, route):
        out = self._route.find_one({"route": route})
        if out:
            del out["_id"]
        return out

    def add_route6(self, cidr, asn):
        aut_num = self._autnum.find_one({"aut-num": int(asn)})
        if aut_num == None:
            print("Cannot find ASN " + str(asn))
        else:
            return str(self._route6.insert_one({
                "route6": cidr,
                "origin": "AS" + str(asn),
                "mnt-by": aut_num["mnt-by"]
            }).inserted_id)

    def get_route6(self, route6):
        out = self._route6.find_one({"route6": route6})
        if out:
            del out["_id"]
        return out

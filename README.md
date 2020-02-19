# ARIXDB

ARIX operates a whois database for ARIX private ASNs. The server runs a custom whois daemon which uses a very simple RPSL-like syntax. The server can be queried with a standard whois client at `whois.arix.dev`.



### Queries

ARIXDB has a very simple structure. There are only 4 object types. `mntner`, `aut-num`, `route`, and `route6`.



#### `mntner`

mntner objects store information about a maintainer. In the case of ARIX this will be a licensed Amateur Radio Operator with a valid callsign. mntner objects look like `CALLSIGN-MNT` and have a single `auth` attribute containing the SHA512 hashed password. This attribute is always filtered by the whois service.

```
mntner:    KJ7DMC-MNT
auth:      # Filtered
source:    ARIX
```



#### `aut-num`

aut-num objects store information about a specific Autonomous System Number (ASN).

```
aut-num:   64512
as-name:   KJ7DMC-AS
mnt-by:    KJ7DMC-MNT
source:    ARIX
```



#### `route`

route objects store information about an IPv4 prefix and the originating ASN. It is important to note that the only valid IPv4 range on ARIX is 44.190.40.0/23. All other ranges are not supported by ARIX.

```
route:     44.190.40.0/29
origin:    64512
mnt-by:    KJ7DMC-MNT
source:    ARIX
```



#### `route6`

route6 objects store information about an IPv6 prefix and the originating ASN. It is important to note that the only valid IPv6 range on ARIX is 2a0e:8f00:fdd1::/48. All other ranges are not supported by ARIX.

```
route6:    2a0e:8f00:fdd1:beef::/96
origin:    64512
mnt-by:    KJ7DMC-MNT
source:    ARIX
```



There is a notable absence of `inetnum` and `inet6num` objects. These important objects are omitted for simplicity of the database and because the ARIX ranges 44.190.40.0/23 and 2a0e:8f00:fdd1::/48 are already registered in ALTDB for public usage. This will undoubtedly be a controversial topic for some, but at the current scale of ARIX, we have decided to remove these objects for simplicity.



### Updates

ARIXDB can currently only be updated by ARIX administrators. Contact the team by email or keybase and we'll update your object(s) right away.

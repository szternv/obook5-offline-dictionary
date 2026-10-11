#!/usr/bin/env python3
"""Apply the physically validated selected-word autofill patch to libdictionaryview.

Validated on the tested OBOOK5 hardware. This script still refuses unknown input hashes.
"""
from pathlib import Path
import hashlib, sys

STOCK_MD5 = "e18ae4624cb2bdf1edc041f203757b5d"
FINAL_MD5 = "02ef37b7d69995475b8cf5406ed4b053"

PATCHES = {
    0x33358: (bytes.fromhex("7888998f"), bytes.fromhex("c082998f")), # fetchWord -> setWord
    0x33374: (bytes.fromhex("1000428c"), bytes.fromhex("1000bc8f")),
    0x33378: (bytes.fromhex("0400428c"), bytes.fromhex("6888998f")), # search()
    0x3337C: (bytes.fromhex("0004427c"), bytes.fromhex("09f82003")),
    0x33380: (bytes.fromhex("0a004010"), bytes.fromhex("25204000")),
    0x33388: (bytes.fromhex("6884998f"), bytes.fromhex("08000010")),
    0x3338C: (bytes.fromhex("09f82003"), bytes.fromhex("00000000")),
}

def md5(b): return hashlib.md5(b).hexdigest()

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_autofill_v2.py INPUT_LIB OUTPUT_LIB")
inp, out = map(Path, sys.argv[1:])
data = bytearray(inp.read_bytes())
if md5(data) != STOCK_MD5:
    raise RuntimeError(f"unsupported input MD5: {md5(data)}")
for off, (old, new) in PATCHES.items():
    got = bytes(data[off:off+len(old)])
    if got != old:
        raise RuntimeError(f"unexpected bytes at 0x{off:x}: {got.hex()}")
    data[off:off+len(new)] = new
result = md5(data)
if result != FINAL_MD5:
    raise RuntimeError(f"final MD5 mismatch: {result}")
out.write_bytes(data)
print(f"OK: {out} MD5={result}")

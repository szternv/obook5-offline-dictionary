#!/usr/bin/env python3
"""Reproduce the working Search->Dictionary proof-of-concept.

Research-only. Requires a matching OBOOK library and LLVM clang/objcopy.
The preferred manufacturer implementation is source-level.
"""
from pathlib import Path
import hashlib, struct, subprocess, sys, tempfile

STOCK_MD5 = "97f249f7a36b773582e78e80896e993b"
INTERMEDIATE_MD5 = "f1fa2e2e13dcd2a439248d56f5776692"
FINAL_MD5 = "86cd2535d141d13cb7abe4fd60746326"

EARLY_PATCHES = {
    0x12A624: (bytes.fromhex("2c80868f"), bytes.fromhex("3480868f")),
    0x12A634: (bytes.fromhex("ac7dc624"), bytes.fromhex("5885c624")),
    0x12A6A0: (bytes.fromhex("08000524"), bytes.fromhex("04000524")),
    0x13717C: (bytes.fromhex("2c80868f"), bytes.fromhex("3480868f")),
    0x137190: (bytes.fromhex("ac7dc624"), bytes.fromhex("5885c624")),
    0x1371A4: (bytes.fromhex("08000324"), bytes.fromhex("04000324")),
}

LATE_LABEL_PATCHES = {
    0x113AB0: (bytes.fromhex("2c80868f"), bytes.fromhex("3480868f")),
    0x113AC4: (bytes.fromhex("ac7dc624"), bytes.fromhex("5885c624")),
}

def md5(b): return hashlib.md5(b).hexdigest()

def apply(data, table):
    for off, (old, new) in table.items():
        got = bytes(data[off:off+len(old)])
        if got != old:
            raise RuntimeError(f"unexpected bytes at 0x{off:x}: {got.hex()} != {old.hex()}")
        data[off:off+len(new)] = new

if len(sys.argv) != 3:
    raise SystemExit("usage: apply_search_to_dictionary.py INPUT_LIB OUTPUT_LIB")

inp, out = map(Path, sys.argv[1:])
data = bytearray(inp.read_bytes())
start = md5(data)
if start == STOCK_MD5:
    apply(data, EARLY_PATCHES)
    if md5(data) != INTERMEDIATE_MD5:
        raise RuntimeError("intermediate MD5 did not match tested build")
elif start != INTERMEDIATE_MD5:
    raise RuntimeError(f"unsupported input MD5: {start}")

hook_src = Path(__file__).with_name("search_to_dictionary_hook.S")
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    obj, raw = td/'hook.o', td/'hook.bin'
    subprocess.run(["clang","-target","mipsel-linux-gnu","-march=mips32r2","-mabi=32","-fPIC","-c",str(hook_src),"-o",str(obj)], check=True)
    subprocess.run(["llvm-objcopy","-O","binary","--only-section=.text",str(obj),str(raw)], check=True)
    hook = raw.read_bytes()

search_va = 0x101EC4
if data[search_va:search_va+4] != bytes.fromhex("0e001c3c"):
    raise RuntimeError("unexpected function prologue")
data[search_va:search_va+len(hook)] = hook
apply(data, LATE_LABEL_PATCHES)

# Extend RW PT_LOAD and .bss by 4 bytes for persistent DictFetchScrWord*.
phoff = struct.unpack_from("<I", data, 0x1C)[0]
phentsize = struct.unpack_from("<H", data, 0x2A)[0]
rw_ph = phoff + 3*phentsize
p = list(struct.unpack_from("<IIIIIIII", data, rw_ph))
if p[0] != 1 or p[2] != 0x1BA000:
    raise RuntimeError("unexpected RW LOAD layout")
p[5] += 4
struct.pack_into("<IIIIIIII", data, rw_ph, *p)

shoff = struct.unpack_from("<I", data, 0x20)[0]
shentsize = struct.unpack_from("<H", data, 0x2E)[0]
shnum = struct.unpack_from("<H", data, 0x30)[0]
shstrndx = struct.unpack_from("<H", data, 0x32)[0]
shstr_hdr = shoff + shstrndx*shentsize
shstr_off = struct.unpack_from("<I", data, shstr_hdr+0x10)[0]
shstr_size = struct.unpack_from("<I", data, shstr_hdr+0x14)[0]
shstr = data[shstr_off:shstr_off+shstr_size]
for i in range(shnum):
    off = shoff + i*shentsize
    name_off = struct.unpack_from("<I", data, off)[0]
    name = bytes(shstr[name_off:]).split(b"\0",1)[0]
    if name == b".bss":
        size = struct.unpack_from("<I", data, off+0x14)[0]
        struct.pack_into("<I", data, off+0x14, size+4)
        break
else:
    raise RuntimeError(".bss not found")

result = md5(data)
if result != FINAL_MD5:
    raise RuntimeError(f"result MD5 {result} != tested {FINAL_MD5}")
out.write_bytes(data)
print(f"OK: {out} MD5={result}")

#!/bin/sh
set -u
OUT="/user/OBOOK_STOCK_EXPORT"
LOG="/user/obook-stock-export.log"
exec >"$LOG" 2>&1
mkdir -p "$OUT"
cp -f /opt/image/opt/Qtopia/lib/libeinkfbreader.so.1.0.0 "$OUT/"
cp -f /opt/image/opt/Qtopia/lib/libdictionaryview.so.1.0.0 "$OUT/"
md5sum "$OUT/libeinkfbreader.so.1.0.0" "$OUT/libdictionaryview.so.1.0.0" > "$OUT/MD5SUMS.txt"
sync
cat "$OUT/MD5SUMS.txt"

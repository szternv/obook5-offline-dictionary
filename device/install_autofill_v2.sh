#!/bin/sh
set -u

SRC="/user/libdictionaryview.autofill-v2.so.1.0.0"
DST="/opt/image/opt/Qtopia/lib/libdictionaryview.so.1.0.0"
BACKUP="/user/OBOOK_BACKUP_libdictionaryview.so.1.0.0"
LOG="/user/obook-autofill-v2.log"

EXPECTED_STOCK="e18ae4624cb2bdf1edc041f203757b5d"
EXPECTED_NEW="02ef37b7d69995475b8cf5406ed4b053"

exec >"$LOG" 2>&1

md5_of() {
    md5sum "$1" 2>/dev/null | awk '{print $1}'
}

echo "=== OBOOK5 dictionary autofill v2 ==="
date
echo "current:  `md5_of "$DST"`"
echo "payload:  `md5_of "$SRC"`"
echo "expected: $EXPECTED_NEW"

if [ ! -f "$SRC" ]; then
    echo "ERROR: missing $SRC"
    exit 60
fi

if [ "`md5_of "$SRC"`" != "$EXPECTED_NEW" ]; then
    echo "ERROR: payload checksum mismatch."
    exit 61
fi

CUR=`md5_of "$DST"`
if [ "$CUR" = "$EXPECTED_NEW" ]; then
    echo "Already installed."
    exit 0
fi

if [ "$CUR" != "$EXPECTED_STOCK" ]; then
    echo "ERROR: current libdictionaryview is not the known stock build."
    echo "Expected stock: $EXPECTED_STOCK"
    echo "Nothing changed."
    exit 62
fi

# Preserve a stock backup if there isn't already a valid one.
if [ ! -f "$BACKUP" ] || [ "`md5_of "$BACKUP"`" != "$EXPECTED_STOCK" ]; then
    cp -f "$DST" "$BACKUP"
    sync
fi

if ! mount -o remount,rw /opt; then
    echo "ERROR: could not remount /opt read-write."
    exit 63
fi

TMP="$DST.obook-new"
rm -f "$TMP"
cp -f "$SRC" "$TMP"
chmod 0755 "$TMP"

if [ "`md5_of "$TMP"`" != "$EXPECTED_NEW" ]; then
    echo "ERROR: copied file checksum mismatch."
    rm -f "$TMP"
    mount -o remount,ro /opt || true
    exit 64
fi

mv -f "$TMP" "$DST"
sync
mount -o remount,ro /opt || true

echo "installed: `md5_of "$DST"`"
echo "SUCCESS"
echo
echo "Behavior:"
echo "selected word -> setWord(selected) -> search() -> stock showFullScreen"
echo
echo "The Search->Dictionary reader patch and dictionary databases were untouched."

sync
sleep 2
reboot

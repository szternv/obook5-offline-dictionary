#!/bin/sh
set -u

BACKUP="/user/OBOOK_BACKUP_libdictionaryview.so.1.0.0"
DST="/opt/image/opt/Qtopia/lib/libdictionaryview.so.1.0.0"
LOG="/user/obook-autofill-v2-restore.log"
EXPECTED_STOCK="e18ae4624cb2bdf1edc041f203757b5d"

exec >"$LOG" 2>&1

md5_of() {
    md5sum "$1" 2>/dev/null | awk '{print $1}'
}

echo "=== Restore stock libdictionaryview ==="
date

if [ ! -f "$BACKUP" ] || [ "`md5_of "$BACKUP"`" != "$EXPECTED_STOCK" ]; then
    echo "ERROR: valid stock backup not found."
    exit 70
fi

mount -o remount,rw /opt || exit 71
cp -f "$BACKUP" "$DST"
chmod 0755 "$DST"
sync
mount -o remount,ro /opt || true

echo "restored: `md5_of "$DST"`"
sync
sleep 2
reboot

#!/bin/sh
BACKUP="/user/OBOOK_BACKUP_libeinkfbreader.so.1.0.0"
DST="/opt/image/opt/Qtopia/lib/libeinkfbreader.so.1.0.0"
LOG="/user/obook-dictionary-restore.log"

exec >"$LOG" 2>&1
echo "=== OBOOK reader restore ==="
date

if [ ! -f "$BACKUP" ]; then
    echo "ERROR: backup not found: $BACKUP"
    exit 30
fi

if ! mount -o remount,rw /opt; then
    echo "ERROR: could not remount /opt read-write."
    exit 31
fi

cp -f "$BACKUP" "$DST"
chmod 0755 "$DST"
sync
md5sum "$DST"
mount -o remount,ro /opt || true

echo "Restored. Rebooting..."
sync
sleep 2
reboot

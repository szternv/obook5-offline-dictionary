#!/bin/sh
set -u

SRC="/user/libeinkfbreader.dictionary.so.1.0.0"
DST="/opt/image/opt/Qtopia/lib/libeinkfbreader.so.1.0.0"
BACKUP="/user/OBOOK_BACKUP_libeinkfbreader.so.1.0.0"
LOG="/user/obook-dictionary-patch.log"
EXPECTED_STOCK="97f249f7a36b773582e78e80896e993b"
EXPECTED_OLD="f1fa2e2e13dcd2a439248d56f5776692"
EXPECTED_NEW="86cd2535d141d13cb7abe4fd60746326"

exec >"$LOG" 2>&1

echo "=== OBOOK Search -> Dictionary patch ==="
date
echo

if [ ! -f "$SRC" ]; then
    echo "ERROR: missing $SRC"
    exit 20
fi

SRC_MD5=`md5sum "$SRC" | awk '{print $1}'`
CUR_MD5=`md5sum "$DST" | awk '{print $1}'`

echo "source md5:  $SRC_MD5"
echo "current md5: $CUR_MD5"
echo "target md5:  $EXPECTED_NEW"

if [ "$SRC_MD5" != "$EXPECTED_NEW" ]; then
    echo "ERROR: patch file checksum does not match."
    exit 21
fi

if [ "$CUR_MD5" = "$EXPECTED_NEW" ]; then
    echo "Patch is already installed."
    exit 0
fi

if [ "$CUR_MD5" != "$EXPECTED_OLD" ] && [ "$CUR_MD5" != "$EXPECTED_STOCK" ]; then
    echo "ERROR: installed reader is not a known tested build."
    echo "Nothing was changed."
    exit 22
fi

if [ ! -f "$BACKUP" ]; then
    cp -f "$DST" "$BACKUP"
    sync
fi

# Keep the known-good built-in English->Chinese dictionary active for the first test.
cat > /home/Settings/dictionary.conf <<'EOF'
[global]
default=/opt/image/opt/Qtopia/data/dictdb/default_ec0.dict
[dictionary]
selected=/opt/image/opt/Qtopia/data/dictdb/default_ec0.dict
EOF
chmod 0644 /home/Settings/dictionary.conf

echo
echo "Remounting /opt read-write..."
if ! mount -o remount,rw /opt; then
    echo "ERROR: could not remount /opt read-write."
    exit 23
fi

TMP="$DST.obook-new"
rm -f "$TMP"
cp -f "$SRC" "$TMP"
chmod 0755 "$TMP"

TMP_MD5=`md5sum "$TMP" | awk '{print $1}'`
if [ "$TMP_MD5" != "$EXPECTED_NEW" ]; then
    echo "ERROR: copied file failed checksum verification."
    rm -f "$TMP"
    mount -o remount,ro /opt
    exit 24
fi

mv -f "$TMP" "$DST"
sync
NEW_MD5=`md5sum "$DST" | awk '{print $1}'`
echo "installed md5: $NEW_MD5"

mount -o remount,ro /opt || true

if [ "$NEW_MD5" != "$EXPECTED_NEW" ]; then
    echo "ERROR: installed file checksum is wrong."
    exit 25
fi

echo
echo "SUCCESS."
echo "The reader Search handler now calls DictFetchScrWord::searchWord()."
echo "The visible menu label remains Search; tapping it now opens Dictionary."
echo "A backup is at: $BACKUP"
echo
echo "Rebooting once so bookreader definitely loads the new library..."
sync
sleep 2
reboot

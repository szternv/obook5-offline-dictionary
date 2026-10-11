#!/bin/sh
# EDIT ONLY THIS:
DICT_NAME="MyDictionary.dict"

ROOT="/user/OBOOK_DICTIONARIES"
LINKROOT="/data/.词典"
SRC="/user/$DICT_NAME"
DST="$ROOT/$DICT_NAME"
LINK="$LINKROOT/$DICT_NAME"
LOG="/user/obook-install-dictionary.log"

exec >"$LOG" 2>&1
mkdir -p "$ROOT" "$LINKROOT"

[ -f "$SRC" ] && mv -f "$SRC" "$DST"
[ -f "$DST" ] || { echo "ERROR: $DST not found"; exit 1; }

rm -f "$LINK"
ln -s "$DST" "$LINK"

cat > /home/Settings/dictionary.conf <<EOF
[global]
default=$LINK
[dictionary]
selected=$LINK
EOF

chmod 0644 /home/Settings/dictionary.conf
sync
echo "Installed and selected: $DICT_NAME"
sleep 2
reboot

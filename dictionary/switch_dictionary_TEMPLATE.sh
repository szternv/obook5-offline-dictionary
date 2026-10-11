#!/bin/sh
# EDIT ONLY THIS:
DICT_NAME="MyDictionary.dict"

ROOT="/user/OBOOK_DICTIONARIES"
LINKROOT="/data/.词典"
DST="$ROOT/$DICT_NAME"
LINK="$LINKROOT/$DICT_NAME"

[ -f "$DST" ] || exit 1
mkdir -p "$LINKROOT"
rm -f "$LINK"
ln -s "$DST" "$LINK"

cat > /home/Settings/dictionary.conf <<EOF
[global]
default=$LINK
[dictionary]
selected=$LINK
EOF

sync
sleep 2
reboot

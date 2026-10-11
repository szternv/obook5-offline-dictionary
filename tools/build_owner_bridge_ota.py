#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, tarfile, tempfile, os, re

BASE_MD5 = "8ced2385925ac03b0f6a82aa73a8e7bc"

BRIDGE_BLOCK = r'''
# === OBOOK OWNER BRIDGE PUBLIC POC ===
RCS="/etc/init.d/rcS"
RCS_BACKUP="/home/rcS.pre-obook-tools.backup"
HOOK="/home/obook-owner-boot-hook.sh"
INSTALL_LOG="/user/obook_owner_bridge_install.log"

cat > "$HOOK" <<'EOF'
#!/bin/sh
i=0
while [ $i -lt 90 ]; do
    if grep -qs " /user " /proc/mounts; then
        break
    fi
    sleep 1
    i=$((i+1))
done

if ! grep -qs " /user " /proc/mounts; then
    exit 0
fi

echo "boot-hook reached: $(date)" >> /user/obook-boot-hook.log 2>&1

if [ -f /user/ENABLE_OBOOK_STARTUP ] && [ -f /user/obook-startup.sh ]; then
    rm -f /user/ENABLE_OBOOK_STARTUP
    /bin/sh /user/obook-startup.sh > /user/obook-startup.log 2>&1
    RC=$?
    echo "startup script exit=$RC at $(date)" >> /user/obook-boot-hook.log
    sync
fi
EOF
chmod 0755 "$HOOK"

{
    echo "=== OBOOK OWNER BRIDGE INSTALL ==="
    date
} > "$INSTALL_LOG" 2>&1

if [ -f "$RCS" ]; then
    if [ ! -f "$RCS_BACKUP" ]; then
        cp -p "$RCS" "$RCS_BACKUP"
    fi

    mount -o remount,rw / 2>>"$INSTALL_LOG"

    if ! grep -q "OBOOK OWNER BRIDGE PUBLIC POC" "$RCS"; then
        cat >> "$RCS" <<'EOF'

# === OBOOK OWNER BRIDGE PUBLIC POC ===
/home/obook-owner-boot-hook.sh &
# === END OBOOK OWNER BRIDGE PUBLIC POC ===
EOF
    fi

    chmod 0755 "$RCS"
    sync
    mount -o remount,ro / 2>>"$INSTALL_LOG"
else
    echo "ERROR: /etc/init.d/rcS not found" >> "$INSTALL_LOG"
fi
sync
# === END OBOOK OWNER BRIDGE PUBLIC POC ===
'''

def md5_file(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def append_once(path, marker, block):
    data = path.read_bytes()
    text = data.decode("utf-8", errors="surrogateescape")
    if marker not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += block
        path.write_bytes(text.encode("utf-8", errors="surrogateescape"))

def patch_version(root, version):
    v = root/"image/opt/Qtopia/home/version"
    if v.exists():
        v.write_text(version + "\n", encoding="utf-8")
    x = root/"image/opt/Qtopia/home/upgrade.xml"
    if x.exists():
        t = x.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r"<Version>.*?</Version>", f"<Version>{version}</Version>", t)
        x.write_text(t, encoding="utf-8")

def rebuild_checksum(root):
    checksum = root/"upgrade_files.chksum"
    lines = checksum.read_text(encoding="utf-8").splitlines()
    new = []
    for line in lines:
        if not line.strip() or ":" not in line:
            continue
        rel, _ = line.rsplit(":", 1)
        rel_clean = rel[2:] if rel.startswith("./") else rel
        p = root/rel_clean
        if not p.is_file():
            raise RuntimeError(f"checksum-listed file missing: {rel}")
        new.append(f"{rel}:{md5_file(p)}")
    checksum.write_text("\n".join(new) + "\n", encoding="utf-8")

def repack(src_dir, out):
    with tarfile.open(out, "w:gz", compresslevel=9) as tf:
        for name in sorted(os.listdir(src_dir)):
            tf.add(src_dir/name, arcname=name, recursive=True)

ap = argparse.ArgumentParser()
ap.add_argument("official_v13_img")
ap.add_argument("output_img")
ap.add_argument("--version", default="V1.4")
args = ap.parse_args()

inp = Path(args.official_v13_img)
out = Path(args.output_img)

actual = md5_file(inp)
if actual != BASE_MD5:
    raise SystemExit(f"STOP: unsupported official image MD5 {actual}; expected {BASE_MD5}")

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    with tarfile.open(inp, "r:gz") as tf:
        tf.extractall(td)

    for rel in ("script/upgraded.sh", "script_ext/upgraded.sh"):
        p = td/rel
        if not p.exists():
            raise RuntimeError(f"missing {rel}")
        append_once(p, "OBOOK OWNER BRIDGE PUBLIC POC", BRIDGE_BLOCK)

    patch_version(td, args.version)
    rebuild_checksum(td)
    out.parent.mkdir(parents=True, exist_ok=True)
    repack(td, out)

md5 = md5_file(out)
Path(str(out)+".md5").write_text(md5, encoding="ascii")
print(f"Created: {out}")
print(f"MD5: {md5}")
print(f"MD5 file: {out}.md5")

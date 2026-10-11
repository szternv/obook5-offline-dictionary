# Beginner guide: the one-time local OTA step

This is the most technical part of the whole installation, so this page
explains the goal before the details.

## What are we trying to do?

Normally the OBOOK asks OBOOK's server:

```text
"Is there an update for me?"
```

For the one-time bridge installation, we want **your own OBOOK on your own
network** to ask your PC instead.

Your PC runs `tools/ota_server.py`.

So the desired path is:

```text
YOUR OBOOK
    |
    | asks for service.obook.com.cn:8085
    v
YOUR LOCAL DNS / ROUTER
    |
    | points that hostname to your PC
    v
YOUR PC
    |
    `-- ota_server.py serves your locally built bridge package
```

Nothing needs to be exposed to the public Internet.

---

## Step A — Find your PC's local address

If you are using Windows Mobile Hotspot, the host is commonly:

```text
192.168.137.1
```

but verify yours.

Open PowerShell:

```powershell
ipconfig
```

Look for the adapter used by the hotspot/local network.

You need the IPv4 address that the OBOOK can reach.

---

## Step B — Start the OTA server

Example:

```powershell
python .\tools\ota_server.py `
  --host-ip 192.168.137.1 `
  --image C:\obook-work\obook5-v1.4-owner-bridge.img `
  --version V1.4
```

Keep this window open.

If Windows Firewall asks whether Python can accept connections on the private
network, allow it for the private/local network you are using.

---

## Step C — Make the update hostname resolve locally

The OBOOK needs:

```text
service.obook.com.cn
```

to resolve to the PC's local address for this temporary setup.

How you do that depends on your network.

Examples include:

- a router with a local DNS override / host override feature;
- a local DNS server running on the PC;
- a hotspot setup whose DNS can be configured to your local resolver.

The important result is not the specific software you use.

The important result is:

```text
OBOOK asks for service.obook.com.cn
        ↓
connection reaches YOUR PC on port 8085
```

---

## Step D — Know whether it worked

With `ota_server.py` running, choose **Check upgrade** on the OBOOK.

Watch the PC console.

A successful connection should show a request containing something similar to:

```text
GET /readerapi.aspx?version=...&model=epd86s2e
```

That console request is your best confirmation that the network routing is
correct.

If the OBOOK says there is no update and the PC console shows nothing, the
problem is still DNS/networking.

---

## Step E — Common problems

### The PC server starts, but the OBOOK never connects

Check:

1. OBOOK and PC are on the same intended network.
2. The hostname is really resolving to the PC from that network.
3. Windows Firewall allows Python on the private network.
4. TCP port 8085 is not blocked.
5. `ota_server.py` is still running.
6. The `--host-ip` value is the address the OBOOK can actually reach.

### I can open localhost on the PC, but the OBOOK cannot connect

`localhost` means "this same device".

On the PC:

```text
localhost
```

means the PC itself.

On the OBOOK, it would mean the OBOOK itself.

The OBOOK must use the PC's actual local address, such as:

```text
192.168.137.1
```

### The console receives `/readerapi.aspx`, but the image download fails

Check that:

- the image path passed to `--image` exists;
- the matching `.md5` file is next to it;
- the filenames have not changed after starting the server.

---

## After this step

Once the owner bridge is installed and confirmed, you normally do not need the
local OTA setup again.

Search -> Dictionary, autofill, rollback, and dictionary selection are handled
through the normal USB-visible storage plus the one-shot startup marker.

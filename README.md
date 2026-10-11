# 📖 OBOOK5 Offline Dictionary Mod

Enable the OBOOK5's **built-in offline dictionary**, make it automatically look up the word you selected, and install your own dictionaries.

This guide is written for people who are comfortable copying files and following commands, but **do not need to know Linux, MIPS assembly, reverse engineering, or firmware development**.

The final result looks like this:

```text
Read a book
   ↓
Long-press a word
   ↓
Tap "Search"
   ↓
The stock Dictionary app opens
   ↓
The selected word appears automatically
   ↓
The OBOOK searches it automatically
   ↓
You see the definition / translation
```

This full flow has been tested on a real OBOOK5.

> [!IMPORTANT]
> This project does **not** include OBOOK firmware or OBOOK proprietary program files.
> You use your own compatible firmware/device files and the included tools modify them locally.

---

# 🟢 Start here

There are **four main stages**:

```text
1. Check that your OBOOK matches the tested model
2. Install the one-time "owner bridge"
3. Install the Dictionary + autofill patches
4. Add whatever dictionaries you want
```

The first three stages are normally done only once.

After that, installing another dictionary is much easier.

---

# ✅ Is my OBOOK compatible?

This release was tested with:

| Item | Tested value |
|---|---|
| Device | OBOOK5 |
| Model / board | `epd86s2e` |
| Official firmware | V1.3 |
| Processor | Ingenic X2000 |
| Screen | 480 × 800 |

You will also verify file hashes later.

> [!CAUTION]
> If the hashes in this guide do not match your files, **stop**.
> Do not try to bypass the checks.
>
> A different firmware revision may contain different machine code even if the device looks identical.

Exact tested hashes are in [`docs/TESTED_HASHES.md`](docs/TESTED_HASHES.md).

Observed UI behavior is documented in [`docs/UI_BEHAVIOR.md`](docs/UI_BEHAVIOR.md).

---

# 🧰 What you need

You need:

- your OBOOK5;
- its USB cable;
- a Windows PC;
- Wi-Fi;
- Python 3 installed on Windows;
- WSL with Ubuntu installed;
- your own copy of the exact compatible OBOOK5 V1.3 update image;
- this repository.

You do **not** need to know programming to follow the normal installation.

---

# 1. Prepare Windows

## 1.1 Check that Python is installed

Open the Windows Start menu.

Type:

```text
PowerShell
```

Open **Windows PowerShell**.

Type:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.12.4
```

The exact version does not matter as long as it is Python 3.

If Windows says that `python` is not recognized, install Python 3 first and then reopen PowerShell.

---

## 1.2 Install WSL / Ubuntu

WSL lets Windows run Linux command-line tools.

If you already have Ubuntu in WSL, skip this section.

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart Windows if it asks you to.

Then open **Ubuntu** from the Start menu.

The first time it opens, Ubuntu may ask you to create:

- a Linux username;
- a Linux password.

These can be different from your Windows login.

---

## 1.3 Install the build tools inside Ubuntu

Inside the Ubuntu window, run:

```bash
sudo apt update
```

It may ask for the Linux password you created.

Then run:

```bash
sudo apt install python3 clang llvm tar gzip coreutils
```

When Ubuntu asks whether you want to continue, type:

```text
Y
```

and press Enter.

When the command finishes, the Linux tools are ready.

---

# 2. Make a safe work folder

Do not work directly inside the GitHub repository.

Inside Ubuntu, create a separate folder:

```bash
mkdir -p ~/obook-work/build
mkdir -p ~/obook-work/stock
mkdir -p ~/obook-work/unpacked
```

Think of this folder as your private workshop.

It is where your own OBOOK firmware and extracted OBOOK files will live.

They should **not** be uploaded to GitHub.

---

# 3. Put your official OBOOK V1.3 update image in the work folder

You need your own legitimate copy of the compatible official OBOOK5 V1.3 update image.

For the rest of this guide we will call it:

```text
obook5-v1.3.img
```

Place it somewhere convenient on Windows.

For example:

```text
C:\Users\YOURNAME\Downloads\obook5-v1.3.img
```

In WSL, Windows drives appear under `/mnt/`.

So:

```text
C:\
```

becomes:

```text
/mnt/c/
```

For example:

```bash
cp /mnt/c/Users/YOURNAME/Downloads/obook5-v1.3.img ~/obook-work/
```

Replace `YOURNAME` with your actual Windows user folder.

---

# 4. Verify that your firmware is the exact tested firmware

This is one of the most important safety checks.

Inside Ubuntu:

```bash
md5sum ~/obook-work/obook5-v1.3.img
```

For the firmware used by this project, you should get:

```text
8ced2385925ac03b0f6a82aa73a8e7bc
```

So the complete line should look similar to:

```text
8ced2385925ac03b0f6a82aa73a8e7bc  /home/yourname/obook-work/obook5-v1.3.img
```

## If it matches

Continue.

## If it does NOT match

**Stop here.**

Do not edit the script to ignore the hash.

Your firmware may simply be a different version that needs its own compatibility work.

---

# 5. Build the one-time owner bridge

## What is the owner bridge?

Normally, files you copy to the OBOOK over USB are just normal user files.

The **owner bridge** gives you a simple way to tell your own OBOOK:

> "On the next boot, run this one script once with system permissions."

It watches for these two files:

```text
ENABLE_OBOOK_STARTUP
obook-startup.sh
```

When both exist, the OBOOK runs the script once.

The marker is removed before the script runs, so a bad script should not run again automatically forever.

You normally install the owner bridge only once.

---

## 5.1 Build the bridge update

You need to run the repository's bridge builder.

Assume the repository folder is accessible from Ubuntu.

Run:

```bash
python3 tools/build_owner_bridge_ota.py \
  ~/obook-work/obook5-v1.3.img \
  ~/obook-work/build/obook5-v1.4-owner-bridge.img \
  --version V1.4
```

If your terminal is not currently inside the repository folder, first `cd` into it.

For example:

```bash
cd /mnt/c/Users/YOURNAME/Downloads/OBOOK5_OFFLINE_DICTIONARY
```

Then run the command above.

The script creates:

```text
~/obook-work/build/obook5-v1.4-owner-bridge.img
~/obook-work/build/obook5-v1.4-owner-bridge.img.md5
```

> [!NOTE]
> `V1.4` here is only a name used for our local modified package.
> It is **not** an official OBOOK firmware version.

---

# 6. Let the OBOOK download your local bridge update

This is the most unusual part of the installation.

The OBOOK normally asks OBOOK's update server whether an update exists.

For this one-time owner installation, you temporarily make **your own OBOOK, on your own local network**, ask your PC instead.

Your PC then serves the bridge package you just created.

---

## 6.1 Put the PC and OBOOK on the same local network

One easy option on Windows is **Mobile Hotspot**.

Open:

```text
Settings → Network & Internet → Mobile hotspot
```

Turn it on.

Connect the OBOOK to that hotspot.

A common Windows hotspot address for the PC is:

```text
192.168.137.1
```

But do not assume yours is identical.

---

## 6.2 Make the OBOOK update hostname point to your PC

The tested updater contacts:

```text
service.obook.com.cn
```

on port:

```text
8085
```

For this controlled installation, your local DNS/router must resolve that hostname to the PC that will run `ota_server.py`.

In other words, on your temporary local setup you want:

```text
service.obook.com.cn
        ↓
YOUR PC'S LOCAL IP
```

This is the most network-technical step in the guide.

If you already know how to make a local DNS override, use your preferred method.

If you do not, see:

**[`docs/BEGINNER_LOCAL_OTA.md`](docs/BEGINNER_LOCAL_OTA.md)**

That file explains what you are trying to achieve, how to recognize success, and what to check if the OBOOK never reaches your server.

> [!IMPORTANT]
> Do this only on a network and device you control.

---

## 6.3 Start the local update server

Open Windows PowerShell in the repository folder.

Example:

```powershell
python .\tools\ota_server.py `
  --host-ip 192.168.137.1 `
  --image C:\path\to\obook5-v1.4-owner-bridge.img `
  --version V1.4
```

Replace:

```text
192.168.137.1
```

with your PC's actual local address if different.

Replace:

```text
C:\path\to\obook5-v1.4-owner-bridge.img
```

with the actual image location.

Keep this PowerShell window open.

---

## 6.4 Trigger the update on the OBOOK

On the OBOOK:

1. connect to the controlled Wi-Fi network;
2. open the normal system update screen;
3. choose **Check upgrade**;
4. look at the PowerShell window on the PC.

You want the PC console to show that the OBOOK requested:

```text
/readerapi.aspx
```

If you see that request, the OBOOK is talking to your local server.

Accept the update offered on the OBOOK.

Let the OBOOK install it and reboot.

Do not unplug or power it off while the update is being installed.

---

# 7. Verify that the owner bridge works

Connect the OBOOK to the PC over USB.

You should see its normal internal storage.

The owner bridge uses the root of that storage.

To test the bridge, copy:

```text
device/ENABLE_OBOOK_STARTUP
```

to the root.

You also need an `obook-startup.sh`.

For later installation steps, the supplied installer script becomes that file.

After a successful one-shot run:

```text
ENABLE_OBOOK_STARTUP
```

should disappear.

You may also see:

```text
obook-boot-hook.log
obook-startup.log
```

This confirms the bridge executed.

From this point onward, you should not normally need the OTA procedure again.

---

# 8. Get the two original OBOOK libraries

The mod changes two existing OBOOK libraries.

You should obtain the original versions from your own firmware.

## Easiest method: extract them from your official update image

Inside Ubuntu:

```bash
tar -xzf ~/obook-work/obook5-v1.3.img \
  -C ~/obook-work/unpacked
```

Now copy the two files:

```bash
cp \
  ~/obook-work/unpacked/image/opt/Qtopia/lib/libeinkfbreader.so.1.0.0 \
  ~/obook-work/stock/
```

and:

```bash
cp \
  ~/obook-work/unpacked/image/opt/Qtopia/lib/libdictionaryview.so.1.0.0 \
  ~/obook-work/stock/
```

---

## 8.1 Verify the first library

Run:

```bash
md5sum ~/obook-work/stock/libeinkfbreader.so.1.0.0
```

Expected:

```text
97f249f7a36b773582e78e80896e993b
```

---

## 8.2 Verify the second library

Run:

```bash
md5sum ~/obook-work/stock/libdictionaryview.so.1.0.0
```

Expected:

```text
e18ae4624cb2bdf1edc041f203757b5d
```

If either hash is different, stop.

---

# 9. Build the Dictionary button patch

This is the patch that changes the reader-side action so the built-in dictionary opens.

Inside the repository folder in Ubuntu, run:

```bash
python3 tools/apply_search_to_dictionary.py \
  ~/obook-work/stock/libeinkfbreader.so.1.0.0 \
  ~/obook-work/build/libeinkfbreader.dictionary.so.1.0.0
```

If everything is correct, the script should report success.

The new file should have MD5:

```text
86cd2535d141d13cb7abe4fd60746326
```

Check:

```bash
md5sum ~/obook-work/build/libeinkfbreader.dictionary.so.1.0.0
```

---

# 10. Copy the Dictionary patch to the OBOOK

Now return to Windows / File Explorer.

You need three files on the **root** of the OBOOK storage.

### File 1

Your newly created:

```text
libeinkfbreader.dictionary.so.1.0.0
```

### File 2

Take:

```text
device/install_search_to_dictionary.sh
```

and copy it to the OBOOK with this exact name:

```text
obook-startup.sh
```

### File 3

Copy:

```text
device/ENABLE_OBOOK_STARTUP
```

The OBOOK root should now contain:

```text
libeinkfbreader.dictionary.so.1.0.0
obook-startup.sh
ENABLE_OBOOK_STARTUP
```

Safely disconnect the USB cable.

Reboot the OBOOK.

The installer may cause one additional automatic reboot.

That is expected.

---

# 11. Test the Dictionary button

Open a book.

Long-press a word.

The long-press menu will still show:

```text
Search
```

That label does **not** change on the tested device.

Tap **Search**.

The built-in Dictionary app/window should open instead of the original in-book search behavior.

At this point, the dictionary may open without yet automatically using your selected word.

That is what the next patch fixes.

---

# 12. Build the automatic word-fill patch

Back in Ubuntu, run:

```bash
python3 tools/apply_autofill_v2.py \
  ~/obook-work/stock/libdictionaryview.so.1.0.0 \
  ~/obook-work/build/libdictionaryview.autofill-v2.so.1.0.0
```

Expected MD5:

```text
02ef37b7d69995475b8cf5406ed4b053
```

Verify:

```bash
md5sum ~/obook-work/build/libdictionaryview.autofill-v2.so.1.0.0
```

---

# 13. Copy the autofill patch to the OBOOK

Again, put three files on the OBOOK root.

### File 1

```text
libdictionaryview.autofill-v2.so.1.0.0
```

### File 2

Copy:

```text
device/install_autofill_v2.sh
```

to the OBOOK as:

```text
obook-startup.sh
```

### File 3

Copy:

```text
device/ENABLE_OBOOK_STARTUP
```

Safely disconnect USB.

Reboot.

Again, one extra automatic reboot may occur.

---

# 14. Test the completed mod

Open a book.

Try a simple word, for example:

```text
house
```

Then:

1. long-press `house`;
2. tap **Dictionary**;
3. wait for the dictionary window.

The expected result is:

```text
Dictionary window opens
        +
"house" is already entered
        +
search runs automatically
        +
a result appears
```

If that happens, the difficult part is finished.

You now have the complete firmware-side dictionary mod installed.

---

# 📚 Installing your own dictionaries

This part is much easier.

You do **not** need to patch the firmware again each time.

---

## 15. Understand the dictionary format

An OBOOK customer dictionary is a SQLite database.

It uses this table:

```sql
CREATE TABLE dict (
    word varchar (128) primary key,
    content varchar(255)
);
```

Think of it as a very simple two-column list:

```text
WORD       DEFINITION / TRANSLATION
house      casa; vivienda
book       libro
maison     casa; vivienda
bonjour    hola; buenos días
```

---

# 16. Make a tiny test dictionary

Before trying a huge dictionary, create a small one.

Create a file named:

```text
MyDictionary.csv
```

Put this inside:

```csv
word,content
house,casa; vivienda
book,libro
computer,computadora; ordenador
maison,casa; vivienda
bonjour,hola; buenos días
```

Save it as UTF-8.

---

# 17. Convert the CSV into an OBOOK `.dict`

Open PowerShell or Ubuntu in the repository folder.

Run:

```bash
python3 dictionary/convert_to_obook_dict.py \
  MyDictionary.csv \
  MyDictionary.dict
```

On Windows PowerShell you can also use:

```powershell
python .\dictionary\convert_to_obook_dict.py `
  .\MyDictionary.csv `
  .\MyDictionary.dict
```

You should now have:

```text
MyDictionary.dict
```

---

# 18. Check the dictionary before copying it

Run:

```bash
python3 dictionary/inspect_obook_dict.py MyDictionary.dict
```

You should see the database schema and entry count.

Test one word:

```bash
python3 dictionary/inspect_obook_dict.py \
  MyDictionary.dict \
  --word house
```

You want to see the `house` entry and its content.

If the PC cannot find the word, do not copy the database to the OBOOK yet.

Fix the dictionary source first.

---

# 19. Install the custom dictionary

Open:

```text
dictionary/install_and_select_dictionary_TEMPLATE.sh
```

in a text editor.

Near the top, find:

```sh
DICT_NAME="MyDictionary.dict"
```

Change the filename if your dictionary has another name.

For example:

```sh
DICT_NAME="French-Spanish.dict"
```

Save a copy of the edited file as:

```text
obook-startup.sh
```

Now copy these files to the root of the OBOOK:

```text
MyDictionary.dict
obook-startup.sh
dictionary/ENABLE_OBOOK_STARTUP
```

Reboot.

The script automatically:

1. creates the OBOOK dictionary folder if needed;
2. moves the large dictionary there;
3. creates the link expected by the original OBOOK software;
4. selects the dictionary;
5. reboots.

---

# 20. Where does the dictionary actually go?

The real large file is stored here:

```text
/user/OBOOK_DICTIONARIES/MyDictionary.dict
```

The original OBOOK software expects a dictionary under:

```text
/data/.词典/
```

But `/data` is small.

So the installer creates a Linux shortcut called a **symbolic link**:

```text
/data/.词典/MyDictionary.dict
        │
        └──────────────► /user/OBOOK_DICTIONARIES/MyDictionary.dict
```

The OBOOK software thinks the file is in `/data`, while the actual storage space is used from `/user`.

You do not normally need to manage this manually.

---

# 21. Switch to a dictionary that is already installed

Suppose these are already installed:

```text
English-Spanish.dict
French-Spanish.dict
Spanish-Spanish.dict
```

Open:

```text
dictionary/switch_dictionary_TEMPLATE.sh
```

Change:

```sh
DICT_NAME="MyDictionary.dict"
```

to:

```sh
DICT_NAME="French-Spanish.dict"
```

Save it as:

```text
obook-startup.sh
```

Copy to the OBOOK root:

```text
obook-startup.sh
ENABLE_OBOOK_STARTUP
```

Reboot.

You do not need to copy the large dictionary file again.

---

# 22. Combine several dictionaries into one

If you read English, French and Spanish, you may prefer one combined database.

Example:

```bash
python3 dictionary/merge_obook_dicts.py Combined.dict \
  EN=English-Spanish.dict \
  FR=French-Spanish.dict \
  ES=Spanish-Spanish.dict
```

Then install:

```text
Combined.dict
```

as your active dictionary.

This avoids manually switching every time the language changes.

---

# 23. I downloaded a `.dict` from the Internet. Can I use it?

Maybe.

The important thing to understand is:

> `.dict` is only a filename extension. It does not guarantee one specific format.

There are three common cases.

## Case 1 — already compatible

Run:

```bash
python3 dictionary/inspect_obook_dict.py Downloaded.dict
```

If it is SQLite and contains the expected:

```text
dict
word
content
```

it may work directly.

---

## Case 2 — SQLite, but uses different names

For example, another dictionary may contain:

```text
entries
headword
definition
```

That is easy to convert.

Conceptually:

```text
headword   → word
definition → content
```

---

## Case 3 — not SQLite at all

StarDict often contains:

```text
dictionary.ifo
dictionary.idx
dictionary.dict
```

That `.dict` is **not** the same format as this OBOOK `.dict`.

The general process is:

```text
original dictionary
       ↓
extract word + definition
       ↓
CSV / JSON / JSONL
       ↓
convert_to_obook_dict.py
       ↓
OBOOK-compatible SQLite .dict
```

The same idea applies to:

- StarDict;
- MDX / MDict;
- DSL;
- XML;
- another SQLite schema.

---

# 24. Why some plurals or conjugated words may not work

The OBOOK searches the text that you selected.

So if you select:

```text
maisons
```

the dictionary looks for:

```text
maisons
```

It may not automatically decide that the basic dictionary form is:

```text
maison
```

The database can solve this by including both:

```text
maison   → casa
maisons  → casas; plural of maison
```

For English verbs:

```text
go       → ir
goes     → ir
went     → ir
gone     → ir
going    → ir
```

This is why a good language-learning dictionary should ideally contain inflected forms or aliases.

---

# ♻️ Recovery

The installers make backups before replacing the original libraries.

Keep these files:

```text
/user/OBOOK_BACKUP_libeinkfbreader.so.1.0.0
/user/OBOOK_BACKUP_libdictionaryview.so.1.0.0
/home/rcS.pre-obook-tools.backup
```

Do not delete them just because the mod works.

---

## Restore the original reader library

Copy:

```text
device/restore_reader.sh
```

to the OBOOK root as:

```text
obook-startup.sh
```

Also copy:

```text
device/ENABLE_OBOOK_STARTUP
```

Reboot.

---

## Restore the original dictionary-view library

Copy:

```text
device/restore_autofill_v2.sh
```

to the OBOOK root as:

```text
obook-startup.sh
```

Copy the startup marker again.

Reboot.

---

# 🆘 Beginner troubleshooting

## "python is not recognized"

Python is missing from Windows or not in PATH.

Install Python 3, then reopen PowerShell.

---

## "The hash is different"

Stop.

Do not force the patch.

Your build is not the exact tested build.

---

## "The patch script says unsupported input MD5"

Same answer: stop.

The safety check is doing its job.

---

## "The OBOOK update screen does not contact my PC"

The local DNS/network override is not working yet.

Do not rebuild the firmware repeatedly.

First verify:

- OBOOK is connected to the correct Wi-Fi;
- the PC and OBOOK can reach each other;
- port 8085 is allowed through Windows Firewall;
- the update hostname resolves to the local PC;
- `ota_server.py` is still running.

See [`docs/BEGINNER_LOCAL_OTA.md`](docs/BEGINNER_LOCAL_OTA.md).

---

## "The Dictionary button appears, but I still have to type the word"

The first patch is installed, but the autofill patch is not.

Install the `libdictionaryview.autofill-v2` patch.

---

## "Dictionary opens, but my custom dictionary finds nothing"

First test it on the PC:

```bash
python3 dictionary/inspect_obook_dict.py MyDictionary.dict --word house
```

If the entry is not found on the PC either, the problem is in the dictionary data.

If it works on the PC, check that the correct dictionary is selected on the OBOOK.

---

## "I installed another `.dict` from the Internet and it does not work"

It may not be an OBOOK-format SQLite database.

Run:

```bash
python3 dictionary/inspect_obook_dict.py Downloaded.dict
```

If it says:

```text
file is not a database
```

the file uses a different dictionary format and must be converted first.

---

# 🔬 For technical readers

You do not need this section to install the mod.

The rough stock runtime stack is:

```text
bookreader
   │
   ├── libeinkfbreader.so
   │      reader selection action
   │
   ├── libdictionaryview.so
   │      dictionary UI + selected-word handoff
   │
   └── libdictionary.so
          dictionary backend
```

The reader patch leaves the visible **Search** label unchanged, but redirects that action so it calls the existing dictionary helper with the selected `QString`.

The autofill patch keeps the normal stock dictionary-window setup but changes the relevant handoff to the equivalent of:

```cpp
DictionaryView *view = getView();
view->setWord(selectedWord);

view = getView();
view->search();
```

Then the original fullscreen-display path continues.

More detail:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/TESTED_HASHES.md`](docs/TESTED_HASHES.md)

---

# 📜 What this repository intentionally does not contain

This project does not publish:

- official OBOOK firmware;
- extracted OBOOK `.so` libraries;
- pre-patched OBOOK proprietary binaries;
- partition dumps;
- private runtime logs;
- commercial dictionary databases;
- unrelated vulnerability-disclosure material.

The scripts and documentation authored for this repository are separate from vendor/third-party material.

See:

- [`NOTICE.md`](NOTICE.md)
- [`DISCLAIMER.md`](DISCLAIMER.md)
- [`docs/PUBLISHING_AND_IP.md`](docs/PUBLISHING_AND_IP.md)

---

# 🤝 Contributing

If you have another OBOOK5 firmware version, compatibility reports are welcome.

Please provide:

```text
Device:
Firmware version:
libeinkfbreader MD5:
libdictionaryview MD5:
Which step failed:
Relevant text log:
```

Please do **not** upload OBOOK firmware or proprietary OBOOK binaries to an issue.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

# Project status

```text
[x] Existing Search action redirected to the built-in Dictionary app
[x] Selected-word autofill
[x] Automatic lookup
[x] Custom SQLite dictionaries
[x] Dictionary switching
[x] Combined dictionaries
[x] Rollback scripts
[x] Beginner installation guide
[ ] More firmware revisions
[ ] On-device graphical dictionary selector
```

If your build matches the tested hashes, follow the steps in order and do not skip the verification stages.

# Beginner print checklist

Use this page as a short companion while following the main README.

## Before changing anything

- [ ] I have an OBOOK5.
- [ ] My firmware is the tested V1.3 build.
- [ ] Official image MD5 matches `8ced2385925ac03b0f6a82aa73a8e7bc`.
- [ ] Python works on Windows.
- [ ] Ubuntu/WSL works.
- [ ] `clang` and `llvm` are installed.
- [ ] My vendor firmware is stored outside the Git repository.

## Owner bridge

- [ ] Built `obook5-v1.4-owner-bridge.img`.
- [ ] Started `ota_server.py`.
- [ ] OBOOK update request appeared in the PC console.
- [ ] OBOOK installed the local bridge update.
- [ ] One-shot startup marker disappears after use.

## Search-action redirect

- [ ] Stock `libeinkfbreader` MD5 matches.
- [ ] Built patched library.
- [ ] Patched MD5 is `86cd2535d141d13cb7abe4fd60746326`.
- [ ] Copied patched library + `obook-startup.sh` + marker.
- [ ] Rebooted.
- [ ] Long-press menu still shows `Search`.
- [ ] Tapping `Search` now opens the stock Dictionary app.

## Autofill

- [ ] Stock `libdictionaryview` MD5 matches.
- [ ] Built autofill-v2.
- [ ] Patched MD5 is `02ef37b7d69995475b8cf5406ed4b053`.
- [ ] Copied autofill library + installer + marker.
- [ ] Rebooted.
- [ ] Selected word now appears automatically.
- [ ] Search runs automatically.

## Custom dictionary

- [ ] Created or converted `.dict`.
- [ ] `inspect_obook_dict.py` can find a test word.
- [ ] Edited `DICT_NAME`.
- [ ] Copied dictionary + startup script + marker.
- [ ] Rebooted.
- [ ] Test word works in a real book.

## Keep these backups

- [ ] `OBOOK_BACKUP_libeinkfbreader.so.1.0.0`
- [ ] `OBOOK_BACKUP_libdictionaryview.so.1.0.0`
- [ ] `rcS.pre-obook-tools.backup`

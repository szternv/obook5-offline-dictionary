# Tested target and hashes

These values identify the exact build used to validate the public patchers.

| File / target | MD5 |
|---|---|
| Official OBOOK5 V1.3 OTA image | `8ced2385925ac03b0f6a82aa73a8e7bc` |
| Stock `libeinkfbreader.so.1.0.0` | `97f249f7a36b773582e78e80896e993b` |
| Patched Search -> Dictionary reader | `86cd2535d141d13cb7abe4fd60746326` |
| Stock `libdictionaryview.so.1.0.0` | `e18ae4624cb2bdf1edc041f203757b5d` |
| Patched autofill-v2 dictionary view | `02ef37b7d69995475b8cf5406ed4b053` |

Target:

```text
Device: OBOOK5
Model/board: epd86s2e
Official base: V1.3
SoC: Ingenic X2000
CPU: little-endian MIPS32r2
```

## Rule

If a stock input hash differs, **do not bypass the check**. Treat that firmware
as a separate reverse-engineering target.

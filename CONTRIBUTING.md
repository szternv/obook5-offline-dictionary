# Contributing

Thanks for helping improve OBOOK5 dictionary support.

The main goal is to add compatibility and improve documentation **without
redistributing vendor-owned files**.

## Good contributions

- compatibility information for another firmware build;
- new hash-locked patch profiles;
- improvements to the patch builders;
- better dictionary converters;
- additional open-data importers;
- safer recovery checks;
- documentation fixes;
- reproducible bug reports.

## Please do not submit

- OBOOK firmware images;
- extracted OBOOK executables or `.so` files;
- pre-patched proprietary libraries;
- filesystem/partition dumps;
- commercial dictionary databases;
- logs containing personal identifiers or credentials.

## Compatibility reports

Please include:

```text
Device/model:
Firmware version:
Stock libeinkfbreader MD5:
Stock libdictionaryview MD5:
Expected result:
Actual result:
Relevant text log:
```

If the hashes differ from the tested build, do not disable the patcher's guard.
A new build should receive its own analyzed offsets and expected output hashes.

## Code changes

Before submitting changes:

```bash
python3 -m py_compile tools/*.py dictionary/*.py
bash -n device/*.sh dictionary/*.sh
```

When changing a binary patcher, test both:

1. a known-supported input, which must produce the expected output hash;
2. a deliberately unsupported input, which must be rejected.

## Dictionary importers

When adding support for a third-party dataset or format:

- keep the generic converter separate from the dataset itself;
- document the original source;
- document the dataset's license;
- do not bundle a dataset unless redistribution is clearly permitted.

## Scope

This project is for interoperability and modification of devices the user owns
or is authorized to modify. Keep unrelated security research and vulnerability
disclosure out of public issues for this project.

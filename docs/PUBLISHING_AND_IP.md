# Publishing / IP hygiene

This file is a practical checklist, not legal advice.

## Good things to publish

- original Python patch/build scripts;
- original shell scripts;
- original MIPS hook source;
- hashes and offsets needed for compatibility checks;
- documentation of the interoperability behavior;
- tools that transform a user's own local firmware/libraries;
- dictionary conversion tools;
- small synthetic/example dictionary data you wrote yourself.

## Keep out of the repository by default

- the official firmware `.img`;
- extracted vendor `.so` files;
- pre-patched vendor `.so` files;
- full filesystem/partition dumps;
- vendor recovery packages you do not have redistribution permission for;
- proprietary dictionary databases;
- personal/private logs;
- unrelated vulnerability notes.

## Dictionary data

Treat dictionary data as a separate licensing problem.

If you later add Wiktionary/Kaikki/Apertium-derived databases, include the
appropriate source attribution and comply with the relevant license. Do not
assume that because the converter is MIT-licensed, every generated dictionary
can be redistributed under MIT.

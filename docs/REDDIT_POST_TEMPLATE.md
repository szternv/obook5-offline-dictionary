# Optional Reddit post template

**Title:** I enabled selected-word offline dictionaries on the OBOOK5 — public tools + guide

I spent some time reverse-engineering my OBOOK5 and found that the firmware
already contains a working dictionary stack, but the reader-side integration
does not expose it properly.

I now have the following flow working on my device:

`long-press word → Search → Dictionary app opens → selected word autofills → result`

I cleaned up the successful procedure into a public repository. It does **not**
contain OBOOK firmware or proprietary binaries: the scripts only patch files
that each owner extracts from their own exact compatible firmware.

The repo includes:

- one-time owner bootstrap;
- Search-action redirect patch builder;
- selected-word autofill patch builder;
- safe install/rollback scripts;
- SQLite `.dict` converter/inspector;
- custom dictionary installer;
- multi-dictionary merger;
- a full PDF walkthrough.

The currently tested target is the OBOOK5 `epd86s2e` V1.3 build, and the tools
refuse unknown hashes.

If anyone has another firmware revision and is comfortable checking hashes /
doing static analysis, compatibility reports would be useful.

**Please do not post or upload vendor firmware/binaries in the thread.**

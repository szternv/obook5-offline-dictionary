# Recovery

The installers save stock-library backups under `/user`.

Expected backups:

```text
/user/OBOOK_BACKUP_libeinkfbreader.so.1.0.0
/user/OBOOK_BACKUP_libdictionaryview.so.1.0.0
/home/rcS.pre-obook-tools.backup
```

## Restore reader library

Copy `device/restore_reader.sh` to the OBOOK root as `obook-startup.sh`, copy
`device/ENABLE_OBOOK_STARTUP`, then reboot.

## Restore dictionary-view library

Copy `device/restore_autofill_v2.sh` to the OBOOK root as
`obook-startup.sh`, copy the marker, then reboot.

The marker is deleted before the startup script is run, which avoids automatic
re-execution on every boot.

If the device no longer reaches normal boot or exposes user storage, stop.
Low-level BootROM/partition flashing is intentionally outside the public
dictionary-mod procedure.

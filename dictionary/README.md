# Dictionary tools

Once the firmware-side mod is installed, custom dictionaries are just SQLite
databases.

## Required schema

```sql
CREATE TABLE dict (
    word varchar (128) primary key,
    content varchar(255)
);
```

## Quick example

```bash
python3 convert_to_obook_dict.py example_dictionary.csv Example.dict
python3 inspect_obook_dict.py Example.dict
```

## Included tools

| File | Purpose |
|---|---|
| `convert_to_obook_dict.py` | CSV / TSV / JSON / JSONL → OBOOK `.dict` |
| `inspect_obook_dict.py` | Validate and inspect a database |
| `merge_obook_dicts.py` | Merge several compatible databases |
| `install_and_select_dictionary_TEMPLATE.sh` | Install and select a new database |
| `switch_dictionary_TEMPLATE.sh` | Select an already-installed database |
| `example_dictionary.csv` | Tiny synthetic example |

A random file named `.dict` is not necessarily compatible. See
[`../docs/DICTIONARY_FORMAT.md`](../docs/DICTIONARY_FORMAT.md).

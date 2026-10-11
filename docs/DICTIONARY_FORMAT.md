# OBOOK5 customer dictionary format

A compatible customer dictionary is a SQLite 3 database containing:

```sql
CREATE TABLE dict (
    word varchar (128) primary key,
    content varchar(255)
);
```

Example rows:

```text
house    casa; vivienda
book     libro
maison   casa; vivienda
```

`content` may contain simple HTML-like markup such as `<b>`, `<i>` and `<br>`.

## Storage

Large databases are kept in:

```text
/user/OBOOK_DICTIONARIES/
```

The stock software is pointed to a symlink under:

```text
/data/.词典/
```

The active selection is stored in:

```text
/home/Settings/dictionary.conf
```

## Pre-existing `.dict` files

The `.dict` extension alone does not imply compatibility.

- SQLite + table `dict(word, content)`: potentially direct.
- SQLite with another schema: convert the relevant columns.
- StarDict `.dict`: not the same format; extract headword/definition first.
- MDX/DSL/XML/etc.: parse/export headword + definition, then build the OBOOK
  SQLite database.

Use `dictionary/inspect_obook_dict.py` before installing.

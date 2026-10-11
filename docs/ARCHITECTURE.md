# Architecture notes

## Runtime stack

The tested reader process is `bookreader`. It dynamically loads, among other
libraries:

```text
libeinkfbreader.so.1.0.0
libdictionaryview.so.1.0.0
libdictionary.so.1
```

Conceptually:

```text
bookreader
  |
  +-- libeinkfbreader
  |     reader UI / selection actions
  |
  +-- libdictionaryview
  |     DictFetchScrWord / DictionaryView
  |
  +-- libdictionary
        dictionary backend
```

## Search-action redirect patch

The tested reader handler is replaced with a small MIPS32r2 PIC hook that
creates/reuses a `DictFetchScrWord` object and calls:

```cpp
searchWord(selectedQString)
```

The visible long-press menu label remains **Search** on the tested device. The patch redirects the behavior behind that existing action so it opens the stock Dictionary app.

The patch builder verifies the exact input hash and exact expected output hash.

## Selected-word autofill

In the tested build, `searchWord(selectedQString)` reaches the dictionary view,
but the stock `fetchWord(QString const&)` implementation does not populate the
word as intended.

The validated minimal modification preserves the stock `searchWord()` setup and
changes the relevant calls to the equivalent of:

```cpp
getView();
setWord(selectedQString);
getView();
search();
```

then continues through the original stock fullscreen path.

## Why this repository uses patch builders

The project does not need to redistribute vendor binaries. Each owner extracts
the exact stock libraries from their own legitimate firmware/device and the
scripts transform those local files only when their hashes match the tested
build.

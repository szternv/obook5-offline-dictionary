# Observed UI behavior

On the physically tested OBOOK5, the long-press selection menu continues to show:

```text
Note | Mark | Search
```

The mod does **not** rename the visible `Search` label.

Instead, it redirects the behavior behind that action:

```text
long-press word
    ↓
tap Search
    ↓
stock Dictionary app opens
    ↓
selected word is inserted automatically
    ↓
lookup runs automatically
    ↓
result is displayed
```

This distinction is intentional in the documentation so users know exactly what
they should expect on the device.

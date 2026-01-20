# fasthtml-htmxv4-patch

Small helpers to use `htmx` v4 (alpha) with `python-fasthtml`.

## Install (editable)

```bash
python -m pip install -e ./fasthtml_htmxv4_patch
```

## Use

```python
from fasthtml.common import *
from fasthtml_htmxv4_patch import *

app, rt = fast_app_v4(..., hdrs=[...])
```


"""`fasthtml` helpers for `htmx` v4 (alpha)

This is a tiny "patch" module so each project can migrate from htmx v2 → v4 by
adding a single import.

Typical usage (per app/module)
------------------------------

>>> from fasthtml.common import *
>>> from fasthtml_htmxv4_patch import *

Then either:

- Use `fast_app_v4(...)` (recommended): defaults to `htmx=False` and appends the
  required header tags.
- Or manually add `meta_cfg`, `fhjsscr`, `htmx_v4` to your `hdrs=` and set
  `htmx=False`.
"""

import json

from fastcore.meta import delegates
from fasthtml.common import Meta, Script, fast_app, fhjsscr, ft_hx

HTMX_V4_SRC = "https://unpkg.com/htmx.org@4.0.0-alpha4/dist/htmx.js"
DEFAULT_HTMX_V4_CONFIG = {"metaCharacter": "-"}


@delegates(ft_hx)
def Partial(*args, **kwargs): return ft_hx("hx-partial")(*args, **kwargs)


htmx_v4 = Script(src=HTMX_V4_SRC)
meta_cfg = Meta(name="htmx:config", content=json.dumps(DEFAULT_HTMX_V4_CONFIG))
htmx_v4_hdrs = (meta_cfg, fhjsscr, htmx_v4)


def fast_app_v4(*args, htmx=False, hdrs=None, **kwargs):
    """`fast_app` with `htmx=False` + v4 header tags added to `hdrs=`."""
    if hdrs is None: hdrs = []
    elif isinstance(hdrs, (list, tuple)): hdrs = list(hdrs)
    else: hdrs = [hdrs]
    hdrs += list(htmx_v4_hdrs)
    return fast_app(*args, htmx=htmx, hdrs=hdrs, **kwargs)
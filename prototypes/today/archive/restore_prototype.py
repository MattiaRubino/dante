#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = sorted(HERE.glob("lifeos-home-oggi-v7.html.gz.b64.part*"))
if not PARTS:
    raise SystemExit("Archive parts not found")

payload = "".join(part.read_text(encoding="ascii").strip() for part in PARTS)
compressed = base64.b64decode(payload)
html = gzip.decompress(compressed)
out = HERE.parent / "lifeos-home-oggi-v7.html"
out.write_bytes(html)
print(f"Restored: {out}")

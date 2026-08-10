from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "lifeos-home-shell-v11.html"
EXPECTED_SHA256 = "d21e54fce4f6417149b2b86e26bd2f3229581b716d6440459702add9c4f17c19"

parts = sorted(HERE.glob("lifeos-home-shell-v11.html.gz.b64.part*"))
if not parts:
    raise SystemExit("No archive parts found")

encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
payload = gzip.decompress(base64.b64decode(encoded))
actual = hashlib.sha256(payload).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f"SHA-256 mismatch: {actual}")

OUT.write_bytes(payload)
print(f"Restored {OUT}")
print(f"SHA-256 {actual}")

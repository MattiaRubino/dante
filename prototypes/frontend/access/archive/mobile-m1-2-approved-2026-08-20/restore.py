from __future__ import annotations

import base64
import hashlib
import lzma
from pathlib import Path

EXPECTED_SHA256 = "2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676"
EXPECTED_SIZE = 107010
ROOT = Path(__file__).resolve().parent
parts = sorted(ROOT.glob("part-*.b64"))
if not parts:
    raise SystemExit("No archive parts found")
encoded = b"".join(p.read_bytes().strip() for p in parts)
compressed = base64.b64decode(encoded, validate=True)
html = lzma.decompress(compressed, format=lzma.FORMAT_XZ)
sha = hashlib.sha256(html).hexdigest()
if len(html) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
    raise SystemExit(f"Integrity mismatch: size={len(html)} sha256={sha}")
out = ROOT / "dante-access-mobile-m1-2-prg0-approved.html"
out.write_bytes(html)
print(f"OK {out.name} {len(html)} bytes {sha}")

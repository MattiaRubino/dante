from __future__ import annotations

import base64
import gzip
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "v8_fragment.html.gz.b64"
BASE_SHA256 = "5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56"
FINAL_SHA256 = "473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f"
FINAL_SIZE = 307487
ANCHOR = "</body></html>\n<style>\n.center-copy{display:none!important}\n.label{display:none!important}\n"

base_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "lifeos_home_vnext_soft_surfaces.html"
base = base_path.read_bytes()
base_sha = hashlib.sha256(base).hexdigest()
if base_sha != BASE_SHA256:
    raise SystemExit(f"base SHA-256 mismatch: {base_sha} != {BASE_SHA256}")
fragment = gzip.decompress(base64.b64decode(PAYLOAD.read_text(encoding="ascii"))).decode("utf-8")
text = base.decode("utf-8")
if text.count(ANCHOR) != 1:
    raise SystemExit(f"expected one restore anchor, found {text.count(ANCHOR)}")
restored = text.replace(ANCHOR, fragment + ANCHOR, 1).encode("utf-8")
sha = hashlib.sha256(restored).hexdigest()
if sha != FINAL_SHA256:
    raise SystemExit(f"final SHA-256 mismatch: {sha} != {FINAL_SHA256}")
if len(restored) != FINAL_SIZE:
    raise SystemExit(f"final size mismatch: {len(restored)} != {FINAL_SIZE}")
out = ROOT / "lifeos_home_timeline_toolbar_verified_v8.html"
out.write_bytes(restored)
print(f"restored {out.name}: {len(restored)} bytes, sha256={sha}")

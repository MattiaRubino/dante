"""Rebuild LifeOS Home/Today v21 from a verified v20 HTML file.

Usage:
    python restore_v21.py /path/to/LifeOS_Home_Oggi_v20_canvas.html [output.html]
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "86b5bc051520fa1d7ce5415ea2940c3bd1832b3735a4d0232745ed84b15bb0fb"
ARCHIVE = Path(__file__).with_name("lifeos-v20-to-v21.patch.gz.b64")
DEFAULT_OUTPUT = "LifeOS_Home_Oggi_v21_canvas.html"


def main() -> int:
    if len(sys.argv) not in (2, 3):
        raise SystemExit("Pass the v20 HTML path and, optionally, the output path.")
    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit(f"v20 source not found: {source}")
    output = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else Path.cwd() / DEFAULT_OUTPUT
    patch_bytes = gzip.decompress(base64.b64decode(ARCHIVE.read_text(encoding="ascii")))
    with tempfile.NamedTemporaryFile(suffix=".patch", delete=False) as handle:
        handle.write(patch_bytes)
        patch_path = Path(handle.name)
    try:
        subprocess.run(
            ["patch", "--silent", "--output", str(output), str(source), str(patch_path)],
            check=True,
        )
    finally:
        patch_path.unlink(missing_ok=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        output.unlink(missing_ok=True)
        raise SystemExit(f"SHA-256 mismatch: {digest}")
    print(f"Restored {output} ({digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

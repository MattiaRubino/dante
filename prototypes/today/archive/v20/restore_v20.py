"""Rebuild LifeOS Home/Today v20 from the verified v19 HTML.

Usage:
    python restore_v20.py /path/to/LifeOS_Home_Oggi_v19_canvas_verified.html
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "e1144fa16e4f94c1afdc1074dbe8750696fc2197517c1dfeddebaa5c247e5c37"
ARCHIVE = Path(__file__).with_name("lifeos-v19-to-v20.patch.gz.b64")
OUTPUT_NAME = "LifeOS_Home_Oggi_v20_canvas.html"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Pass the verified v19 HTML path.")

    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit(f"v19 source not found: {source}")

    output = Path.cwd() / OUTPUT_NAME
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

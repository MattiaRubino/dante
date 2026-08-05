"""Rebuild LifeOS Home/Today v18 from a restored v17 HTML file.

Usage:
    python prototypes/today/archive/v18/restore_v18.py \
        /path/to/LifeOS_Home_Oggi_v17_canvas_verified.html

The script decodes the archived unified diff, applies it, writes
`LifeOS_Home_Oggi_v18_canvas.html`, and verifies the expected SHA-256.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "b0eb870de16ea862bd707b49fd4fcaf7939151abe3e1b4c2b287a37ee5ef186b"
ARCHIVE = Path(__file__).with_name("lifeos-v17-to-v18.patch.gz.b64")
OUTPUT_NAME = "LifeOS_Home_Oggi_v18_canvas.html"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Pass the path to the restored v17 HTML file.")

    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit(f"v17 source not found: {source}")

    output = Path.cwd() / OUTPUT_NAME
    output.write_bytes(source.read_bytes())

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

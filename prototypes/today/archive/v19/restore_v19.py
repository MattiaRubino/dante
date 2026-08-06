"""Rebuild LifeOS Home/Today v19 from the verified v18 HTML file.

Usage:
    python prototypes/today/archive/v19/restore_v19.py \
        /path/to/LifeOS_Home_Oggi_v18_canvas_verified.html

The script decodes the archived unified diff, applies it, writes
`LifeOS_Home_Oggi_v19_canvas.html`, and verifies both input and output SHA-256.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_SHA256 = "b0eb870de16ea862bd707b49fd4fcaf7939151abe3e1b4c2b287a37ee5ef186b"
EXPECTED_SHA256 = "9fb2fc551b7675a42813544c52b490e1ac973d60bc7547ed16d0c62f1b5a1000"
ARCHIVE = Path(__file__).with_name("lifeos-v18-to-v19.patch.gz.b64")
OUTPUT_NAME = "LifeOS_Home_Oggi_v19_canvas.html"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Pass the path to the verified v18 HTML file.")

    source = Path(sys.argv[1]).resolve()
    if not source.is_file():
        raise SystemExit(f"v18 source not found: {source}")
    source_digest = sha256(source)
    if source_digest != SOURCE_SHA256:
        raise SystemExit(f"Unexpected v18 SHA-256: {source_digest}")

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

    digest = sha256(output)
    if digest != EXPECTED_SHA256:
        output.unlink(missing_ok=True)
        raise SystemExit(f"v19 SHA-256 mismatch: {digest}")

    print(f"Restored {output} ({digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

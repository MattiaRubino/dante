from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PART_GLOB = "home-today-integrated-v1.html.gz.b64.part*"
OUTPUT = ROOT / "home-today-integrated-v1.html"
EXPECTED_SHA256 = "66f1f8af4795aa579394ec07bc872798141907c6c216f5af0daed4f96e5c32b4"


def main() -> None:
    parts = sorted(ROOT.glob(PART_GLOB))
    if not parts:
        raise SystemExit(f"No archive parts found matching {PART_GLOB}")

    encoded = b"".join(part.read_bytes().strip() for part in parts)
    compressed = base64.b64decode(encoded, validate=True)
    html = gzip.decompress(compressed)

    digest = hashlib.sha256(html).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"SHA-256 mismatch: expected {EXPECTED_SHA256}, got {digest}"
        )

    OUTPUT.write_bytes(html)
    print(f"Restored: {OUTPUT}")
    print(f"SHA-256: {digest}")


if __name__ == "__main__":
    main()

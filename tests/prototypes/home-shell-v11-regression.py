from __future__ import annotations

import base64
import gzip
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "prototypes" / "home" / "archive" / "v11"
EXPECTED_SHA256 = "d21e54fce4f6417149b2b86e26bd2f3229581b716d6440459702add9c4f17c19"

parts = sorted(ARCHIVE.glob("lifeos-home-shell-v11.html.gz.b64.part*"))
assert parts, "Home Shell v11 archive parts are missing"
html_bytes = gzip.decompress(base64.b64decode("".join(p.read_text().strip() for p in parts)))
assert hashlib.sha256(html_bytes).hexdigest() == EXPECTED_SHA256
html = html_bytes.decode("utf-8")

required = [
    'class="tb-create tb-create-main"',
    'class="tb-search tb-search-right"',
    'id="stageHub"',
    'aria-label="Assistente LifeOS"',
    'class="ai-thread"',
    'data-open-pop="create"',
    'data-open-pop="search"',
    'stage-surface-label',
    'dock-mode-arrow',
    'hero-home-clean',
]
for marker in required:
    assert marker in html, f"Missing marker: {marker}"

assert "stats-stage" in html
assert "stat-card" in html

print("Home Shell v11 archive/hash/required-markers: PASS")

#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, hashlib, sys

EXPECTED_BASE_SHA = "473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f"
EXPECTED_FRAGMENT_SHA = "f79c603823ba34cc2ef5a52e8545fc97234cef1ff1879e6949f188e6aff12815"
EXPECTED_FULL_SHA = "a45d1f2b5fab677d738306154a93697e497ffb2c8b2e36ddbba4f4289b42cc77"
EXPECTED_FULL_SIZE = 344559

here = Path(__file__).resolve().parent
if len(sys.argv) < 2:
    raise SystemExit("usage: restore_v23.py /path/to/lifeos_home_timeline_toolbar_verified_v8.html [output.html]")
base = Path(sys.argv[1])
out = Path(sys.argv[2]) if len(sys.argv) > 2 else here / "lifeos_home_v8_world_stats_switch_contextual_v23_safe_mid_divider.html"
base_bytes = base.read_bytes()
if hashlib.sha256(base_bytes).hexdigest() != EXPECTED_BASE_SHA:
    raise SystemExit("base SHA mismatch")
fragment = gzip.decompress(base64.b64decode((here / "v23_fragment.html.gz.b64").read_text().strip()))
if hashlib.sha256(fragment).hexdigest() != EXPECTED_FRAGMENT_SHA:
    raise SystemExit("fragment SHA mismatch")
full = base_bytes + fragment
if len(full) != EXPECTED_FULL_SIZE or hashlib.sha256(full).hexdigest() != EXPECTED_FULL_SHA:
    raise SystemExit("restored artifact mismatch")
out.write_bytes(full)
print(out)
print(EXPECTED_FULL_SHA)

from pathlib import Path
import base64, hashlib

HERE = Path(__file__).resolve().parent
PARTS = [
    "dante-home-cosmos-mirrored-v1.webp.b64.part00",
    "dante-home-cosmos-mirrored-v1.webp.b64.part01",
    "dante-home-cosmos-mirrored-v1.webp.b64.part02",
    "dante-home-cosmos-mirrored-v1.webp.b64.part03a",
    "dante-home-cosmos-mirrored-v1.webp.b64.part03b",
    "dante-home-cosmos-mirrored-v1.webp.b64.part04a",
    "dante-home-cosmos-mirrored-v1.webp.b64.part04b",
    "dante-home-cosmos-mirrored-v1.webp.b64.part05a",
    "dante-home-cosmos-mirrored-v1.webp.b64.part05b",
]
EXPECTED_SIZE = 37482
EXPECTED_SHA256 = "8ce54b557e7e1cd436ecd6ac672491e619bc61111788b9b0551eeef257f74002"
OUT = HERE / "dante-home-cosmos-mirrored-v1.webp"

payload = "".join((HERE / name).read_text(encoding="ascii") for name in PARTS)
data = base64.b64decode(payload, validate=True)
sha = hashlib.sha256(data).hexdigest()
if len(data) != EXPECTED_SIZE or sha != EXPECTED_SHA256:
    raise SystemExit(f"refusing restore: size={len(data)} sha256={sha}")
OUT.write_bytes(data)
print(f"restored {OUT.name}: {len(data)} bytes sha256={sha}")

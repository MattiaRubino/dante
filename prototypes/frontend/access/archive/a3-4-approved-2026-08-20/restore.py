from pathlib import Path
import base64, hashlib, lzma

ROOT = Path(__file__).resolve().parent
EXPECTED_XZ = "923f97e10103ca27115433f7004c93134ce579fdedb5a91d28c4ac35a91cf146"
EXPECTED_HTML = "b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6"
OUT = ROOT / "dante-access-a3-4-corner-mark-strong-review.html"

encoded = "".join(p.read_text(encoding="ascii").strip() for p in sorted(ROOT.glob("part-*.b64")))
payload = base64.b64decode(encoded)
if hashlib.sha256(payload).hexdigest() != EXPECTED_XZ:
    raise SystemExit("XZ SHA-256 mismatch")
html = lzma.decompress(payload, format=lzma.FORMAT_XZ)
if hashlib.sha256(html).hexdigest() != EXPECTED_HTML:
    raise SystemExit("HTML SHA-256 mismatch")
OUT.write_bytes(html)
print(OUT)
print(EXPECTED_HTML)

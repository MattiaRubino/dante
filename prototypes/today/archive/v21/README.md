# LifeOS Home/Today v21 archive

The exact v21 standalone prototype is preserved as a deterministic patch from the verified v20 milestone.

## Restore

```bash
python prototypes/today/archive/v21/restore_v21.py \
  /path/to/LifeOS_Home_Oggi_v20_canvas.html
```

Expected output hash:

```text
SHA-256 86b5bc051520fa1d7ce5415ea2940c3bd1832b3735a4d0232745ed84b15bb0fb
```

## Contents

- `lifeos-v20-to-v21.patch.gz.b64`: compressed and Base64-encoded unified diff;
- `restore_v21.py`: decoder, patch application and integrity verification.

The v21 change replaces the card-inline time editor with an anchored, body-level time picker using segmented hour/minute spin controls. The picker does not alter card geometry while open.

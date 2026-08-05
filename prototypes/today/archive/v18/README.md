# LifeOS Home/Today v18 archive

The exact v18 prototype is preserved as a deterministic patch from the v17 milestone.

## Restore

1. Rebuild or obtain the verified v17 HTML file.
2. Run:

```bash
python prototypes/today/archive/v18/restore_v18.py \
  /path/to/LifeOS_Home_Oggi_v17_canvas_verified.html
```

The command creates `LifeOS_Home_Oggi_v18_canvas.html` in the current directory and verifies:

```text
SHA-256 b0eb870de16ea862bd707b49fd4fcaf7939151abe3e1b4c2b287a37ee5ef186b
```

## Contents

- `lifeos-v17-to-v18.patch.gz.b64`: gzip-compressed unified diff encoded as Base64.
- `restore_v18.py`: decoder, patch applicator, and integrity check.

The uncompressed interactive artifact is also distributed in the associated ChatGPT project conversation.

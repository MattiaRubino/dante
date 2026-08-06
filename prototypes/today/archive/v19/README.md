# LifeOS Home/Today v19 archive

The exact v19 prototype is preserved as a deterministic patch from the verified v18 milestone.

## Restore

1. Obtain the verified v18 HTML file with SHA-256:

```text
b0eb870de16ea862bd707b49fd4fcaf7939151abe3e1b4c2b287a37ee5ef186b
```

2. Run from the repository root:

```bash
python prototypes/today/archive/v19/restore_v19.py \
  /path/to/LifeOS_Home_Oggi_v18_canvas_verified.html
```

The command creates `LifeOS_Home_Oggi_v19_canvas.html` in the current directory and verifies:

```text
SHA-256 9fb2fc551b7675a42813544c52b490e1ac973d60bc7547ed16d0c62f1b5a1000
```

## Contents

- `lifeos-v18-to-v19.patch.gz.b64`: gzip-compressed unified diff encoded as Base64.
- `restore_v19.py`: input validation, decoder, patch applicator, and output integrity check.

The interactive artifact is also distributed in the associated ChatGPT project conversation.

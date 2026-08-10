# Home Shell v11 archive

Accepted Phase 4 Home shell checkpoint frozen on 2026-08-10 before integration of the full Today v21 timeline engine.

## Restore

From repository root:

```bash
python prototypes/home/archive/v11/restore_v11.py
```

The script joins the `.partXX` files, base64-decodes them, gunzips the payload and writes:

```text
prototypes/home/archive/v11/lifeos-home-shell-v11.html
```

Expected SHA-256:

```text
d21e54fce4f6417149b2b86e26bd2f3229581b716d6440459702add9c4f17c19
```

Design/behavior documentation: `docs/phase-4/home-shell-v11.md`.

# Home vNext Timeline Toolbar v8 archive

This directory preserves the exact user-approved working HTML checkpoint from 2026-08-16 as a deterministic delta over the previous `home-vnext-soft-surfaces-v1` checkpoint.

Final artifact:

- `lifeos_home_timeline_toolbar_verified_v8.html`
- size: `307487` bytes
- SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`

Delta payload:

- `v8_fragment.html.gz.b64`
- decoded fragment size: `9615` bytes
- decoded fragment SHA-256: `dd1b81859548eaa3c299ef8db903e0f26c9f69b30b8c68635b100bed29e834bd`

Restore prerequisite:

Restore the previous exact checkpoint first so that `lifeos_home_vnext_soft_surfaces.html` is available. Its SHA-256 must be:

`5c38d9a9ed17f0ea950f23f21cf84928b00c4bdfa9fac694bdb282a52373fd56`

Then run:

```bash
python restore_v8.py /path/to/lifeos_home_vnext_soft_surfaces.html
```

The script inserts the verified delta at a unique structural anchor and checks the final size/SHA-256.

This is a coded UX prototype checkpoint, not production React code. See `docs/phase-4/home-vnext-timeline-toolbar-v8.md` and `docs/phase-4/frontend-architecture-handoff-2026-08-16.md`.

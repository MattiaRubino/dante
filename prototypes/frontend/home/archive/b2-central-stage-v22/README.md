# B2 Central Stage v22 — no persistent add working baseline

This archive preserves the user-reviewed B2 v22 working state from 2026-08-21.

Base working oracle: B2 v21 responsive.

```text
v21 FULL SHA-256     b653b5455903d0978cae88ff76fb74c285d0104334871cdb9f406f6d945c4cde
v21 PARTIAL SHA-256  390f12cf6c327be27342dcc038d398fd2751c3e2a9cbab3fbf2d981092405763

v22 FULL SHA-256     18e1ae3d6558164975c8783f24a8f86051be57daeb9093661e1c5ee6a9fe6f76
v22 PARTIAL SHA-256  f6ee524db98a799c81fa2c704e751e34af3d1e02482f72eb006b20630ef1ada3
```

v22 removes persistent/add-slot affordances from Home. Partial Mondi renders only real items. Full/overflow remains normal projection navigation. Empty state may expose a contextual entry into a dedicated management surface; Home itself does not perform configuration CRUD.

The patch artifacts use marker `DANTE_GZIP_BASE64_UNIFIED_DIFF_V1` and are unified diffs from the saved v21 previews, gzip-compressed deterministically (`mtime=0`) and Base64 encoded.

Patch payload SHA-256:

```text
full-v21-to-v22.patch.gz.b64
66303e62d5ae6926951f57856810b625cfe2171daebdfc561c1ab3fdf0e1f032

partial-v21-to-v22.patch.gz.b64
ebaee7eb9a25a1584b8d50b5397b2476c840e7d7650ede07c1b4111867985fcc
```

Exact semantics and QA qualification are recorded in `docs/frontend/home/checkpoints/b2-central-stage-v22-no-persistent-add.md`.

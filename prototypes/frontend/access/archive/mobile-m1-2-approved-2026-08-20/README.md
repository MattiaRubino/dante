# DANTE Access Mobile M1.2 + PRG-0 — approved archive

Status: **APPROVED MOBILE REVIEW ORACLE / PRODUCTION-READY SPECIFICATION / PRE-IMPLEMENTATION**  
Date: **2026-08-20**

## Exact artifact

```text
name       dante-access-mobile-m1-2-prg0-approved.html
size       107010 bytes
SHA-256    2ae752ec0598d76f93eb0d7521d30340e7f673dd4d921c7263deb6c526a81676
```

The standalone HTML is stored as XZ → Base64 chunks only because the repository connector used during review has a payload-size limit. This transport representation is not a different build.

Compressed identity:

```text
XZ size      21316 bytes
XZ SHA-256   1c27aef77b33f8ea3a05ea05cd1c14508848f6049f2f2ed34cf8b8d83b36fc91
Base64       28424 bytes
parts        6
```

## Restore

```bash
python restore.py
```

`restore.py` concatenates `part-*.b64`, Base64-decodes, XZ-decompresses and refuses to write the artifact unless both expected byte size and SHA-256 match.

## QA

- immediately preceding M1.2 executable Chromium suite: **30/30 PASS**;
- final PRG-0 deterministic static/mechanical suite: **18/18 PASS**;
- final PRG-0 Chromium rerun: **not claimed** because the execution environment blocked local-file and localhost navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`;
- real iOS/Android/backend release gates remain mandatory and are documented in `docs/frontend/access/mobile-production-readiness.md` and `docs/frontend/access/mobile-qa.md`.

See `qa.json` and `prg0-static-qa.json` for machine-readable evidence.

## Important boundaries

This archive is a review/acceptance oracle. It does not contain real provider authentication, secure native storage, App/Universal Link association, attestation, token/session implementation or production backend calls.

A3.4 remains the desktop oracle. M1.2 + PRG-0 is the mobile oracle over the same Access semantics.

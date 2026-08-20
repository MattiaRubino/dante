# DANTE Access A3.4 — approved review checkpoint

Status: **SELECTED / APPROVED REVIEW CHECKPOINT / PRE-PRODUCTION**

This archive preserves the exact Access A3.4 HTML approved on 2026-08-20 after the A3.1 direct-sign-up checkpoint and the desktop corner-mark visual exploration.

A3.4 is the selected review reference for later production-frontend migration. It is **not** a production React/runtime implementation and it does **not** freeze backend authentication, session, provider-linking, token, recovery or password-policy contracts.

## Artifact identity

- Source filename: `dante-access-a3-4-corner-mark-strong-review.html`
- Size: `93897` bytes
- SHA-256: `b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6`
- XZ payload size: `18400` bytes
- XZ SHA-256: `923f97e10103ca27115433f7004c93134ce579fdedb5a91d28c4ac35a91cf146`

## Archive parts

The XZ payload is Base64-split only to keep repository transport reliable. Concatenate the parts in lexical order; the split does not change the artifact.

- `part-001.b64` — 5000 Base64 characters; SHA-256 `663024b40e6b2c29c52b4e70455d9573d8516747647ed92de01394338d25ed6c`
- `part-002.b64` — 5000 Base64 characters; SHA-256 `0e5649cf9cb4889edee781d10327fb41f9e27abeac8e8169b1f2598f16de6fa3`
- `part-003.b64` — 5000 Base64 characters; SHA-256 `f714a662c5b83b58e17102e03f6347b04195af4563d27fcc45771e5e4b9e896a`
- `part-004.b64` — 5000 Base64 characters; SHA-256 `4e1dc77f0d524fcab7090e7a2f24b712187b661a3f8a0136ab83740239c49517`
- `part-005.b64` — 4536 Base64 characters; SHA-256 `4e3a262abcd77e0a7227c3a10bf2015a68d4b8e636c083bd96917a4f79493efa`

## Restore

```bash
cat part-*.b64 | tr -d '\n\r' | base64 -d > access-a3-4.html.xz
sha256sum access-a3-4.html.xz
xz -d -c access-a3-4.html.xz > dante-access-a3-4-corner-mark-strong-review.html
sha256sum dante-access-a3-4-corner-mark-strong-review.html
```

Expected hashes:

```text
XZ    923f97e10103ca27115433f7004c93134ce579fdedb5a91d28c4ac35a91cf146
HTML  b1fa909765c1a82db64571ee467ede6bc344c34afc6093d0eae07f335840cec6
```

`restore.py` performs the same restore and fails if either identity does not match.

## Visual delta from A3.1

A3.4 preserves A3.1 behavior/copy and changes the desktop brand-stage treatment only:

- replaces the generic decorative orbit field with the exact locked DANTE Living Orbits symbol geometry;
- desktop corner mark: 1080 × 1080 px, left `-390px`, bottom `-340px`, opacity `0.22`;
- 901–1100 px treatment: 940 × 940 px, left `-360px`, bottom `-315px`, opacity `0.18`;
- the brand stage remains hidden at `<=900px`, so mobile Access remains clean;
- A3.5 full-opacity exploration was explicitly rejected in favor of this stronger-but-muted A3.4 treatment.

The artifact still contains an internal historical CSS comment saying `A3.3 review experiment`; that comment is non-rendering metadata inherited from the iteration and is intentionally left untouched so the approved bytes remain exact.

## Brand provenance

The embedded vector geometry comes from locked brand authorities:

- symbol master: `assets/brand/logo/master/dante-symbol-master-v0.svg` — Git blob `834bc5820fd7065d326a47832cfcb55163f84a76`;
- wordmark master: `assets/brand/wordmark/master/dante-wordmark-master-v0.svg` — Git blob `5985990461a25833e04db5b8972e9c4569d54273`.

No brand master is modified by this checkpoint.

## Scope boundary

The artifact demonstrates the complete reviewed Access + first-entry experience, including provider handoff simulations, DANTE-owned email/password signup, verification, recovery, account-linking UX, re-auth, language switching and lightweight first-run handoff. Provider UI and backend behavior are not simulated as authoritative provider/backend contracts.

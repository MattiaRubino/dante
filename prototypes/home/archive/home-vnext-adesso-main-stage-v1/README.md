# Home vNext Adesso + Main Stage v1 archive

This directory stores the exact standalone HTML checkpoint accepted on 2026-08-17 after the v8 timeline-toolbar state.

## Artifact

`lifeos_home_v8_world_stats_switch_contextual_v23_safe_mid_divider.html`

- size: `344559` bytes
- SHA-256: `a45d1f2b5fab677d738306154a93697e497ffb2c8b2e36ddbba4f4289b42cc77`
- parent approved v8 SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`
- v8 byte-identical prefix: yes (`307487` bytes)

The artifact is stored as a deterministic compressed delta over the approved v8 baseline.

- `v23_fragment.html.gz.b64` — compressed/base64 appended fragment
- `restore_v23.py` — verifies base, fragment and restored full SHA before writing the HTML
- decoded fragment SHA-256: `f79c603823ba34cc2ef5a52e8545fc97234cef1ff1879e6949f188e6aff12815`

The restore path was executed before checkpointing and reproduced the full artifact byte-for-byte.

See `docs/phase-4/home-vnext-adesso-main-stage-v1.md` and `qa-static.json` for the decision and integrity record.

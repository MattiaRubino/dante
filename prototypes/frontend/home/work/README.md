# DANTE Home — modular work source (A2)

This is the maintainable pre-production source mechanically derived from the immutable complete Home oracle at `../current/home.html`.

The complete standalone HTML is intentionally retained and is not modified by A2.

## Copy-on-write modularization

A2 avoids duplicating the entire 748 KB oracle across dozens of new files.

- `index.template.html` is a copy-on-write pointer to the structural template; materializing it derives the exact non-style/non-script structure with deterministic placeholders.
- `styles/` exposes 37 named CSS modules covering all 38 raw style bodies.
- `scripts/` exposes 4 named JavaScript modules covering all 20 raw script bodies.
- Untouched modules are small **oracle pointers**.
- Before editing a module, run `python build.py --materialize <module-path>` to replace that pointer locally with the exact current source for its mapped block(s).
- Once materialized/edited, `build.py` automatically uses the module override instead of the oracle block.
- `assets/day-ribbon-backdrop.png` is a deterministic pointer to the large PNG already embedded in the immutable oracle; the builder verifies the decoded PNG identity. This avoids copying ~375 KB of Base64 into `work/`.
- `manifest.json` owns deterministic block mapping and oracle identity.
- `build/` is generated output and ignored by Git.

Normal build:

```bash
python build.py
```

Materialize one module before changing it:

```bash
python build.py --materialize styles/29-neutralize-old-rails.css
```

Required A2 build identity:

```text
size     748625 bytes
SHA-256  986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df
oracle_match=PASS
```

A2 is structural only. It does not authorize visual, behavioral, naming, branding, backend or production-framework changes.

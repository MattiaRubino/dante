# DANTE — Temporal Create C1 Pre-refactor Final Validation — HISTORICAL

**Status:** SUPERSEDED HISTORICAL EVIDENCE — NOT CURRENT C1 CLOSURE AUTHORITY  
**Original validation date:** 2026-09-02  
**Superseded:** 2026-09-03 by the user manual fail and C1 re-architecture  
**Repository:** `MattiaRubino/dante`  
**Branch:** `feature/home-timeline`

## Historical evidence preserved

The pre-refactor C1 implementation/harness candidate was:

`2b910092ecd70de74338427924666a965938ba9f`

Frontend CI:

- run `33660540265`;
- run number #676;
- Quality PASS;
- Mobile Bundle PASS;
- Chromium Web E2E 96/96 PASS;
- Firefox frozen Timeline 10/10 PASS;
- Frontend CI Gate PASS.

A documentation descendant was later published at:

`27dd5093d21b0a49c8413068aacca139fb2366a4`

with Frontend CI #680 / `33665329466` FULL GREEN.

Quality on the old candidate included:

- typecheck 5/5 PASS;
- architecture 218 modules / 537 dependencies / 0 violations;
- web unit 35 files / 185 tests PASS;
- package suites PASS;
- production build PASS;
- diff/mutation checks PASS.

Old measured Home bundle was approximately:

```text
287.61 kB raw
94.69 kB gzip
```

## Why this is no longer the live final validation

The user executed manual product acceptance after those automated greens and found material UX defects in the Create vertical. The correct decision was:

```text
C1 MANUAL FAIL
```

The old tests proved the implementation satisfied the **old** contract. They did not prove that the old contract was good enough as a high-level production Create experience.

The current workstream therefore re-architects the Create information architecture, Planning Tray interaction and all-day presentation while preserving closed DANTE/F0/T1/domain semantics.

## Current authority

Do not use this file to decide current gate status.

Read instead:

1. `temporal-live-status.md`;
2. `temporal-create-c1-rearchitecture-2026-09-03.md`;
3. `temporal-create-c1-manual-findings-2026-09-03.md`;
4. `temporal-create-handoff.md`.

At the time this historical record was superseded, the active code checkpoint was:

`bd9bc6db13301763393c5345685dd38a1837aaaa`

with Frontend CI #759 / `33744558905`:

- Quality PASS;
- Mobile PASS;
- Chromium 83/96 PASS, 13 stale-contract C1 failures;
- Firefox skipped;
- Gate FAIL.

## Permanent value of this historical evidence

Keep this record because it demonstrates that before the UX re-architecture:

- F0 placement/Undo/idempotency behavior had blocking automated coverage;
- Context vs appearance non-collapse had automated coverage;
- all four CP6 Event recurrence families had automated coverage;
- manual-only Create boundary had automated coverage;
- frozen Timeline regression suite was green;
- Access keyboard harness had been hardened without weakening assertions.

Those guarantees should be preserved or replaced by equivalent/new-contract coverage during the re-architecture.

## Closure rule

This file cannot close C1.

Only a new post-refactor full-green candidate, followed by a new coherent manual acceptance and explicit:

`C1 MANUAL PASS — APPROVED`

may close C1.

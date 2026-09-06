# DANTE — `feature/home-react` Branch Closure Record

**Status:** HISTORICAL / EVIDENCE ONLY — FINAL INTEGRATION CANDIDATE  
**Date:** 2026-09-06  
**Branch:** `feature/home-react`  
**Integration PR:** #65  
**Protected-main baseline consumed:** `431fb34029baeacc9ef9f721e9626b39ca10dd39`

This is the single consolidated closure record for the long-lived `feature/home-react` workstream. It is not current product or architecture authority. Current frontend truth lives in `docs/frontend/README.md`, `docs/frontend/home/current-checkpoint.md`, the World Focus current checkpoint/roadmap/contracts and the materialized code/tests.

Git and PR history remain the complete chronology.

## 1. Scope and outcome

The branch materialized and hardened the Home/World Focus frontend direction through M4, then reconciled that work with the then-current protected `main` without rewriting history.

The final accepted engineering shape preserves:

```text
protected-main platform truth
+ Home/AppShell/Timeline accepted frontend owners
+ World Focus model/application/UI ownership
+ World Focus structural and dependency guards
+ M4 Contextual DANTE D2-D6 chain
```

It does not create canonical World persistence, backend World APIs, real provider/LLM effect execution or a second source of Domain truth.

## 2. Major World Focus milestones

```text
WF0 / WF-G3                     frozen / locked
Workspace Platform              engineering closed
WS0-WS8                         closed
M0                              closed
M1                              closed / validated
post-M1 safety falsification    closed / pass
M2                              closed / validated
M3                              closed / validated
M3 hostile closure              closed / pass
M4 / D2-D6                      closed / validated
M4 hostile closure              closed / pass
R3 main reconciliation          closed / automated QA pass
M5                              not started
M6/M7                           not started / blocked by sequence
```

M4 final historical anchors:

```text
engineering HEAD  1b8ae1a3d953d85dcc14d513e512428d1f268c8d
CI                33990483780 / run #1087 PASS
docs closure      969e0f0058c5ca573282cbfc5aebc6c3715d1141
```

## 3. M1 / post-M1 evidence retained from retired operational handoff

The retired `world-focus-m1-operational-handoff.md` was a temporary continuation pointer, not a durable authority. Its useful execution evidence remains recorded here and in the M1/post-M1 review evidence:

```text
M1-1 identity/reference
HEAD e0f4003496bfbf828ed9ab7718af8e7e30342ad3
CI   33679425668 PASS

M1-2 non-visual semantics/application seams
HEAD 5e98e4b97639cd018badc23e35e7a523f2940875
CI   33738873773 PASS

M1 final red-first falsification
HEAD 67bd06d63d84273ba2077761919d714c8d442254
CI   33740212989 EXPECTED FAILURE
finding: hidden non-enumerable cursor.contextReferences

M1 final code closure
HEAD 7369c51e7ba04f8913728a0770f700c728c3b9f9
CI   33740710290 PASS

post-M1 safety red
HEAD 0b674effa292881303288dd90c88db2c14e61872
CI   33747167897 EXPECTED FAILURE

post-M1 safety closure
HEAD ecc2128b62395f82eab9ee7ff239355b4ca81ee4
CI   33754084001 PASS
```

The two post-M1 safety defects were closed without weakening the hostile test: late completion after cancelled non-cooperative read, and O8 Evidence/History caller aliasing.

## 4. Timeline handoff consolidation

`timeline-handoff.md` and `timeline-current-checkpoint.md` were branch-operational continuation aids. They are retired before protected-main integration under the Documentation Lifecycle Policy.

No unique current Timeline law is lost. Durable ownership remains in:

```text
docs/frontend/home/timeline-t1-frozen-contract.md
docs/frontend/home/temporal-experience-architecture.md
docs/frontend/home/temporal-frontend-roadmap.md
docs/frontend/home/temporal-f0-contract.md
```

The accepted T1 interaction grammar remains protected, including first-gesture custom drag, deselect-first focus behavior, explicit title/time/subitem actions, drag cleanup/cancellation behavior, accepted move+undo semantics and Chromium/Firefox regression coverage.

T2+ is not activated by branch closure.

## 5. Protected-main reconciliation

The first technical conflict/reconciliation PR was #64, with protected `main` as head and `feature/home-react` as base. It merged protected-main ancestry into the feature rather than rebasing or rewriting history.

Key reconciliation anchors:

```text
protected main         431fb34029baeacc9ef9f721e9626b39ca10dd39
feature pre-merge      561cd43f058427a84a5487b6eaf807d100fb9233
ancestry merge         2547d4a08b5f289ba53676aea194348bb22bd6ce
R3 semantic candidate  b60d0e6cda31af1ad7575dabcc46cd88b402f043
R3 formatted candidate e28e29a7ab3a8cd71b0c386ced824385c8c2d9e6
```

R3 did not choose `ours` or `theirs` wholesale. It preserved current-main DB/Auth/Recovery/Email/Observability/OpenAPI/Intelligence/Temporal owners and restored frozen M4 World Focus owners plus the shared architectural guards required by that implementation.

## 6. R3 exact-code validation

PR #65 exercised the protected-main required checks against exact candidate `e28e29a7ab3a8cd71b0c386ced824385c8c2d9e6`:

```text
Backend CI         34023569263 PASS
Dependency Review  34023569294 PASS
Frontend CI        34023569317 PASS
```

That includes:

```text
Backend Quality / mypy / tests / package build       PASS
Backend PostgreSQL acceptance                        PASS
AI deterministic eval gate                           PASS
Frontend contract drift                              PASS
format / lint / typecheck / architecture             PASS
generated-source drift / units / production build   PASS
Chromium Web E2E                                     PASS
frozen Timeline Firefox                              PASS
Mobile Bundle                                        PASS
```

No PR review threads/comments were pending at the closure review.

The final lifecycle/documentation consolidation is intentionally non-semantic. The repository ruleset and required checks on the final PR head remain the authority for actual protected-main integration.

## 7. Explicit non-approvals

Branch closure and merge must not manufacture product approvals that were never granted:

```text
C1 Manual Temporal Create      OPEN
C1 MANUAL PASS — APPROVED      NOT GRANTED
human/manual World Focus visual acceptance  NOT PERFORMED
M5 complete contrasting Worlds NOT STARTED
production World backend       NOT AUTHORIZED
real provider/LLM effects      NOT AUTHORIZED
```

## 8. Where current truth lives

After integration, do not continue from this branch record. Read:

```text
docs/frontend/README.md
docs/frontend/home/current-checkpoint.md
docs/frontend/home/world-focus-current-checkpoint.md
docs/frontend/home/world-focus-frontend-roadmap.md
docs/frontend/home/world-focus-product-contract.md
docs/frontend/home/world-focus-platform-contract.md
docs/frontend/home/world-focus-structural-contract.md
docs/frontend/home/world-focus-geometry-contract.md
docs/frontend/home/world-focus-evidence-index.md
```

Future work starts from the then-current protected `main` under a new explicit scope. This file remains historical/evidence only.

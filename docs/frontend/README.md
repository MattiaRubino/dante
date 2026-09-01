# DANTE — Frontend Documentation Entry Map

**Status:** CURRENT FRONTEND DOCUMENTATION ENTRY POINT  
**Date:** 2026-09-01  
**Branch context:** production-shaped frontend plus active `feature/home-react` workstreams

This directory contains the durable product, architecture, handoff and production-readiness documentation for the materialized frontend.

The checked-out code/tests/CI remain implementation truth. Historical prototype material is evidence/oracle only where current documentation explicitly says so.

## 1. First read for any new frontend chat

Always start with:

1. `docs/frontend/home/current-checkpoint.md` — **live branch state and active workstream**;
2. `docs/frontend/home/production-depth-handoff.md` — shared frontend engineering/operational handoff.

Do not infer current sequencing from an older feature review or roadmap before reading those two files.

## 2. Then choose the actual workstream

### AppShell / Home

Read:

1. `docs/frontend/home/home-structural-contract.md` — frozen Whole-Home macro ownership/geometry;
2. `docs/frontend/app-shell/p1-global-app-shell.md` — shared AppShell/Topbar contract;
3. `docs/frontend/home/contract.md` — durable Home product/behavior **prototype oracle**, not the live branch checkpoint;
4. `docs/frontend/open-decisions.md`;
5. `docs/frontend/ui-registry.md`;
6. `docs/frontend/design-tokens.md`.

`home/contract.md` intentionally preserves accepted Home product intent from the prototype lineage. Its old prototype milestone/version labels are historical context and do **not** override `current-checkpoint.md`, current React code or newer frozen structural contracts.

### Timeline / temporal capability

Read in this order:

1. `docs/frontend/home/timeline-current-checkpoint.md` — current temporal status;
2. `docs/frontend/home/timeline-handoff.md` — new-chat temporal handoff;
3. `docs/frontend/home/timeline-t1-frozen-contract.md` — user-accepted observable T1 contract;
4. `docs/frontend/home/temporal-experience-architecture.md` — current temporal product/application architecture;
5. `docs/frontend/home/temporal-frontend-roadmap.md` — T1 frozen, T2 next only when temporal work explicitly resumes.

Timeline T1 must not be reopened by unrelated Home/World work. Critical interaction/geometry behavior remains protected in Chromium and Firefox.

### World Focus

Read in this order:

1. `docs/frontend/home/world-focus-current-checkpoint.md` — **live World status and exact next gate**;
2. `docs/frontend/home/world-focus-handoff.md` — durable World new-chat handoff;
3. `docs/frontend/home/world-focus-product-contract.md` — current World product authority after WR0/WR1/WR2;
4. `docs/frontend/home/world-focus-platform-contract.md` — current implementation/platform authority;
5. `docs/frontend/home/world-focus-structural-contract.md` — frozen route/workspace structural contract;
6. `docs/frontend/home/world-focus-geometry-contract.md` — locked WF-G3 geometry;
7. `docs/frontend/home/world-focus-delivery-methodology.md` — mandatory mini-vertical method and user gate;
8. `docs/frontend/home/world-focus-frontend-roadmap.md` — current pre-backend sequencing;
9. `docs/frontend/home/world-focus-evidence-index.md` — historical research/review map, only when deeper archaeology is needed.

World research/review evidence deliberately does not carry live sequencing authority. Internal status lines inside those evidence documents describe the historical pass in which they were written.

Current World sequencing is controlled only by the live checkpoint/handoff/current contracts/roadmap.

## 3. Production-readiness authorities

For any non-trivial implementation also inspect the relevant current engineering contracts:

- `docs/frontend/production-readiness/component-architecture.md`;
- `docs/frontend/production-readiness/backend-integration-contract.md`;
- `docs/frontend/production-readiness/quality-gates.md`;
- `docs/frontend/terminology.md`;
- `docs/frontend/localization.md`;
- `docs/frontend/design-tokens.md`.

## 4. Access/Auth boundary

`docs/frontend/access.md` is the current durable Access Web contract.

Access/Auth is a separate workstream. Home/Timeline/World changes must not casually modify it to resolve unrelated CI flakes or UI problems.

The current frontend does not claim real Auth backend behavior unless a later full-stack Access/Auth vertical explicitly provides it.

## 5. Semantic authority hierarchy

Frontend documentation consumes rather than redefines DANTE's deeper authorities.

When semantic meaning is touched, re-read as applicable:

- Product Identity / North Star;
- current product simulations;
- Domain Atlas / Language Map;
- Logical Model;
- Physical Model;
- Database source of record / Alembic history;
- Intelligence Context/Runtime contracts;
- Governed Operation/Effect contracts.

Permanent examples:

```text
frontend view model != backend DTO != Domain != persistence row
AI output != canonical fact
AI proposal != Decision
provider state != canonical state
planned != actual
absence != false
UI hiding != authorization
```

Product labels must not silently become Domain ontology.

## 6. Home migration / prototype rule

The accepted Home prototype is an executable UX/reference oracle, not source code to transliterate line-by-line into React.

Current React implementation must:

- preserve accepted product/behavior intent unless an explicit reviewed scope changes it;
- preserve the frozen Whole-Home structural contract;
- use current React/TypeScript ownership rather than revive prototype internals;
- separate view models from backend/domain/persistence shapes;
- preserve semantic IDs/localization and machine-readable structural contracts;
- keep semantic World/group/event/state colors distinct from generic infrastructure chrome.

Prototype branches and wrappers are historical evidence, not runtime dependencies.

## 7. Machine-readable structural authority

Whole-Home structure is also protected by machine-readable contracts under:

`prototypes/frontend/shared/contracts/`

including the current Home structure/responsive matrices and World Focus structure/responsive geometry contracts.

These are exercised by repository tests/CI together with React and Playwright guards.

## 8. Documentation hygiene rule

A document can be one of:

```text
LIVE CHECKPOINT
HANDOFF
CURRENT CONTRACT / ARCHITECTURE
CURRENT ROADMAP
FROZEN CHANGE-CONTROL CONTRACT
EVIDENCE / HISTORICAL ORACLE
```

Do not leave an obsolete roadmap/checkpoint in the live read path after a later decision supersedes it.

When a workstream materially changes sequence or accepted behavior:

1. update its live checkpoint;
2. update its handoff;
3. update current contract/roadmap if the decision changes them;
4. remove truly superseded checkpoint/roadmap documents when their useful reasoning is already preserved elsewhere;
5. retain deep research as evidence only when it still adds unique reasoning, and route it through an evidence index where needed.

The goal is that a new chat can determine **where we are, what is frozen, what is open and what comes next without reconstructing chronology from Git history**.

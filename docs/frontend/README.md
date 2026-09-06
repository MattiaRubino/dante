# DANTE — Frontend Documentation Entry Map

**Status:** CURRENT FRONTEND DOCUMENTATION ENTRY POINT — MAIN PLATFORM RECONCILED — WORLD FOCUS M4 CLOSED / R3 QA PENDING  
**Date:** 2026-09-06  
**Working branch:** `feature/home-react`

This directory contains the durable product, architecture, handoff and production-readiness documentation for the materialized frontend. Current code, tests and CI evidence outrank historical branch notes.

## 1. First read

For current frontend work read:

1. `docs/frontend/home/current-checkpoint.md` — live integrated frontend state;
2. `docs/frontend/home/production-depth-handoff.md` when present — shared engineering/operational handoff;
3. the workstream-specific current contract/roadmap below.

Do not reconstruct current sequencing from archived or dated evidence documents.

## 2. AppShell / Home / Temporal

Read:

1. `docs/frontend/home/home-structural-contract.md`;
2. `docs/frontend/app-shell/p1-global-app-shell.md`;
3. `docs/frontend/home/temporal-frontend-roadmap.md`;
4. `docs/frontend/home/temporal-f0-contract.md`;
5. `docs/frontend/home/timeline-t1-frozen-contract.md`;
6. `docs/frontend/home/temporal-create-c1-manual-acceptance.md`;
7. `docs/frontend/home/contract.md`;
8. `docs/frontend/open-decisions.md`;
9. `docs/frontend/ui-registry.md`.

Current status:

```text
H0 Whole Home structure        FROZEN
P1 AppShell / Topbar           FROZEN
T1 Timeline                    FROZEN
F0 Temporal application seam   CLOSED / FROZEN
C1 Manual Temporal Create      OPEN
C1 MANUAL PASS                 NOT GRANTED
C2 Structured Detail           BLOCKED until C1 closes
```

Merging or reconciling branches does not manufacture C1 manual product approval.

## 3. World Focus

Read in this order:

1. `docs/frontend/home/world-focus-current-checkpoint.md`;
2. `docs/frontend/home/world-focus-product-contract.md`;
3. `docs/frontend/home/world-focus-platform-contract.md`;
4. `docs/frontend/home/world-focus-structural-contract.md`;
5. `docs/frontend/home/world-focus-geometry-contract.md`;
6. `docs/frontend/home/world-focus-delivery-methodology.md`;
7. `docs/frontend/home/world-focus-frontend-roadmap.md`;
8. `docs/frontend/home/world-focus-evidence-index.md` only for deeper archaeology.

The old live handoff and WF0 scenario-oracle files are not current operating authorities. Their useful reasoning is retained in current contracts/evidence and Git history.

Current status:

```text
WF0 / WF-G3                       FROZEN / LOCKED
M0-M3                             CLOSED / VALIDATED
M4 Contextual DANTE / D2-D6       CLOSED / VALIDATED
M4 hostile closure                CLOSED / PASS
main -> feature/home-react merge  COMPLETE @ 2547d4a08b5f289ba53676aea194348bb22bd6ce
R3 semantic reconciliation        CANDIDATE / QA PENDING
M5 contrasting Worlds             NOT STARTED
M6 visual/a11y/perf               BLOCKED BY M5
M7 pre-backend freeze             BLOCKED BY M6
human/manual visual acceptance    NOT PERFORMED
```

## 4. Current platform truth inherited from main

The branch consumes current protected-main platform truth rather than an old frontend-only snapshot. That includes the current PostgreSQL/Alembic baseline, Access/Auth implementation, Recovery, Email, Observability, OpenAPI/API-client boundaries and Intelligence foundation.

Frontend work must not overwrite those owners for convenience.

Current Access Web capability includes the governed backend integration for email/password, session lifecycle, recovery/reset/reauth, Google and Apple provider flows, passkeys, authenticator management and `/security`. Access UI/model remains behind its application boundary and the governed API client.

## 5. Permanent semantic boundaries

```text
frontend view model != backend DTO != Domain != persistence row
World != Domain owner
World relevance != authorization
projection != canonical truth
AI output != accepted fact
assistant prose != Insight
Insight != Proposal != Decision != effect
confirmed != executed
Receipt != provider/runtime/canonical completion
planned/intended != Actual
Comparison != Decision
absence != false
UI hiding != authorization
```

World Focus remains pre-backend for its own canonical World/DANTE persistence/effect semantics even though the repository now contains real backend platform capability elsewhere.

## 6. Engineering authorities

For non-trivial frontend work also inspect:

- `docs/frontend/production-readiness/component-architecture.md`;
- `docs/frontend/production-readiness/backend-integration-contract.md`;
- `docs/frontend/production-readiness/quality-gates.md`;
- `docs/frontend/terminology.md`;
- `docs/frontend/localization.md`;
- `docs/frontend/design-tokens.md`;
- current `dependency-cruiser.config.mjs`;
- current GitHub Actions workflows.

Machine-readable Home and World Focus structural contracts under `prototypes/frontend/shared/contracts/` are blocking CI contracts, not decoration.

## 7. Reconciliation rule

R3 preserves current `main` as authority for platform/Access/Temporal integration while restoring the frozen M4 World Focus owners and architectural guards. R3 is not validated until CI is green on the exact candidate HEAD.

No PR merge, protected-main write, rebase, squash or force-push is implied by this document.

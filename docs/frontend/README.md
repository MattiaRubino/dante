# DANTE — Frontend Documentation Entry Map

**Status:** CURRENT FRONTEND DOCUMENTATION ENTRY POINT  
**Date:** 2026-09-06

This directory contains the durable product, architecture, contract and production-readiness documentation for the materialized frontend. Current code, tests and current CI evidence outrank historical branch notes and dated evidence.

## 1. First read

For current frontend work read:

1. `docs/frontend/home/current-checkpoint.md` — current integrated frontend state;
2. the workstream-specific current contract/roadmap below;
3. deeper dated evidence only when rationale or historical proof is needed.

Do not reconstruct current sequencing from archived handoffs or obsolete `NEXT` prose.

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

Branch reconciliation, CI or merge does not manufacture C1 manual product approval.

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

Current engineering status:

```text
WF0 / WF-G3                       FROZEN / LOCKED
M0-M3                             CLOSED / VALIDATED
M4 Contextual DANTE / D2-D6       CLOSED / VALIDATED
M4 hostile closure                CLOSED / PASS
protected-main ancestry merge     COMPLETE
R3 semantic reconciliation        CLOSED / AUTOMATED QA PASS
M5 contrasting Worlds             NOT STARTED
M6 visual/a11y/perf               BLOCKED BY M5
M7 pre-backend freeze             BLOCKED BY M6
human/manual visual acceptance    NOT PERFORMED
```

R3 exact-code candidate `e28e29a7ab3a8cd71b0c386ced824385c8c2d9e6` passed Backend CI, Dependency Review and Frontend CI on PR #65. Required protected-main checks on the final merge head remain the merge authority; historical run IDs prove only their exact SHA.

The branch candidate becomes protected-main truth only through PR #65 and the repository ruleset. Git/PR state is authoritative for whether that integration has occurred.

## 4. Current platform truth inherited from main

The reconciled frontend consumes protected-main platform truth rather than an old frontend-only snapshot. That includes the current PostgreSQL/Alembic baseline, Access/Auth implementation, Recovery, Email, Observability, OpenAPI/API-client boundaries and Intelligence foundation.

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

World Focus remains pre-backend for its own canonical World/DANTE persistence/effect semantics even though the repository contains real backend platform capability elsewhere.

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

## 7. Lifecycle rule

Temporary chat/session/live handoffs are not current repository authorities and must not survive into protected `main`. Historical proof belongs in dated evidence, the consolidated branch closure record or Git/PR history. Current product and architecture truth belongs in the current contracts/checkpoints above.

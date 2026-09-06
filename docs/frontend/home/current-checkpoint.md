# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT LIVE ENTRY POINT — MAIN PLATFORM RECONCILED — WORLD FOCUS M4 CLOSED / R3 QA PENDING  
**Date:** 2026-09-06  
**Working branch:** `feature/home-react`  
**Protected-main baseline merged:** `431fb34029baeacc9ef9f721e9626b39ca10dd39`  
**Merge commit:** `2547d4a08b5f289ba53676aea194348bb22bd6ce`

This is the live frontend navigation checkpoint after protected-main ancestry was merged into `feature/home-react`. R3 is reconciling semantic ownership after the mechanical merge. Current code/tests/CI outrank historical branch labels.

## 1. Integrated platform state

The branch now contains current `main` platform truth, including the current PostgreSQL/Alembic baseline and the current backend/platform capabilities for Access/Auth, Recovery, Email, Observability, OpenAPI/API-client boundaries and Intelligence foundation.

Those owners are not frontend reconciliation targets. R3 must preserve them.

## 2. Home / Temporal state

```text
H0 Whole Home structure        FROZEN
P1 AppShell / Topbar           FROZEN
T1 Timeline                    FROZEN
F0 Temporal application seam   CLOSED / FROZEN
C1 Manual Temporal Create      OPEN
C1 MANUAL PASS — APPROVED      NOT GRANTED
C2 Structured Detail           BLOCKED until C1 closes
```

Current Temporal Create capability from `main` remains present. Branch integration and automated CI do not count as manual C1 acceptance.

Permanent Temporal distinctions remain:

```text
Activity != Event != Routine
Schedule != Occurrence != Session != Actual
planned/intended != happened
recurrence specification != generated Occurrence
Context != appearance
manual Create != AI/NL/voice
Timeline ViewModel != application model != DTO != DB row
provider state != canonical DANTE state
```

## 3. World Focus state

```text
WF0                                      FROZEN / USER AUTHORIZED
WF-G3                                    LOCKED / USER AUTHORIZED
B0 / WR0-WR2 / B1 / B2                  CLOSED AS RECORDED
Workspace Platform                       ENGINEERING CLOSED
D0                                       ACCEPTED
D1                                       CLOSED FOR SEQUENCING
WS0-WS8                                  CLOSED
POST-WS8 HYGIENE                         CLOSED / APPLIED
PRE-M0 FALSIFICATION                     CLOSED / PASS
M0                                       CLOSED
M1                                       CLOSED / VALIDATED
POST-M1 SAFETY FALSIFICATION             CLOSED / PASS
M2                                       CLOSED / VALIDATED
M3 Adaptive World Composition            CLOSED / VALIDATED
M3 final hostile closure                 CLOSED / PASS
M4 Contextual DANTE / D2-D6              CLOSED / VALIDATED
M4 final hostile closure                 CLOSED / PASS
main -> feature/home-react merge          COMPLETE @ 2547d4a08b5f289ba53676aea194348bb22bd6ce
R3 semantic reconciliation               CANDIDATE / QA PENDING
M5 complete contrasting Worlds           NOT STARTED
M6 integrated product/visual/a11y/perf   BLOCKED BY M5
M7 pre-backend frontend freeze           BLOCKED BY M6
human/manual visual review               NOT PERFORMED
```

The M4 closure source remains:

```text
M4 documentation closure
969e0f0058c5ca573282cbfc5aebc6c3715d1141

M4 engineering hostile closure
1b8ae1a3d953d85dcc14d513e512428d1f268c8d
CI 33990483780 / run #1087 PASS
```

Historical green evidence remains evidence for those exact SHAs only; it is not current R3 validation.

## 4. M4 semantic result that R3 must preserve

World Focus has one bounded pre-backend DANTE path:

```text
quiet/global or explicit contextual invoke
-> deterministic mounted conversation
-> bounded contextual ownership
-> standalone validated Insight
-> Proposal
-> required blocking Confirmation
-> local Decision
-> truthful local Receipt
```

Permanent non-collapses:

```text
World != canonical Domain owner
World relevance != authorization
projection != canonical truth
reference exists != payload available != current != disclosable != fresh
Evidence != Provenance != integrity attestation
AI output != accepted fact
selected UI/context != authorization
context reference != canonical truth
conversation message != Insight
assistant prose != validated Insight
Insight != Proposal
Proposal != Decision
Decision != effect
confirmed != executed
Receipt != canonical/provider/runtime completion
provider ACK != canonical completion
Comparison != Decision
missing trajectory position != zero
```

## 5. R3 ownership result

R3 is intentionally not `ours` or `theirs` wholesale.

```text
main authority
+ frozen M4 World Focus owners
+ composed shared guards/i18n/docs
= reconciliation candidate
```

R3 restores the M4 World Focus page/fixture/geometry/E2E ownership and the M4 Signal Stage class contract, removes temporary files resurrected only to make the ancestry merge possible, and composes shared CI/architecture/localization/documentation without discarding current-main platform work.

## 6. QA gate

R3 is **not validated yet**.

Required exact-candidate validation:

```text
Frontend contract drift: Home + World Focus
format
lint
typecheck
architecture
generated-source drift
unit tests
production build
Chromium Web E2E
frozen Timeline Firefox
Mobile compatibility/bundle
current Access tests
current Temporal tests
M4 hostile World Focus suite
backend required checks through the PR gate
Dependency Review
```

A draft PR may be opened only to obtain the real protected-main PR checks. Draft PR creation is not permission to merge.

## 7. Immediate sequence

```text
complete R3 semantic reconciliation
-> exact PRE-SCOPE compare
-> verify behind_by=0 from current main
-> open draft PR to main for real required checks
-> fix only concrete failures by ownership
-> R4 evidence closure after exact-head green
-> separate explicit authorization before any merge to protected main
```

No rebase, squash, force-push or protected-main write is authorized by this checkpoint.

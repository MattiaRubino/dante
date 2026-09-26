# Timeline / Temporal-Operational Vertical — Implementation Roadmap

- **Status:** CURRENT EXECUTION ROADMAP — reconciled 2026-09-26
- **Branch/workstream:** `feature/timeline-temporal-operational`
- **Vertical boundary:** Home `+` creation/configuration → canonical temporal truth → Timeline projection/actions → bounded lifecycle completion
- **Completed functional frontier:** B10 ✅ CLOSED 2026-09-26
- **Current block:** B11 Advanced Recurrence / Conditional / Reminder
- **Last proven persistence frontier:** B10-D / Alembic `20260926_80`
- **B10-D closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`
- **B10-E closure evidence:** `docs/workstreams/timeline-temporal-operational-b10-e-closure-2026-09-26.md`
- **Deferred block:** B07 UI/UX Consolidation v1 — execute only after B14
- **Live execution ledger:** `docs/workstreams/timeline-temporal-operational-map.md`
- **Continuation handoff:** `docs/workstreams/timeline-temporal-operational-handoff.md`

This document is the sequencing authority for the remaining Timeline / Temporal-Operational work.

---

# 0. Execution discipline

Every functional block closes vertically:

```text
current Product / Domain / Logical / Physical authority
→ persistence / Alembic / Dictionary when required
→ backend / application
→ HTTP API / OpenAPI when public
→ generated API client when public
→ frontend / real product surface when part of the block
→ local automated proof
→ documentation reconciliation
→ only then advance
```

The user runs local tests. Do not use GitHub Actions/CI unless explicitly authorized.

Published migrations are immutable. Generated API-client artifacts come only from repository generation tooling and are never hand edited.

Permanent boundaries:

```text
Domain != Logical != Physical != API DTO != frontend ViewModel
projection != canonical truth
planned/intended != happened
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Confirmation != Authority / Verification / Decision
Reconciliation != universal truth
Expected outcome != Outcome
Responsibility != Participation
Person != Account
Step != Activity
Plan != Activity
Dependency != hierarchy
ordering != dependency
proposal != accepted effect
current accepted state != latest row
MaterialState payload != mutable runtime record
idempotency key != Domain identity
Undo != history rewind
editable Create intent != canonical persistence
```

---

# 1. Active execution order

Historical block identifiers are preserved. Execution order is intentionally non-numeric where dependencies require it.

```text
B00 Real Data Spine                              ✅ CLOSED / PROVEN
B01 Activity Core                                ✅ CLOSED / PROVEN
B02 Schedule Core                                ✅ CLOSED / PROVEN
B03 Event Core                                   ✅ CLOSED / PROVEN
PRE-B04 DB/API GOVERNANCE                        ✅ CLOSED / FROZEN
B04 Temporal Constraints + Movement Policy       ✅ CLOSED / PROVEN
B05 Product Organization                         ✅ CLOSED / PROVEN
B06 Routine / Recurrence / Occurrence Baseline   ✅ CLOSED / PROVEN
B08 Session Runtime                              ✅ CLOSED / USER-REPORTED 2026-09-24
B09 Responsibility / Participation               ✅ CLOSED / USER-REPORTED 2026-09-25

B10 Actual / Outcome / Confirmation / Resolution ✅ CLOSED 2026-09-26
  B10-A Actual / realization core                 ✅ CLOSED / PROVEN 2026-09-25
  B10-B Outcome                                   ✅ CLOSED / PROVEN 2026-09-25
  B10-C Confirmation                              ✅ CLOSED / PROVEN 2026-09-26
  B10-D Reconciliation / resolution workflow      ✅ CLOSED / PROVEN 2026-09-26
  B10-E Final integration + acceptance            ✅ CLOSED / USER-REPORTED ACCEPTANCE 2026-09-26

B11 Advanced Recurrence / Conditional / Reminder 🟨 NEXT
B13 Work Structure / Decomposition / Dependencies⬜
B12 Replanning / Conflict / Solver               ⬜
B14 Temporal Create Completeness Gate             ⬜
B07 UI/UX Consolidation v1                       ⏸ DEFERRED UNTIL B14
B15 Whole Vertical Closure                       ⬜
```

Execution sequence:

```text
B09 → B10 → B11 → B13 → B12 → B14 → B07 → B15
```

B13 precedes B12 so replanning/solver logic already understands work structure and dependencies. B14 precedes B07 so final UI consolidation does not polish unsupported editable intent.

---

# 2. Proven foundation through B09

B00–B06, B08 and B09 are closed. Their permanent boundaries remain active in all later work.

```text
Activity may exist without Schedule
Event != Activity
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule is accepted-placement authority
Life Area / Tags are product organization, not Domain ownership
Person != Account != Actor
Responsibility != Participation
Session != Actual
Session END != completion
```

B09 adds typed Person/Responsibility/expected Participation behavior without collapsing Person into Account or expected Participation into Actual attendance.

---

# 3. B10 — Actual / Outcome / Confirmation / Reconciliation — CLOSED

B10 added realized/reconciled truth while preserving:

```text
planned/intended != happened
Schedule != Session != Actual
Session END != completion
Actual != Outcome != Confirmation
Confirmation != Authority / Verification / Decision
Reconciliation != universal truth
Expected outcome != Outcome
no Actual != known non-realization/failure
```

## B10-A — Actual / realization core — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-a-closure-2026-09-25.md`.

```text
Alembic  20260925_74
Topology 159|5|115|93|305|258|435
```

```text
Session END != Actual
absence of Actual = unknown
known realization_occurred=false != absence
Session evidence != Actual identity
current accepted realization != latest row
```

## B10-B — Outcome — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-b-closure-2026-09-25.md`.

```text
Alembic  20260925_78
Topology 163|5|119|93|317|268|440
facet: outcome.disposition
```

```text
one stable Outcome per Actual
Outcome disposition pinned to exact Actual realization MaterialState
Actual correction does not reinterpret older Outcome disposition
```

The temporary `_75` vocabulary/result identity model is superseded and must not return.

## B10-C — Confirmation — CLOSED / PROVEN

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-c-closure-2026-09-26.md`.

```text
Alembic  20260925_79
Topology 167|5|123|93|329|279|446
facet: confirmation.attestation
```

```text
identity = (target Outcome MaterialState, confirmer Person, purpose)
0..N confirmations per exact Outcome disposition MaterialState
absence of Confirmation != false
Outcome correction does not transfer Confirmation
```

The post-closure public-contract hardening is closed: OpenAPI/generated truth includes `201` creation, `200` replay and bounded ProblemDetails failures.

## B10-D — Reconciliation / resolution workflow — CLOSED / PROVEN

Scope: `docs/workstreams/timeline-temporal-operational-b10-d-scope-2026-09-26.md`.
Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-d-closure-2026-09-26.md`.

Persistence frontier:

```text
20260926_80
```

Canonical family:

```text
outcome_reconciliation
outcome_reconciliation_state
outcome_reconciliation_evidence
outcome_reconciliation_current_history
outcome_reconciliation_operation
facet: outcome.reconciliation
```

Stable identity:

```text
(outcome_disposition_material_state_ref, purpose_code)
```

Authority boundary:

```text
Outcome owner is the only resolver in B10-D
can confirm != can resolve
resolver identity is state data
```

Evidence pins exact Confirmation attestation MaterialStates. Confirmation correction does not reinterpret older reconciliation; Outcome correction does not transfer reconciliation.

Approved contextual actions:

```text
unresolved
select
accept_multiple
defer
escalate
```

Generated client commit:

```text
cebfb557196d3fc0f412262a1d12feae9291b875
```

User-run proof:

```text
PostgreSQL/runtime/API + direct B10-C regression    4 passed in 14.94s
web typecheck                                       PASS
Confirmation + Reconciliation web controls         6 passed / 2 files
generated check                                     PASS — 345 files deterministic/current
api-client typecheck                                PASS
B10-D/B10-C/OpenAPI inventory backend gate          6 passed
```

No CI/GitHub Actions were used.

## B10-E — Final integration + acceptance — CLOSED / USER-REPORTED ACCEPTANCE

Closure evidence: `docs/workstreams/timeline-temporal-operational-b10-e-closure-2026-09-26.md`.

B10-E integrated the chain:

```text
Session → Actual → Outcome → Confirmation → Reconciliation
```

Repository integration coverage was added in:

```text
apps/backend/tests/integration/temporal/test_b10_e_whole_block.py
apps/web/src/features/temporal/timeline-truth-inspector.test.tsx
```

The B10 truth inspector is mounted from the canonical Home timeline runtime. The user performed the requested integrated real-app walkthrough and reported the flow working, including correction boundaries and reload persistence.

The B10-E-specific automated tests were added but were not separately reported as user-run at closure time; closure therefore records B10-E precisely as `USER-REPORTED ACCEPTANCE`, while B10-A through B10-D retain their `PROVEN` classifications.

Whole B10 is now CLOSED. Advance directly to B11.

---

# 4. B11 — Advanced Recurrence / Conditional / Reminder — NEXT

B11 extends recurrence and conditional/reminder behavior without RRULE-as-ontology, fake Activity materialization or an unjustified universal Reminder owner.

The editable Create reminder intent must leave B11 either:

```text
canonically supported
truthfully handed off
or hidden until supported
```

Before implementation, reconcile the current B06 recurrence baseline with the relevant Domain / Logical / Physical / Database authority and inspect existing reminder/conditional UI/API intent.

---

# 5. B13 — Work Structure / Decomposition / Dependencies

B13 distinguishes:

```text
1. INTERNAL STEP
   Step != Activity

2. COMPOSITE WORK
   real Activities retain independent identity/lifecycle/Schedule/Session

3. DEPENDENCY
   Dependency != hierarchy
   ordering != dependency
```

It also closes temporal execution-structure foundations where semantically appropriate: maximum Session count, merge compatibility, spacing, preparation/recovery and related structure rules.

---

# 6. B12 — Replanning / Conflict / Solver

Deterministic-first replanning/conflict/solver:

```text
canonical truth + constraints/preferences + B13 dependencies
→ deterministic candidate generation / optimization
→ Proposal(s)
→ optional AI interpretation/ranking assistance
→ governed acceptance
→ canonical Schedule mutation
```

```text
proposal != accepted Schedule
preferred window != accepted Schedule
fallback policy != hidden mutation
solver UNKNOWN != INFEASIBLE
AI != scheduling authority
```

---

# 7. B14 — Temporal Create Completeness Gate

For every editable field visible in Create, exactly one must be true:

```text
A. canonically persisted and behaviorally proven
B. truthful handoff to owning capability
C. explicitly presentation/read-only
D. hidden/removed until supported
```

Forbidden:

```text
editable UI value
→ collected
→ silently ignored by normal submit
```

---

# 8. B07 — UI/UX Consolidation v1

Execute after B14 so final Home/Timeline/`+`/editors/actions/navigation are designed once against truthful functional vocabulary. B07 does not create missing semantics.

---

# 9. B15 — Whole Vertical Closure

Final whole-vertical reconciliation across migrations/catalog/Dictionary, backend/API/client, frontend, negative invariants, local automated proof and dogfood.

B15 does not reopen closed semantic boundaries without explicit evidence.
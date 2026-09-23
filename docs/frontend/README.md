# DANTE — Frontend Documentation Entry Map

**Status:** CURRENT FRONTEND DOCUMENTATION ENTRY POINT  
**Reconciled:** 2026-09-23

This directory contains durable product, architecture, contract and production-readiness documentation for the materialized frontend. Current code/tests plus active workstream authority outrank historical branch notes and dated evidence.

## 1. First read

For current frontend work read:

1. `docs/frontend/home/current-checkpoint.md` — current frontend navigation checkpoint;
2. the active bounded workstream authority for the feature being changed;
3. deeper dated evidence only when rationale or historical proof is needed.

Do not reconstruct current sequencing from old C1/T1 handoffs or obsolete `NEXT` prose.

## 2. Home / Timeline / Temporal — current state

The former `feature/home-timeline` C1/T1 frontend roadmap is **historical pre-vertical evidence**. The real backend/persistence Timeline vertical is now owned by:

1. `docs/workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`;
2. `docs/workstreams/timeline-temporal-operational-roadmap.md`;
3. `docs/workstreams/timeline-temporal-operational-map.md`;
4. `docs/workstreams/timeline-temporal-operational-handoff.md`.

Current state:

```text
Home/AppShell structural foundations              retained
Timeline/Temporal prototype-era contracts          retained as design/history where still applicable
Real Data Spine through B06                        ✅ CLOSED / PROVEN
Activity / Schedule / Event                        ✅ canonical backend-backed
Constraints / Movement Policy                      ✅ canonical backend-backed
Life Area / Tags                                    ✅ canonical backend-backed
Routine / Recurrence / Occurrence                  ✅ canonical backend-backed
Expected/scheduled recurring Timeline              ✅ real backend-backed
B08 Session Runtime                                ← NEXT
B07 final UI/UX consolidation                      ⏸ DEFERRED until after B12
```

The old `C1 OPEN / C2 BLOCKED` labels no longer govern current Timeline sequencing. They describe the earlier frontend-only phase before the real product vertical replaced its local/mock assumptions with canonical backend/persistence behavior.

## 3. Current vertical boundary

Frontend work in the active Timeline vertical supports:

```text
Home `+`
→ create/configure canonical temporal state
→ Timeline representation/actions
→ Session/Actual lifecycle where owned by later blocks
→ Responsibility/Participation roles
→ advanced recurrence/reminders
→ replanning/solver proposals
→ final deferred UI/UX consolidation
```

Explicitly outside the current vertical:

```text
external provider integration
native/mobile/offline/multi-device
account-to-account collaboration/chat/shared editing
broad analytics/statistics/signals
```

## 4. Deferred B07 rule

B07 UI/UX Consolidation is intentionally deferred until B08–B12 capabilities exist.

During B08–B12, UI may be utilitarian/temporary but must remain:

```text
truthful to canonical semantics
usable for real-stack/manual testing
accessible enough for the implemented capability
free of fake persistence/provider/runtime success
```

Final presentation/interaction cleanup belongs to B07, not to opportunistic redesign inside every capability block.

## 5. Historical frontend temporal evidence

These files remain useful phase-time evidence but are not current sequencing authority:

- `home/temporal-frontend-roadmap.md`;
- `home/temporal-create-c1-manual-acceptance.md`;
- dated C1 engineering/finding/rearchitecture records;
- T1/F0 freeze documents where they describe the earlier frontend-only architecture.

Where an old document says recurrence materialization/provider integration/backend range query is “future”, current executable/workstream truth now decides what has actually been implemented.

## 6. World Focus

World Focus documentation remains separate from the active Timeline vertical. Read its current/durable contracts under `docs/frontend/home/` only when working on that subsystem.

No Timeline block automatically reopens World Focus visual/product work.

## 7. Permanent semantic boundaries

```text
frontend ViewModel != backend DTO != Domain != persistence row
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Session != Actual
Session != Actual != Outcome
Responsibility != Participation
planned/intended != happened
proposal != accepted effect
projection != canonical truth
AI output != accepted fact/effect
UI hiding != authorization
```

## 8. Engineering authorities

For non-trivial frontend work also inspect:

- `docs/frontend/production-readiness/component-architecture.md`;
- `docs/frontend/production-readiness/backend-integration-contract.md`;
- `docs/frontend/production-readiness/quality-gates.md`;
- `docs/frontend/terminology.md`;
- `docs/frontend/localization.md`;
- `docs/frontend/design-tokens.md`;
- current dependency boundaries and generated-client governance.

## 9. Lifecycle rule

Current contracts/checkpoints describe present truth. Dated evidence and archived phase documents preserve what was true at their checkpoint and must not compete with the active workstream for present-tense sequencing.
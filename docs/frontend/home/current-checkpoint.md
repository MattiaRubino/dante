# DANTE — Home / Frontend Current Checkpoint

**Status:** CURRENT FRONTEND CHECKPOINT — TEMPORAL CANDIDATE RECONCILED  
**Reconciled:** 2026-09-23  
**Protected-main baseline at temporal selection:** Alembic `20260906_18`  
**Active candidate:** `feature/timeline-temporal-operational` / Alembic `20260923_57`

This is the current navigation checkpoint for Home/AppShell/Timeline/Temporal frontend work. Current code/tests and the active Timeline workstream outrank historical frontend-only C1/T1 labels.

## 1. Platform state

The frontend consumes the integrated platform owners for Access/Auth, Recovery, Email, Observability, OpenAPI/API-client boundaries, Intelligence foundation and the real PostgreSQL backend. Frontend code must not replace those owners with local canonical truth for convenience.

## 2. Home / Timeline / Temporal state

```text
Home/AppShell structural foundation             retained
Real Data Spine                                 ✅ B00 CLOSED / PROVEN
Activity Core                                   ✅ B01 CLOSED / PROVEN
Schedule Core                                   ✅ B02 CLOSED / PROVEN
Event Core                                      ✅ B03 CLOSED / PROVEN
Temporal Constraints + Movement Policy          ✅ B04 CLOSED / PROVEN
Life Area / Tags                                ✅ B05 CLOSED / PROVEN
Routine / Recurrence / Occurrence               ✅ B06 CLOSED / PROVEN

B08 Session Runtime                             ← NEXT
B09 Responsibility / Participation              ⬜
B10 Actual / Outcome / Confirmation              ⬜
B11 Advanced Recurrence / Reminder              ⬜
B12 Replanning / Conflict / Solver              ⬜
B07 UI/UX Consolidation                         ⏸ DEFERRED
B15 Whole Vertical Closure                      ⬜
```

The old frontend-only labels:

```text
C1 OPEN
C1 MANUAL PASS NOT GRANTED
C2 BLOCKED
```

are **historical phase-time state**, not current Timeline sequencing authority. B00–B06 replaced the earlier local/pre-backend assumptions with canonical backend/persistence behavior and real recurring Timeline state.

## 3. Current authority

For present Timeline work read:

1. `../../workstreams/timeline-temporal-operational-post-b06-scope-decision-2026-09-23.md`;
2. `../../workstreams/timeline-temporal-operational-roadmap.md`;
3. `../../workstreams/timeline-temporal-operational-map.md`;
4. `../../workstreams/timeline-temporal-operational-handoff.md`;
5. `../../database/timeline-temporal-operational.md`.

Historical frontend Temporal files remain useful for design rationale only when they do not conflict with the current workstream or executable truth.

## 4. Current vertical boundary

```text
Home `+`
→ create/configure canonical state
→ Timeline projection/actions
→ required Session/Actual lifecycle
→ Responsibility/Participation roles
→ advanced recurrence/reminders
→ replanning/conflict/solver proposals
→ final deferred UI/UX consolidation
```

Out of scope for the active vertical:

```text
external provider integration
native/mobile/offline/multi-device
account-to-account collaboration/chat/shared editing
broad analytics/statistics/signals
```

## 5. Deferred B07 behavior

The UI is allowed to remain visually provisional during B08–B12 so capability work is not repeatedly redesigned. Temporary UI still must be truthful, usable for real manual testing, and must not invent canonical/provider/runtime success.

Final consolidation of `+`, editors, Timeline actions, lifecycle controls, responsibility/participation, advanced recurrence/reminders and solver proposals belongs to B07 after B12.

## 6. Permanent temporal distinctions

```text
Activity != Event != Routine
Routine != Recurrence != Occurrence
Occurrence != Schedule
Schedule != Temporal Constraint != Movement Policy
Schedule != Session != Actual
Session != Actual != Outcome
Actual != Outcome != Confirmation
Responsibility != Participation
planned/intended != happened
proposal != accepted effect
Timeline ViewModel != application model != DTO != DB row
provider identity/state != canonical DANTE identity/state
```

## 7. World Focus boundary

World Focus remains a separate subsystem. Its historical/current contracts are not automatically reopened by Timeline work. Any future World Focus implementation resumes from then-current authority under a separately authorized scope.

## 8. Next product gate

The next active Timeline gate is **B08 Session Runtime pre-scope** from the proven `_57` frontier.

No provider integration, native app, collaboration system, broad analytics, Actual semantics or speculative schema expansion is implicitly authorized by B08.
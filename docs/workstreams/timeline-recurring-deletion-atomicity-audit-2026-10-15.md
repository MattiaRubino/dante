# Temporal hard deletion — atomicity and ownership audit (2026-10-15)

**Status: CURRENT ENGINEERING BLOCKER / TEST DESIGN, NOT IMPLEMENTATION PROOF.**
Branch inspected: `feature/timeline-temporal-operational` at `4c68a78c`.
Normative product contract: `docs/domain/decisions/activity-session-operational-lifecycle-v2.md`.
This review applies to one-off and recurring Activity **and** Event; the same product
choices do not imply identical persistence owners.

## Verified current implementation boundaries

1. `dante.delete_self_activity_lifecycle_graph` (Alembic `_147`) starts
   from an owner-checked Activity and its real Sessions, then traverses FK
   descendants. `_148` adds fingerprint-guarded Activity deletion but rejects
   recurring instances. This function cannot be invoked with a Routine, Event
   source, or Occurrence id as though it were an Activity.
2. `dante.skip_self_occurrence` (Alembic `_55`) records a durable technical
   skip for an existing Occurrence. The `_111`
   `dante.bind_self_routine_occurrence_activity` implementation does **not**
   check `dante.occurrence_skip` before binding an Activity.
3. `RoutineOccurrenceMaterializationApplication._materialize_activity`
   calls Activity creation, dependent setup, and final occurrence binding as
   separate application operations with separate transactions. Binding is
   deliberately last and is the existing completion marker.
4. Recurring Event uses one canonical Event **source** plus individual
   Occurrences. Deleting one Event instance must not delete the shared Event
   source or a sibling; deleting the source must cover all descendants and
   future generation. `EventInspectorActions` currently does not expose a
   proven hard-delete workflow.
5. A generic Schedule removal/Undo is not an Activity coordinated unschedule
   transaction. Hard delete must not be implemented by unscheduling, and
   unschedule must never erase real Session, attendance, Actual or Outcome.

## Blocking race: partial materialization

Example: transaction A creates a generated Activity before binding it to its
Occurrence; transaction B removes the already-bound instance and records skip.
A later A bind or repair can otherwise recreate a deleted link or leave an
unbound orphan. Merely locking the deletion SQL, adding a UI confirmation, or
checking `occurrence_skip` during a prior read is insufficient.

**Required fix before exposing destructive endpoints:** materialization's
creation/configuration/binding must have one durable admission/commit boundary
or an equivalent database-enforced reservation + repair protocol; deletion,
skip, checkpoint and binding must serialize on the same owner/source/Occurrence
identity. The final admission must re-check current skip/deleted-source state
inside the transaction. A failed or interrupted materialization must not
leave a live orphan Activity or Event placement.

## Invariants required of the implementation

- **Owner and identity:** verify the self actor, current source/Occurrence,
  profile/material revisions, exact child ownership and fresh Session/factual
  impact before mutating. Never infer Event ownership from an Activity link.
- **Single instance:** Activity: full selected Activity-owned graph removed,
  source Routine + sibling Occurrences/Activities retained, durable technical
  exclusion. Event: only the selected Occurrence-owned graph removed,
  source Event and siblings retained, technical exclusion prevents re-creation.
  Preserving minimum Occurrence skip identity is a technical prevention record,
  not a retained Activity/Event.
- **Whole series:** delete source Routine/Event, all recurrence history,
  checkpoint/Occurrence instances (including unplaced and past instances),
  generated Activity graphs and Event-instance graphs; future checkpoint must
  neither discover nor recreate the source. Do not infer affected rows from
  only a limited visible Timeline/window.
- **One-off Event/Activity:** hard delete canonical object and its owned graph,
  including dependent reminders, objectives and factual data. Foreign actor
  records and independent People/Life Areas/shared entities must not be
  destructively traversed; unsupported cross-owner dependencies fail closed.
- **CAS/replay:** stale preview, reused conflicting operation id, new attempt
  or factual revision, and race with start/stop/checkpoint must reject without
  partial deletion. Replaying an accepted deletion must not cause a second
  effect. A single failure rolls back all row removals and skip/exclusion.
- **Scheduling:** remove/Undo changes only accepted placement with an
  independently guarded, coordinated command. Hard delete is irreversible
  product action and has no generic Undo.
- **PostgreSQL authority:** SECURITY DEFINER routines with minimal EXECUTE,
  never runtime table DELETE, forward-only Alembic, exact Dictionary/ORM
  parity, migration/catalog/ACL proofs and no disabled FK/constraint triggers.

## Mandatory acceptance cases before close

| ID | Scenario | Proof |
| --- | --- | --- |
| TD-01 | Delete unplaced one-off Activity including named + open/paused/ended Sessions and Objectives | PostgreSQL owner/negative/rollback + readback |
| TD-02 | Solo questa generated Activity: sibling retained; repeat checkpoint and window change do not recreate | PostgreSQL fresh/replay + authenticated browser |
| TD-03 | Tutta la serie Activity: all materialized + unmaterialized/future, mixed Sessions/Reminders/Objectives | PostgreSQL exact source/child reads + repeat checkpoint |
| TD-04 | Delete one-off Event: agenda/participation/attendance/Schedule/Objective/Actual/facts only for owner | PostgreSQL negative owner/shared refs + browser |
| TD-05 | Solo questa Event Occurrence: source, other Occurrences, participation and their states unchanged | PostgreSQL + recurrence projection + browser |
| TD-06 | Tutta la serie Event: source, current and previously generated instances, history and future checkpoint | PostgreSQL negative owner + browser |
| TD-07 | Concurrent checkpoint/materialize vs single/series delete; kill or error between creation and binding | Competing transactions / forced rollback; no orphan or resurrection |
| TD-08 | New Session/attendance/Actual, stale fingerprint/revision, repeated/conflicting operation id | Serializable conflict + unchanged rows after refusal |
| TD-09 | Cross-actor linking and independently owned Person/Life Area; FK cycle | Fail closed, unrelated records retained |
| TD-10 | Unschedule/undo Activity and Event with factual history, and hard-delete Undo denial | Real PostgreSQL + authenticated Chromium |
| TD-11 | Post-delete inspector, Timeline, review queue and generated client contracts | Vitest + real stack + reload |
| TD-12 | Exact full repository gate on one final SHA and real-app dogfood | 27 groups + manual acceptance, independently recorded |

A unit test or a historical browser PASS does not substitute for PostgreSQL,
real-stack and full 27-group proof on the same final source. This audit is
not permission to ship a partial destructive capability.

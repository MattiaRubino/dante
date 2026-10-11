# B14 Logical Overlay — Independent Session, Objective Draft, Home Workspace

**Past review extension candidate (_142):** one derived Activity review per owner with a past accepted interval and no recorded execution/Actual when explicit review policy requests it. A pending Objective on that past Activity enters Objective review even without a Session. The queue remains a read projection; a manual Session, Actual decision, or Objective confirmation is written by its own existing capability. A missed plan stays unknown until explicit action. Cumulative user-local PostgreSQL gate passed; real-app acceptance is open.

- **Status:** ACCEPTED DOWNSTREAM REPRESENTATION OF APPROVED PRODUCT CONTRACT; implementation source at Alembic `20261010_141`; technical proof cumulative user-local PASS; real-app UI acceptance open.
- **Date:** 2026-10-11
- **Product/Domain authority:** `docs/domain/decisions/activity-session-live-timeline-v1.md` §8 and `docs/domain/concepts/session.md`
- **Accepted baseline:** `docs/logical-model/whole-logical-model-v1.md`
- **Earlier scoped overlay:** `activity-subactivity-session-bounded-v1.md` (2026-10-02, still valid for decomposition)
- **Physical implementation overlay:** `../../physical-model/b14-session-objective-home-workspace-2026-10-11.md`

## 1. Stable identities / semantic non-collapse

Activity, planned Schedule slice, Session execution attempt, Actual, Objective, Observation/Evaluation, Outcome and Confirmation remain independently identified. A planned Session slice is a provenance link to a Schedule, **not** an already-executed Session. An Activity can have zero or more actual Session attempts, and zero or more planned slices. No `Session -> Session` ownership hierarchy is introduced.

An optional **main Activity live Session** and zero or more **planned internal Session executions** are distinguished by provenance and explicit Activity execution policy, not by an invented nested Session relation. If the main capture mode is `disabled` or `record`, an explicitly owned planned slice is still eligible for live Session execution under its own Schedule admission; the generic Activity live clock stays disabled. With main `live`/`record_and_live`, a child requires main running and the main Pause/Stop cascade is one accepted operation; resuming the main does not resume children. No inverse cascade.

**Qualification of earlier logical overlay §10:** the older sentence “disabled = no Activity-owned Session capture surface” described the **generic Activity clock** and does not prohibit explicitly planned Session slices under the newer approved contract. It must not be enforced as a ban on all Session activity.

## 2. Objective input is not Result

One Objective can have **at most one current provisional input**, scoped to its authorized actor. A mutable versioned draft persists across page refreshes and has no Observation or Evaluation authority. An explicit confirmation consumes its current version and creates exactly one accepted canonical ObjectiveResult transactionally. The confirmation receipt supports replay without duplicate observations; once confirmed, correction uses the existing canonical Objective correction capability, not editing that draft.

A draft lifecycle record is a technical state/control object, **not** another Objective or alternate truth for Outcome/Actual.

## 3. Derived Home views

- **Conclusi:** bounded, actor-owned read of real ended Session attempts and explicitly occurred Actuals. “Sessione conclusa” does not imply “Attività completata”.
- **Da verificare:** existing B10 governed review/reconciliation semantics; a planned interval expiring without Play is not automatically a failure or an Actual.
- **Obiettivi:** bounded read of Objective identities without a confirmed Observation, with staged-input metadata; one shared result writer in Inspector and Home.

These are projections (LR-08), not new canonical owners or hidden background tasks. The current Home surface reads up to 40 items per view; runtime APIs enforce a 100-item hard cap. A full paginated archive is a separate product requirement.

## 4. History, authority, tests

State transitions use actor-guarded PostgreSQL capability functions, canonical UUIDv7 identifiers and CAS/idempotent operation keys. The approved Schedule is never shifted by real Session timing. The tested Alembic branch head is `20261010_141` with cumulative user-local database, Dictionary and API/client/browser checks reported green; **the real Home acceptance gate remains open**. This overlay is additive: do not rewrite the closed Whole Logical Model baseline or claim protected-main integration.

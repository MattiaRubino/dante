# Timeline / Temporal-Operational — B13-C Execution Structure Constraints scope

- **Status:** APPROVED — semantic and discovery scope frozen; implementation gate separate
- **Date:** 2026-09-29
- **Branch:** `feature/timeline-temporal-operational`
- **Pre-scope HEAD:** `2e19deaf61e05766ddfad096b234efc48c8fcaa1`
- **Previous gate:** B13-B CLOSED / focused PostgreSQL and catalog proof at Alembic `20260928_90`
- **Parent:** B13 Work Structure / Decomposition / Dependencies
- **CI:** not authorized; the user runs local gates

## 1. Purpose and authority

B13-C makes execution structure explicit for work organized by a self-owned Plan. The first relevant context is a current Plan Step linked to an existing, distinct Activity. The Plan supplies organizational context; the Activity keeps its own identity, Schedule, Session and Actual. An unlinked structural Step has no fabricated execution history.

Sources: `docs/product/v1-scheduling-flexibility.md` (Session structure and compatible planned merging), `docs/domain/concepts/activity.md` (divisibility and execution policy), `docs/domain/concepts/session.md` (truthful execution and correction lineage), `docs/domain/concepts/temporal-constraint.md` plus Part 2 (duration, spacing, recovery and relative geometry), `docs/logical-model/slices/time-reality-v1.md`, `docs/logical-model/representation-framework-v1-part-2.md`, the current B04/B08 temporal constraint and Session implementations, and the B13-A/B closure records.

The intended result is a bounded, user-visible author/read/evaluate path for supported execution-structure rules. No editable field is allowed to be collected and then ignored. This scope freezes semantic boundaries and acceptance criteria; the physical representation and exact supported subset are decided in the implementation discovery before DDL.

## 2. Distinct kinds of execution truth

```text
Plan / Step execution intent
!= Activity identity
!= accepted Schedule placement
!= performed Session
!= Actual realization / Outcome
```

A maximum intended number of Sessions or an indivisibility choice describes how work is planned to be divided. It does not cap the number of truthful Session records that may later be captured. Existing Sessions are facts even when they exceed a hard planning limit; a violation is diagnosed rather than rejected or erased. Ending a Session does not establish completion.

The accepted Schedule may have a different structure from a candidate arrangement. The number of historical Sessions must not be used as a proxy for planned Session count, nor may a Plan-specific count silently include Activity execution attributed to another context when that attribution cannot be established. The implementation must specify the exact candidate or accepted-planning basis being counted.

## 3. Bounded execution-structure rules

The discovery must test these capabilities against current canonical subjects and persistence before selecting an implementation:

1. **Divisibility and optional maximum intended Session count.** The user may express whether work can be divided and, where a meaningful planning-slice basis exists, a positive upper bound on the intended count. No bound means unrestricted by this rule. Indivisible must have a clear relationship to the bound of one; contradictory settings are rejected. A count is assessed against the specified planning basis, never by denying Session capture.
2. **Compatibility of proposed execution slices.** Product language permits combining compatible *planned* work slices. Compatibility is a bounded, explicit planning assessment; it neither merges real Session identities nor creates an accepted Schedule. An assessment may report incompatible or unknown when required context is missing. Do not infer compatibility merely from adjacent times or Step order.
3. **Duration, spacing, preparation and recovery.** These are temporal rules owned by Temporal Constraint. B13-C must inspect B04/B08 current authoring and evaluation contracts, then reuse them when their subject, temporal facet and planning basis match. The existing duration family can be extended only with a separately justified, typed forward representation. There must be no second Plan-owned numeric spacing or recovery field that competes with Temporal Constraint.
4. **Plan scope and linked Activity.** Resolve which rules are effective for the linked Activity in a Plan without silently changing an Activity used elsewhere or duplicating inherited rules onto every Step. If source attribution, effective-scope precedence or candidate-slice identity is unavailable, report that limitation and do not claim an evaluation of that case.

Two meanings of “merge Session” remain separate:

```text
combine compatible proposed slices = planning assessment
correct two already recorded Sessions = Session correction with lineage
```

The latter belongs to the existing Session/History domain and is not implemented by this gate.

## 4. Implementation discovery required before DDL

Record, with repository references:

1. the current B13-A Plan/Step identity and replacement/current-history path, B13-B active endpoint guards, B04 Temporal Constraint subject/facet/duration support, B08 Session links, and the exact accepted Schedule representation;
2. the smallest justified owner and address for any independent execution policy, including whether it is Plan-contextual or Activity-wide; how multiple Plans containing one Activity avoid contradictory or silently aggregated policy;
3. the precise meaning of an intended Session count: what is counted, on which candidate or accepted planning snapshot, how correction/replay is handled, and what happens when no candidate slice model exists;
4. how a compatibility check gets a real pair of proposed slices and enough bounded context, without inventing completed execution or an implicit solver;
5. which temporal rule variants have an implemented evaluator today, which need a forward extension of Temporal Constraint, and which remain explicitly unavailable;
6. user-visible hard/soft interpretation and evaluation status, including missing basis, conflicts and infeasibility; no invented “valid” result from unknown inputs;
7. the exact protected PostgreSQL write/read path, history/CAS/idempotency and Dictionary/ORM/catalog changes if a new persistent rule is warranted; the minimal HTTP/client/UI surface;
8. a capability ledger for maximum count, merge compatibility, spacing, preparation and recovery: **implemented and proven**, **truthful handoff to the existing owner**, or **unsupported and not editable**. A requirement cannot be silently checked off because its name appears in the UI.

If no coherent canonical planning basis exists for a proposed rule, record the blocker before implementation rather than persisting a decorative policy.

## 5. Product and mutation boundary

The Home Plan/Step surface may author a supported rule and show its effective scope, strength where applicable, current value and assessment with a reason. An authored Plan rule must survive refresh through canonical reads. A Temporal Constraint must use its existing owner and guard. Avoid duplicating a rule in both Plan and Activity storage without explicit precedence semantics.

An assessment is read-only and must identify the input planning snapshot or candidate shape it assessed. It does not accept a Proposal, reschedule an Activity, combine persisted Schedule records, start or end a Session, or create an Actual/Outcome. A hard planning constraint governs admission of a future proposal under authority rules; recorded reality remains recordable.

## 6. Explicit non-goals

```text
automatic scheduling, replanning, optimization or Proposal acceptance (B12)
whole B13 A/B/C integrated dogfood and real-app acceptance (B13-D)
generic work-item/graph ontology or new universal constraint root
new Dependency qualifiers or derived global blocked state
Session split/merge correction and historical lineage implementation
automatic merge of planned slices or accepted Schedules
blocking or deleting truthful Session/Actual after a planning-rule violation
unbounded inheritance or cross-Plan rule precedence without source authority
B07 UI redesign or B14 Create completeness sweep
```

## 7. Acceptance gate

1. The implementation checkpoint states the exact supported capability set and unavailable cases before persistence work. Each supported authorable value has a defined owner, planning basis and readback path.
2. A user can create/revise/retire and read supported persistent rules with self ownership, replay safety, expected-current protection and historical trace where material. Foreign Plan, Step, Activity and stale references fail deterministically.
3. An indivisible or maximum-count rule is evaluated against explicitly supplied or accepted *planned* slices. Boundary cases, missing basis and contradictory settings have deterministic results. Actual Session capture remains possible when the planned limit is exceeded.
4. A supported compatibility assessment distinguishes proposed-slice combination from Session correction; insufficient evidence stays unknown. No hidden Schedule/Session mutation occurs.
5. Supported spacing, preparation, recovery and duration assessments use Temporal Constraint semantics, preserve hard/soft and temporal facet, and distinguish accepted Schedule from actual execution. Cases without a canonical representation are unavailable in authoring and documented in the capability ledger.
6. B13-A structure and B13-B qualified Dependencies remain stable, including active endpoint protection and current derived evaluations. Dependency satisfaction does not imply temporal admissibility.
7. Any persistence change uses forward-only Alembic, guarded runtime privileges, Dictionary and SQLAlchemy mapping reconciliation, and exact PostgreSQL catalog proof. HTTP/OpenAPI, generated-client determinism, web tests and typechecks cover all public values.
8. The user runs the focused local PostgreSQL and web gates; roadmap, map, handoff and database overlay record measured results before B13-C closes. CI/GitHub Actions are not used.

The integrated real-app B13 acceptance is B13-D. B12 remains held until B13-D closes.

## 8. Git scope of this freeze

```text
BRANCH
feature/timeline-temporal-operational
PRE-SCOPE
2e19deaf61e05766ddfad096b234efc48c8fcaa1
CREATE
docs/workstreams/timeline-temporal-operational-b13-c-scope-2026-09-29.md
UPDATE
none
DELETE
none
PURPOSE
freeze B13-C execution-structure boundaries, discovery and acceptance
EXPLICITLY OUT OF SCOPE
implementation, migrations, API, client, UI, B13-D and B12
```

Implementation requires a separate exact-path write gate under `docs/development/agent-operating-manual.md` §5.

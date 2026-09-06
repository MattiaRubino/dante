# DANTE Pre-Vertical Foundation

- **Status:** ACTIVE BRANCH WORKSTREAM
- **Branch:** `feature/pre-vertical-foundation`
- **Baseline:** `main@5258452d7bd4e7a2797922b00035a9068ba41167`
- **Purpose:** close the small cross-cutting seams needed before the first real product vertical, without turning this branch into the vertical itself.

## Scope

This branch prepares DANTE so the first vertical can start with correct identity, time, authenticated user context, realistic dogfooding and repeatable scale/testing support.

The work is intentionally compact and grouped into four milestones.

## PV-01 — Identity, Clock and Time

Establish the canonical backend primitives that future verticals must reuse:

- application-issued UUIDv7 generation with typed references where justified;
- backend `Clock` contract with real and deterministic test implementations;
- IANA timezone handling (`Europe/Rome`, not fixed UTC offsets);
- explicit distinction between user/default display timezone and the temporal semantics owned by Schedule/Event/Routine data;
- deterministic handling/tests for local-day windows, DST gaps/overlaps and ambiguous/nonexistent local times;
- no semantic chronology/currentness derived from UUID ordering.

This milestone must reuse the existing DANTE temporal/database semantics rather than introduce a parallel generic time framework.

## PV-02 — Authenticated DANTE User Context

Close the seam from an authenticated Access/Auth account to the DANTE context required by product operations.

The contract must preserve the existing separations:

`Person != Account != Principal != Actor`

It must determine, without semantic collapse:

- how an authenticated request resolves its DANTE-facing context;
- how the relevant domain/person/world scope is represented;
- where the user's default timezone belongs;
- how future application/API code consumes that context consistently.

A database/Alembic change is allowed only if this seam proves that one is semantically required. No generic `user_id` ownership model may be added merely for convenience.

### PV-02 branch-local candidate

The current branch materializes the minimum concrete seam through:

- `20260906_18` and `dante.account_application_context`;
- a bounded `ensure_account_application_context(uuid,uuid)` capability that preserves the existing runtime denial of generic `Person` creation;
- typed backend `DanteContext` resolution from an admitted `Principal`;
- reuse of the PV-01 `TimeZonePolicy` primitives for `follow_device` and fixed named-IANA policy;
- governed Web transport of the current device timezone through `X-Dante-Time-Zone`;
- real PostgreSQL tests for ACL, first-use idempotence/concurrency and timezone persistence integrity.

Detailed branch-local authority: `../architecture/authenticated-dante-context.md`.

This is implementation candidate state, not protected-main closure evidence. PV-02 acceptance remains subject to the branch test/QA and PV-04 closure gates.

## PV-03 — Dogfood, Personas and Scale Readiness

Create the minimum reusable development/test capability needed to exercise DANTE as it grows:

- one persistent LOCAL/DEV dogfood account for real ongoing use;
- deterministic synthetic personas/scenarios for normal, temporal-edge and historical cases;
- credentials/secrets kept outside Git;
- preserve the existing disposable PostgreSQL integration-test harness rather than replacing it;
- deterministic scale profiles that can grow from small datasets toward larger history/account/object volumes;
- support for a long-lived synthetic history/canary where useful.

This milestone provides generation/readiness infrastructure only. Product-specific load workloads, concurrency profiles and performance budgets are added by the vertical that owns them.

## PV-04 — Whole-Branch Acceptance and Closure

Before integration, prove that the branch is a safe foundation rather than a hidden product expansion:

- unit/integration and real PostgreSQL validation appropriate to the changed code;
- architecture and semantic-boundary checks;
- no regression of Access/Auth, Database/Alembic, Recovery, Email, Observability, Intelligence/Search or existing frontend foundations;
- exact changed-path/scope QA against the approved branch scope;
- reconcile with then-current protected `main` before PR when required;
- required repository gates must pass on the final PR head;
- only after protected-main merge/readback may the workstream be retired/closed.

## Explicitly out of scope

This branch does **not** implement the first product vertical. In particular it does not pre-build:

- `/v1/timeline` or other product Timeline APIs;
- generic Activity/Event/Routine CRUD;
- Session lifecycle product endpoints;
- Actual/Outcome product surfaces;
- a new `Execution` concept;
- generic CAS/versioning or generic idempotency frameworks;
- product-specific performance tuning/load workloads before the owning vertical exists;
- real AI/Search product integration;
- opportunistic redesign of existing CP1–CP6, Access/Auth, Recovery, Email, Observability or frontend foundations.

## Completion condition

The branch is ready to close when a future vertical can start from one coherent foundation where:

```text
authenticated account
→ resolved DANTE user/domain context
→ correct default timezone/time semantics
→ canonical UUIDv7 + Clock primitives
→ persistent dogfood use
→ deterministic personas
→ scalable synthetic data foundation
```

At that point the next branch should implement a deliberately bounded **first real vertical**, and any CAS/idempotency/performance rules should be designed against its concrete operations rather than generalized in advance.

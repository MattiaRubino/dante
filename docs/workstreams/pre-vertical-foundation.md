# DANTE Pre-Vertical Foundation

- **Status:** ACTIVE BRANCH WORKSTREAM
- **Branch:** `feature/pre-vertical-foundation`
- **Baseline:** `main@5258452d7bd4e7a2797922b00035a9068ba41167`
- **Purpose:** close the small cross-cutting seams needed before the first real product vertical, without turning this branch into the vertical itself.

## Scope

This branch prepares DANTE so the first vertical can start with correct identity, time, authenticated user context, realistic dogfooding and repeatable scale/testing support.

The work is intentionally compact and grouped into four milestones.

## PV-01 — Identity, Clock and Time

- **Branch-local status:** IMPLEMENTED / MILESTONE COMPLETE

Establish the canonical backend primitives that future verticals must reuse:

- application-issued UUIDv7 generation with typed references where justified;
- backend `Clock` contract with real and deterministic test implementations;
- IANA timezone handling (`Europe/Rome`, not fixed UTC offsets);
- explicit distinction between user/default display timezone and the temporal semantics owned by Schedule/Event/Routine data;
- deterministic handling/tests for local-day windows, DST gaps/overlaps and ambiguous/nonexistent local times;
- no semantic chronology/currentness derived from UUID ordering.

This milestone reuses the existing DANTE temporal/database semantics rather than introducing a parallel generic time framework.

Whole-branch executable acceptance and protected-main closure remain owned by PV-04.

## PV-02 — Authenticated DANTE User Context

- **Branch-local status:** IMPLEMENTED / MILESTONE COMPLETE

Close the seam from an authenticated Access/Auth account to the DANTE context required by product operations while preserving:

`Person != Account != Principal != Actor`

The implemented contract provides:

- authenticated request → DANTE-facing application context;
- explicit Account → self Person linkage without collapsing Account into Person;
- user/default timezone policy separate from object-owned temporal semantics;
- one stable backend context contract for future product/API operations.

No generic `user_id` ownership model was introduced.

### PV-02 implemented branch contract

The branch materializes the minimum concrete seam through:

- `20260906_18` and `dante.account_application_context`;
- a bounded `ensure_account_application_context(uuid,uuid)` `SECURITY DEFINER` capability that preserves the runtime denial of generic `Person` creation;
- first-use serialization on the owning Account so concurrent initialization returns one self Person/context;
- application-issued UUIDv7 for the initial self Person;
- typed backend `DanteContext` resolution from an admitted `Principal`;
- reuse of PV-01 `TimeZonePolicy` for `follow_device` and fixed named-IANA policy;
- governed Web transport of the current device timezone through `X-Dante-Time-Zone`;
- fail-closed distinction between malformed device timezone input and corrupted persisted timezone/context state;
- fail-closed Alembic downgrade when a live Account↔Person semantic binding exists;
- PostgreSQL acceptance tests covering ACL, first-use idempotence/concurrency, timezone integrity and downgrade safety.

Detailed branch-local authority: `../architecture/authenticated-dante-context.md`.

`self_person_ref` is a homogeneous reference to `Person`, so its canonical DB integrity is the direct FK to `dante.person`. `native_address` remains the bounded address/control projection used by genuinely heterogeneous NativeRef consumers; the bootstrap capability also creates the Person address atomically, but the application-context FK does not need to reinterpret `native_address` as a mandatory semantic parent for every Person.

PV-02 implementation is complete on this branch. This is **not** a claim that the branch has passed protected-main integration, final CI or recovery acceptance: those proofs are deliberately centralized in PV-04.

## PV-03 — Dogfood, Personas and Scale Readiness

- **Branch-local status:** NEXT / NOT STARTED

Create the minimum reusable development/test capability needed to exercise DANTE as it grows:

- one persistent LOCAL/DEV dogfood account for real ongoing use;
- deterministic synthetic personas/scenarios for normal, temporal-edge and historical cases;
- credentials/secrets kept outside Git;
- preserve the existing disposable PostgreSQL integration-test harness rather than replacing it;
- deterministic scale profiles that can grow from small datasets toward larger history/account/object volumes;
- support for a long-lived synthetic history/canary where useful.

This milestone provides generation/readiness infrastructure only. Product-specific load workloads, concurrency profiles and performance budgets are added by the vertical that owns them.

## PV-04 — Whole-Branch Acceptance and Closure

- **Branch-local status:** NOT STARTED

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

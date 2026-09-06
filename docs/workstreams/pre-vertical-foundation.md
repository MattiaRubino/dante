# DANTE Pre-Vertical Foundation

- **Status:** ACTIVE BRANCH WORKSTREAM
- **Branch:** `feature/pre-vertical-foundation`
- **Baseline:** `main@5258452d7bd4e7a2797922b00035a9068ba41167`
- **Purpose:** close the small cross-cutting seams needed before the first real product vertical, without turning this branch into the vertical itself.

## Scope

This branch prepares DANTE so the first vertical can start with correct identity, time, authenticated user context, realistic dogfooding, deterministic personas and repeatable scale/testing support.

The work is intentionally compact and frozen into exactly three milestones:

```text
PV-01 — Identity / Clock / Time
PV-02 — User Context / Dogfood / Personas
PV-03 — Scale Harness / QA / Closure
```

QA findings do not create new milestones. Bugs found inside one milestone are fixed inside that milestone; whole-branch acceptance and integration remain PV-03.

## PV-01 — Identity / Clock / Time

- **Branch-local status:** DONE

Establish the canonical backend primitives that future verticals must reuse:

- application-issued UUIDv7 generation with typed references where justified;
- backend `Clock` contract with real and deterministic test implementations;
- IANA timezone handling (`Europe/Rome`, not fixed UTC offsets);
- explicit distinction between user/default display timezone and the temporal semantics owned by Schedule/Event/Routine data;
- deterministic handling/tests for local-day windows, DST gaps/overlaps and ambiguous/nonexistent local times;
- no semantic chronology/currentness derived from UUID ordering.

This milestone reuses the existing DANTE temporal/database semantics rather than introducing a parallel generic time framework.

## PV-02 — User Context / Dogfood / Personas

- **Branch-local status:** DONE / IMPLEMENTATION COMPLETE

PV-02 closes the authenticated DANTE user-context seam and adds the minimum durable LOCAL/DEV data needed to exercise that seam repeatedly before a product vertical exists.

Executable whole-branch acceptance is deliberately centralized in PV-03; PV-02 completion here means the bounded implementation, documentation and exact-scope QA are complete, not that final branch CI/recovery/main integration has already run.

### A. User Context

- **Status:** DONE

The implemented contract preserves:

`Person != Account != Principal != Actor`

and provides:

- authenticated request → DANTE-facing application context;
- explicit Account → self Person linkage without collapsing Account into Person;
- user/default timezone policy separate from object-owned temporal semantics;
- one stable backend context contract for future product/API operations;
- `20260906_18` and `dante.account_application_context`;
- bounded `ensure_account_application_context(uuid,uuid)` capability while generic runtime `INSERT Person` remains denied;
- first-use serialization on the owning Account;
- application-issued UUIDv7 for the initial self Person;
- typed backend `DanteContext` resolution from an admitted `Principal`;
- reuse of PV-01 `TimeZonePolicy` for `follow_device` and fixed named-IANA policy;
- governed Web transport through `X-Dante-Time-Zone`;
- fail-closed distinction between malformed device timezone input and corrupted persisted context state;
- fail-closed Alembic downgrade when a live Account↔Person binding exists.

Detailed branch-local authority: `../architecture/authenticated-dante-context.md`.

`self_person_ref` is a homogeneous reference to `Person`, so its canonical DB integrity is the direct FK to `dante.person`. `native_address` remains the bounded address/control projection used by heterogeneous NativeRef consumers. The bootstrap capability also creates the Person address atomically, but PV-02 does not reinterpret `native_address` as a mandatory semantic parent for every Person.

### B. Dogfood

- **Status:** DONE

The branch now provides a persistent LOCAL/DEV dogfood bootstrap under `apps/backend/tooling/pre_vertical_foundation/`.

It:

- targets the ordinary persistent LOCAL/DEV DANTE database, never the disposable pytest database;
- reuses canonical Access/Auth `normalize_email` and `PasswordKdf` behavior;
- creates canonical Account + verified EmailIdentity + PasswordCredential state only when absent;
- is idempotent by canonical email identity;
- preserves the same Account and self Person on rerun;
- rejects incompatible/disabled/non-password existing state instead of silently rewriting it;
- rejects a different supplied password instead of silently resetting credentials;
- initializes self Person/application context through the existing PV-02 runtime capability;
- requires normal runtime database/password-pepper configuration plus separate `*.local` password/migrator secret files;
- fails closed unless `DANTE_ENV` is exactly `local` or `dev`;
- never prints password, pepper or database credential material.

No Access/Auth API, schema or login/signup semantics were changed for dogfood support.

Detailed operational contract: `../development/pre-vertical-dogfood-personas.md`.

### C. Personas

- **Status:** DONE

The branch defines exactly three deterministic, product-independent foundation personas:

- `normal` — ordinary current-use timezone/context behavior;
- `temporal_edge` — New York DST gap/overlap plus fixed-zone/device-zone independence;
- `historical` — explicit 2016→2026 history anchors independent of UUID ordering.

Persona Account/self-Person references are stable synthetically generated UUIDv7 values for repeatable fixtures only. UUID ordering is never semantic chronology/currentness authority.

Persona materialization is optional and LOCAL/DEV only. It reuses the same canonical Auth seed primitive and PV-02 context capability, specializes only the pristine `follow_device` timezone default when a fixed synthetic policy is required, and refuses to overwrite incompatible existing deterministic state.

No Timeline, Activity, Event, Routine, Session, Actual or other vertical-specific records are created.

Bounded tests were added for:

- LOCAL/DEV-only environment guards and canonical runtime identity;
- canonical password-pepper configuration and `*.local` secret discipline;
- deterministic UUIDv7 persona identity;
- real Rome/New York ordinary/gap/overlap timezone classification;
- fixed timezone independence from current device zone;
- real PostgreSQL account/context materialization and rerun idempotence;
- wrong-password fail-closed behavior without credential rewrite;
- deterministic persona timezone persistence.

The real PostgreSQL test reuses the existing DANTE PostgreSQL 18.6 disposable acceptance harness; PV-02 does not introduce a second database-test framework.

### PV-02 exact-scope result

PV-02 Dogfood/Personas was implemented from approved pre-scope:

`464b198751e4637ebd2e6e32dbd75c2d7d275cc1`

The post-implementation compare is linear and contains only approved Dogfood/Personas tooling, tests, quality configuration and documentation paths. No Alembic, CP6, Access/Auth source, Recovery or product-vertical path was changed by this PV-02 sub-scope.

## PV-03 — Scale Harness / QA / Closure

- **Branch-local status:** NEXT / NOT STARTED

### A. Scale Harness

Create deterministic scale/readiness support that reuses PV-02 personas and the existing disposable PostgreSQL acceptance harness:

- deterministic small/medium/large scale profiles;
- controlled growth in synthetic Accounts, native identities and history-oriented foundation data;
- optional long-lived synthetic canary/history where useful;
- no product-specific workload, concurrency model or performance budget before the owning vertical exists.

### B. Whole-Branch QA

Prove that the branch remains a safe foundation:

- backend format/lint/mypy/unit/integration validation;
- real PostgreSQL 18.6 acceptance using the existing disposable harness;
- Alembic fresh/forward/reversible-path validation and drift checks;
- Database Dictionary/catalog reconciliation;
- frontend lint/typecheck/tests;
- architecture/semantic-boundary checks;
- no regression of Access/Auth, Database/Alembic, Recovery, Email, Observability, Intelligence/Search or existing frontend foundations;
- exact changed-path/scope QA.

### C. Closure

Only after the whole branch is accepted:

- reread then-current protected `main`;
- reconcile the branch with `main` if required;
- run the applicable recovery rehearsal against the final candidate;
- open the bounded PR;
- require repository gates on the final PR head;
- merge with the repository's protected-main policy;
- perform protected-main merge/readback/tree verification;
- reconcile current documentation;
- retire the branch only after protected-main evidence exists.

## Explicitly out of scope

This branch does **not** implement the first product vertical. In particular it does not pre-build:

- `/v1/timeline` or other product Timeline APIs;
- generic Activity/Event/Routine CRUD;
- Session lifecycle product endpoints;
- Actual/Outcome product surfaces;
- a new `Execution` concept;
- generic CAS/versioning or generic idempotency frameworks;
- product-specific performance/load workloads before the owning vertical exists;
- real AI/Search product integration;
- opportunistic redesign of CP1–CP6, Access/Auth, Recovery, Email, Observability or frontend foundations.

Those existing systems are compatibility contracts for this branch and are changed only when a concrete bug in the approved pre-vertical scope requires it.

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

The next branch can then implement one deliberately bounded real vertical, with CAS/idempotency/performance rules designed against concrete operations rather than generalized in advance.

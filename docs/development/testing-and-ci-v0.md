# Testing and CI v0

- Status: **CLOSED / ACCEPTED BACKEND BASELINE**
- Scope: backend automated validation, CI/CD orchestration, repository security and supply-chain evidence
- Frontend testing/CI implementation: **DEFERRED**

## 1. Principle

DANTE testing is organized by **risk and boundary**, not one giant suite or a vanity coverage number.

A PASS claim identifies exactly what was directly executed.

```text
unit PASS
!= PostgreSQL integration PASS
!= migration PASS
!= provider contract PASS
!= UAT PASS
!= recovery PASS
!= complete PSV PASS
```

The Physical post-selection validation register remains authoritative for specialist obligations and stays NOT RUN until direct evidence exists.

## 2. Backend test taxonomy

Use these classes as applicable:

```text
UNIT / DOMAIN
pure semantic/local behavior

APPLICATION
use-case orchestration against explicit fakes/ports

PROPERTY / INVARIANT
Hypothesis generative invariant validation

STATE MACHINE / LIFECYCLE
Hypothesis stateful sequences where operation order matters

ARCHITECTURE
dependency/import/layer constraints

POSTGRESQL INTEGRATION
real DANTE PostgreSQL semantics

MIGRATION
schema evolution and release transition

CONCURRENCY / ATOMICITY
expected-state/idempotency/multi-owner/outbox behavior

PROVIDER CONTRACT
real non-production provider/service integration where needed

HTTP / API CONTRACT
transport routing/validation/error/contract behavior when API exists

PRIVACY / NON-INTERFERENCE
visibility/authority/leakage behavior including WL-H12

SYSTEM / E2E
black-box deployed/runnable journeys

SECURITY / SUPPLY CHAIN
SAST/dependency/secret/container/IaC checks as artifacts appear

PERFORMANCE / RESILIENCE / RECOVERY / PSV
applicable boundary only
```

## 3. Unit/domain tests

Run without network/PostgreSQL/provider SDK/container whenever behavior is pure.

Priority:

- Domain invariants;
- value/reference semantics;
- state transitions;
- planning/temporal logic;
- expected-state decisions;
- idempotency/equivalence logic;
- visibility/authority policy logic once implemented;
- parsing/normalization where semantically material.

Mock only explicit boundaries; do not mock deep implementation simply to manufacture a unit-test shape.

## 4. Application/use-case tests

Use-case tests exercise orchestration with controlled fakes for persistence/clock/provider/identity where appropriate.

They validate sequencing such as:

```text
load
→ validate
→ authority/governance check
→ expected-state/idempotency check
→ change
→ history/outbox staging
→ persistence result
```

without requiring PostgreSQL for every semantic scenario.

## 5. Property and state-machine testing

Use **Hypothesis** where hand-picked examples are weak coverage of the state space.

High-value candidates:

- identifier/reference round trips;
- temporal/range/recurrence boundaries;
- correction/version semantics;
- expected-state conflicts;
- idempotency key reuse conflicts;
- retention/redaction/visibility invariants;
- serialization/normalization round trips;
- lifecycle operation sequences.

Use state-machine testing where sequences such as create/update/revoke/delete/reconcile materially determine correctness.

Properties must encode meaningful invariants, not random input for its own sake.

## 6. Architecture tests

Once code exists, automated checks enforce at least:

```text
domain --X--> FastAPI
domain --X--> SQLAlchemy
domain --X--> provider SDKs
module A --X--> module B private persistence/adapters
production backend --X--> prototypes
```

The lightest reliable enforcement mechanism is preferred. Exact import-boundary tooling is selected during scaffold against the concrete package graph.

## 7. PostgreSQL integration tests

Persistence integration uses **real PostgreSQL 18.4 with the DANTE-selected extension envelope**.

The canonical DANTE LOCAL PostgreSQL image/build is reused for CI integration/migration validation where practical.

Forbidden substitution:

```text
SQLite backend test
claimed as proof of PostgreSQL behavior
```

Validate, as applicable:

- FK/unique/check constraints;
- transaction/rollback behavior;
- SQLAlchemy mapping/Core behavior;
- expected-state/concurrency behavior;
- DB-generated values/types;
- timezone/collation/serialization semantics;
- PostGIS/pgvector/FTS/pg_trgm behavior when used;
- pooling/connection behavior when relevant.

## 8. Test isolation

Tests are independently repeatable.

Use an appropriate isolation strategy per class:

- transaction rollback;
- clean schema/database;
- disposable/ephemeral PostgreSQL instance;
- deterministic synthetic fixtures.

No test depends on ordering or dirty state from a previous test.

## 9. Migration tests

When migrations exist, CI validates:

1. accepted migration graph/head shape;
2. clean PostgreSQL can migrate base → head;
3. required extensions/preconditions exist;
4. SQLAlchemy metadata/schema intent has no unrepresented drift;
5. migration modules import/lint correctly;
6. migration risk classification is present for material changes;
7. destructive/long-running/locking consequences are explicit.

After releases exist:

```text
previous released schema/data
→ new migration chain
→ application smoke/integration
```

UAT rehearses materially risky migrations with representative synthetic or approved sanitized/minimized state.

## 10. Alembic autogenerate

Autogeneration creates a candidate only.

Manual review covers:

- rename vs drop/add ambiguity;
- type conversion/data loss;
- defaults/backfills;
- indexes/constraints;
- lock/table-rewrite consequence;
- old/new app compatibility;
- downgrade/forward-repair truth.

CI never auto-generates a migration and silently treats it as authority.

## 11. Migration safety tests

Where applicable validate the selected safe pattern itself, including:

- concurrent-index workflow consequences;
- staged constraints (`NOT VALID` → later validation) where used;
- expand/migrate/contract compatibility;
- bounded backfill idempotency/resume/checkpoint behavior;
- timeout/lock failure handling;
- data precondition/postcondition checks.

## 12. Concurrency / expected-state / idempotency

Real PostgreSQL tests deliberately provoke races.

Required families when corresponding implementation exists:

```text
two writers from same expected state
conflicting idempotency-key reuse
equivalent duplicate request
multi-owner atomic transaction failure
outbox + canonical transition atomicity
transaction conflict/retry boundary
```

Tests must demonstrate the accepted semantics, not merely absence of exceptions.

## 13. Provider adapters

Use layers where useful:

```text
unit fake/stub
fast deterministic behavior

provider contract/integration
real non-production provider/service or official local runtime

system
end-to-end through DANTE boundary
```

A mock success payload is not evidence a provider integration works.

Real provider tests use non-production resources/credentials and are isolated from untrusted PR execution.

## 14. HTTP/API tests

When FastAPI routes exist, test real routing/validation/error projection and public contract behavior.

Cover, as applicable:

- request/response validation;
- status/error model;
- headers/correlation/idempotency semantics;
- authority/privacy boundaries;
- OpenAPI determinism;
- compatibility requirements.

Calling the route function directly is not sufficient transport proof.

## 15. Privacy / non-interference testing

DANTE requires explicit tests for information leakage, not only ordinary authorization success/failure.

Test families include, as applicable:

- resource existence leakage;
- count leakage;
- ranking leakage;
- timing/error-shape leakage;
- free/busy inference;
- candidate/explanation leakage;
- aggregate/derived-context leakage;
- unauthorized historical/provenance disclosure.

WL-H12 remains the governing inherited rule.

## 16. Test data

Default:

```text
SYNTHETIC
DETERMINISTIC
SEMANTICALLY VALID
```

Rules:

- no production DB dump as ordinary fixture;
- no real credentials/tokens;
- no accidental personal data in snapshots/logs/artifacts;
- durable regression corpus is versioned when material;
- builders/factories create valid defaults and make exceptional/invalid states explicit.

## 17. Coverage

Coverage is tracked as a signal, not semantic proof.

Initial policy:

- every material behavior receives direct tests at the appropriate level;
- critical Domain/Logical invariants have explicit tests independent of percentage;
- generated/migration/framework boilerplate does not distort incentives;
- exact global/changed-code thresholds wait until the first real vertical slice creates a meaningful denominator;
- once introduced, thresholds change deliberately and do not silently fall to make CI green.

No arbitrary “80% because everyone uses 80%” rule is accepted at foundation time.

## 18. Test cost tiers

### PR — blocking/high signal

As corresponding code exists:

- repository/manifest/config validation;
- Ruff/mypy;
- architecture tests;
- unit/application tests;
- fast Hypothesis profile;
- real PostgreSQL integration;
- migration base→head/drift;
- critical concurrency/privacy tests.

### Accepted main / DEV

Add heavier integration/provider/system smoke where remote/non-production resources are required.

### Scheduled/nightly

Add larger Hypothesis/state/concurrency/fuzz/regression corpora where useful.

### UAT/release

Add release-specific E2E, migration rehearsal, performance, failure injection, security/recovery and applicable PSV.

## 19. Flaky-test policy

A flaky test is a defect, not a test to retry until green.

Investigate/fix it or explicitly quarantine it with reason/owner/exit condition. Retries may diagnose/transiently contain known external instability but cannot become semantic PASS evidence.

## 20. CI provider

Use **GitHub Actions** as primary repository CI/CD orchestration.

Reason:

- source/PR/branch protection already lives on GitHub;
- checks/deployment identity stays close to source history;
- GitHub Environments/OIDC/security/supply-chain features integrate with the repository;
- no current requirement justifies a second CI control plane.

## 21. Workflow architecture

Do not create one enormous workflow with unrelated concerns interleaved.

Backend-oriented classes once real checks exist may include:

```text
repository/config validation
backend quality: format/lint/type/architecture
backend tests: unit/application/property
backend database: PostgreSQL/integration/migration/concurrency
backend security/supply chain
future deploy DEV/UAT/PROD
```

Exact YAML filenames/job names are implementation details. Stable emitted check names matter before branch protection makes them required.

No empty/decorative workflow is created just to reserve a name.

## 22. PR CI security

PR validation:

- least-privilege explicit `GITHUB_TOKEN` permissions;
- no PROD secrets;
- no deployment identity;
- no automatic production deploy;
- deterministic frozen installs;
- caches keyed to actual lock/tool inputs;
- superseded non-deployment runs cancelled where safe;
- failure attributable to stable high-signal checks.

Avoid privileged execution of untrusted PR-controlled code such as unsafe `pull_request_target` patterns.

## 23. Required check activation

Existing DANTE repository rule remains:

```text
real workflow/job exists
+ runs on relevant PRs
+ stable emitted check name verified remotely
+ success/failure behavior observed
+ failure truly means merge must stop
→ only then may the exact check become required on protected main
```

Never configure guessed future check names.

## 24. One-developer review posture

While DANTE has one active developer, do not manufacture a fake independent-review gate that cannot be independently satisfied.

Protected main + PR + automated gates remain real.

When additional maintainers exist, required review/CODEOWNERS can activate at real ownership/security boundaries.

## 25. Actions hardening

Protected workflows:

- explicit minimal `permissions`;
- external Actions pinned to immutable full commit SHA;
- official Actions also SHA-pinned in protected workflows unless a documented technical constraint prevents it;
- allowed Action sources restricted where repository settings support useful enforcement;
- shell commands fail on errors and avoid secret echo;
- downloaded tools/binaries pinned/verified where practical;
- no dynamic execution of PR-controlled scripts with privileged credentials.

## 26. Dependency security

When real manifests exist:

- dependency graph/review visibility is enabled for supported ecosystems;
- Dependency Review evaluates new dependency risk;
- severity/license blocking policy is chosen against real dependencies rather than guessed in advance;
- dependency bot/update automation is configured only for package-manager versions actually supported;
- bot PRs run the same relevant validation as human dependency PRs.

No false claim of `uv.lock`/other automation support without verifying current GitHub capability.

## 27. CodeQL / SAST

CodeQL Python activates when real production Python source exists and can be configured truthfully.

It complements rather than replaces:

```text
Ruff
mypy
tests
architecture checks
dependency review
container/IaC scanning when those artifacts exist
```

“Scanner ran” is not equivalent to “application secure”.

## 28. Secret scanning

Use repository secret scanning/push protection where available for the repository/account/visibility at activation time.

This is a second barrier. Committing secrets remains forbidden regardless of scanner capability.

## 29. Deployment identity

When cloud deployment exists, use GitHub OIDC for short-lived provider identity where supported.

Static long-lived deployment keys are fallback only.

Deployment jobs reference the intended GitHub Environment (`dev`, `uat`, `prod`).

## 30. Build artifacts

When OCI backend images activate:

- reproducible multi-stage build where useful;
- minimal runtime image;
- non-root runtime where practical;
- no build secrets in final layers;
- tag for navigation, digest for promotion identity;
- release SHA/build metadata attached;
- vulnerability scan before production promotion when applicable.

CI artifacts use explicit retention and do not become shadow stores of user/test data.

## 31. Provenance and SBOM

At production release boundary:

- produce artifact provenance/attestation linking source/workflow/artifact digest;
- produce SBOM/dependency inventory appropriate to the release artifact;
- retain evidence according to release/security policy.

Provenance proves where an artifact came from, not that its behavior is correct.

## 32. Runner posture

Use GitHub-hosted Linux runners initially.

Self-hosted runner requires a measured reason such as:

- private network access;
- special hardware;
- measured cost/performance requirement;
- special reproducible environment.

It also requires explicit patching/isolation/cleanup/credential hardening ownership.

## 33. Merge queue

Deferred until real merge concurrency makes it valuable. One developer/low concurrency does not justify it now.

## 34. Deployment concurrency

PR CI may cancel superseded safe runs.

Deployment/migration concurrency is serialized per environment where concurrent mutation is unsafe. A production migration is not blindly cancelled because a newer deployment request exists.

## 35. Change-aware CI

Path filtering may reduce monorepo cost only after correctness is proven.

A backend job still runs when any input capable of affecting it changes, including backend source, backend lock/tool config, database image/migration tooling, shared contract input, workflow/build infrastructure and relevant repository-global configuration.

Never optimize by silently skipping correctness after root/shared changes.

## 36. Frontend testing/CI

Not selected by this document.

Web/mobile test runners, native E2E, package-manager task graph, EAS/build/release details and frontend-specific CI are deferred to the frontend workstream.

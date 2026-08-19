# Testing and CI v0

- Status: **Engineering Foundation branch baseline — pending closure**
- Scope: automated validation, CI/CD orchestration, supply-chain and release evidence

## 1. Principle

DANTE testing is organized by **risk and boundary**, not by one giant suite or a vanity coverage number.

A PASS claim must identify what was directly executed.

```text
unit PASS
!= PostgreSQL integration PASS
!= migration PASS
!= provider contract PASS
!= UAT E2E PASS
!= recovery PASS
!= complete PSV PASS
```

The existing Physical post-selection validation register remains authoritative for specialist obligations and stays `NOT RUN` until direct artifacts exist.

## 2. Test taxonomy

Future production code uses these distinct classes as applicable:

```text
UNIT
pure domain/application calculations and local behavior

PROPERTY / INVARIANT
state-space, generative and invariant validation

ARCHITECTURE
static dependency/import/layer rules

INTEGRATION
real PostgreSQL and activated technical dependencies

MIGRATION
schema evolution, empty->head, release transition and safety checks

CONTRACT
OpenAPI/client/provider adapter compatibility

COMPONENT
web/mobile component behavior

SYSTEM / E2E
black-box user/system journeys across deployed/runnable boundaries

SECURITY / SUPPLY CHAIN
SAST, dependency, secret, container/IaC checks

PERFORMANCE / RESILIENCE / RECOVERY
only at the capability/release boundary that needs them
```

## 3. Backend unit tests

Unit tests should run without network, PostgreSQL, provider SDK calls or containers whenever the behavior under test is pure.

Priority targets:

- domain invariants;
- state transitions;
- application decision logic;
- expected-state/conflict handling;
- idempotency/equivalence behavior;
- candidate/actual distinctions;
- parsing/normalization where semantic;
- permission/governance policy logic once implemented;
- deterministic solver-result interpretation once implemented.

Mocking is used at explicit ports, not deep inside implementation internals merely to force a unit shape.

## 4. Property/invariant tests

Use Hypothesis or equivalent generative testing where hand-picked examples are poor coverage of the state space.

High-value candidates include:

- identifier/reference round-trips;
- temporal/recurrence transitions;
- ordering/range boundaries;
- correction/version semantics;
- expected-state conflict cases;
- idempotency key reuse conflicts;
- normalization/search token cases;
- solver status handling;
- redaction/visibility invariants.

Property tests must encode meaningful properties, not random input for its own sake.

## 5. Architecture tests

Once packages/modules exist, automated checks enforce foundation boundaries.

At minimum:

```text
domain packages do not import FastAPI

domain packages do not import SQLAlchemy

domain packages do not import provider SDKs

packages/* do not import apps/*

production source does not import prototypes/*

module A does not import module B private adapters/internals

client browser-safe code does not import server-only config/secrets
```

The lightest reliable enforcement mechanism is preferred. The rule matters more than buying a heavy architecture-testing framework.

## 6. PostgreSQL integration tests

Persistence integration uses real PostgreSQL with the versions/capabilities required by the implemented slice.

Not allowed as a substitute:

```text
SQLite backend test
claimed as proof of PostgreSQL behavior
```

CI should create an isolated disposable database/container per job or equivalent isolated test resource.

Integration tests cover, as applicable:

- constraints and FK behavior;
- transaction/rollback behavior;
- concurrency/expected-state behavior;
- SQLAlchemy mapping behavior;
- PostGIS/pgvector/search semantics once active;
- connection/pooling behavior where relevant;
- database-generated values/types;
- serialization/timezone/collation behavior material to semantics.

## 7. Database test isolation

Tests must be independently repeatable.

Acceptable strategies include transaction rollback, database/schema recreation or purpose-built isolated databases depending on the test class.

A test must not depend on execution order or dirty state from a previous test.

CI integration data is synthetic and deterministic enough to reproduce failures.

## 8. Migration tests

When migrations exist, CI validates:

1. migration graph has the expected single accepted head unless a deliberate branch/merge revision is in progress;
2. a clean PostgreSQL instance can migrate from base to head;
3. SQLAlchemy metadata/schema intent has no unrepresented migration drift;
4. required extensions/preconditions are present/validated;
5. migration code is reviewed/linted/importable;
6. destructive/long-running operations carry explicit release consideration.

At release boundaries, extend validation to:

```text
previous released schema/data
→ new migration chain
→ application smoke/integration
```

UAT rehearses materially risky migrations with representative synthetic volume/state.

## 9. Alembic autogenerate policy

Alembic autogeneration generates candidate migrations only.

CI must never auto-generate a migration and silently commit/apply it as authoritative.

A developer-generated candidate is reviewed for:

- rename vs drop/add ambiguity;
- type conversion/data loss;
- defaults/backfills;
- constraints/indexes;
- lock duration;
- concurrent rollout compatibility;
- downgrade/rollback truthfulness.

## 10. Provider/adapter contract tests

External providers are tested behind adapters.

Use three layers where useful:

```text
unit fake/stub
fast deterministic local behavior

provider contract/integration test
real non-production provider/service or official local runtime when needed

system test
end-to-end use through DANTE boundary
```

A mock success response is never evidence that a provider integration works.

Real-provider tests use non-production credentials/resources and are isolated from normal untrusted PR execution.

## 11. API contract tests

When HTTP API exists, validate:

- OpenAPI generation is deterministic;
- committed/generated TypeScript client matches current backend contract;
- generated client compiles/types;
- contract examples/schemas validate;
- intentional breaking change is detected/reviewed;
- deprecated compatibility remains until supported mobile clients can retire it.

A backend route test is not enough to prove client compatibility.

## 12. Web tests

Target stack when web production scaffold exists:

```text
unit/component/integration
Vitest + Testing Library

browser E2E
Playwright
```

Focus on observable behavior and accessibility-relevant semantics rather than fragile implementation snapshots.

Snapshot testing is used only where a stable serialized representation genuinely adds value; broad UI snapshots are not the main regression strategy.

Web E2E covers a small set of critical journeys rather than duplicating every component test in a browser.

## 13. Mobile tests

Target stack when mobile production scaffold exists:

```text
unit/component/integration
Jest + React Native Testing Library

native E2E
Maestro
```

Production-grade E2E runs against built development/test application artifacts, not Expo Go assumptions.

Maestro flows remain repository-owned and should be runnable outside a single hosted workflow provider where practical.

Current EAS-hosted Maestro workflow maturity is not treated as a reason to make an alpha hosted execution path a required repository gate before it proves stable.

## 14. System tests

`tests/system/` contains true black-box tests that span application boundaries or validate a deployed environment.

Examples later:

- API + web critical journey;
- API + mobile sync journey;
- provider callback/reconciliation journey;
- deployment smoke;
- cross-component privacy/non-interference cases.

System tests consume public/gateway contracts. They do not reach into application private modules merely to set up assertions unless a bounded test-support API/fixture is explicitly designed.

## 15. Test data

Test data policy:

- synthetic by default;
- deterministic builders/factories for important semantic cases;
- explicit edge-case fixture corpus where domain history requires it;
- no production database dumps;
- no real credentials/tokens;
- no accidental personal data in snapshots/logs/artifacts;
- fixture versioning when a regression corpus becomes durable evidence.

Factories should create semantically valid defaults and make exceptional/invalid state explicit.

## 16. Coverage policy

Coverage is tracked, but DANTE does not equate line coverage with correctness.

Initial foundation policy:

- every material new behavior has direct tests at the appropriate level;
- critical Domain/Logical invariants require explicit tests independent of aggregate percentage;
- generated code, migration boilerplate and framework bootstrap are not allowed to distort quality incentives;
- exact global/changed-code numerical thresholds are set after the first real vertical slice produces a meaningful denominator;
- a later threshold may only ratchet intentionally, not silently fall to make CI green.

This avoids choosing an arbitrary `80%` today and then optimizing code toward the number instead of risk.

## 17. CI provider

### Decision

Use **GitHub Actions** as the primary repository CI/CD orchestration layer.

Rationale:

- repository and branch protection already live on GitHub;
- PR/check/deployment identity remains close to source history;
- GitHub Environments support deployment boundaries;
- OIDC supports short-lived cloud identity with compatible providers;
- dependency review/CodeQL/attestation integrate with repository security.

Mobile-native build execution may invoke/use EAS where appropriate without creating a second independent source-integration authority.

## 18. CI workflow architecture

Do not create one enormous workflow file with every concern interleaved.

Expected workflow classes once code exists:

```text
ci-repo.yml
repository/config/docs policy validation

ci-api.yml
backend format/lint/type/unit/integration/migration

ci-web.yml
web lint/type/test/build

ci-mobile.yml
mobile lint/type/test/build validation

ci-contract.yml
OpenAPI/generated-client drift/compatibility

ci-security.yml
security/supply-chain checks where useful

deploy-dev.yml
deploy-uat.yml
deploy-prod.yml
only when corresponding deployment exists
```

Exact filenames/jobs are implementation details; stable emitted job/check names matter before branch rules make them required.

Reusable workflows/actions may be extracted only after repetition exists.

## 19. PR CI principles

PR validation must be safe for untrusted change context.

Rules:

- least-privilege `GITHUB_TOKEN` permissions;
- no PROD secrets;
- no automatic production deployment;
- read-only cloud/provider access where possible for validation;
- dependency caches keyed to lockfiles/toolchain;
- deterministic locked installs;
- cancellation of superseded PR runs where safe;
- failures remain inspectable and attributable to one stable job/check.

Avoid `pull_request_target` for running untrusted PR code with elevated secrets.

## 20. Change-aware CI

Path/change filtering is allowed to save time but must be conservative.

A job must run when any input capable of affecting it changes, including:

- its app source;
- shared package source;
- root lock/workspace config;
- generated contracts;
- relevant infrastructure/build scripts;
- workflow/toolchain configuration.

Do not build a clever filter that silently skips tests after a root/shared dependency change.

Turborepo may compute affected JS tasks; Python and repository-global inputs remain explicitly represented.

## 21. CI ordering

Fast/high-signal checks run early.

Conceptual PR order:

```text
repository/manifest validation
→ formatting/lint/types
→ unit tests
→ build / contract generation
→ integration/migration tests
→ heavier E2E/security/specialist checks as applicable
```

Independent jobs run in parallel where safe.

No artificial serial pipeline is created merely for visual order.

## 22. Required status-check activation

Current repository policy has no required status checks because no stable real workflows exist.

Engineering Foundation preserves the existing promotion protocol:

```text
real workflow/job exists
+ runs on relevant PRs
+ stable emitted check name verified
+ success observed
+ failure genuinely means merge should stop
→ then exact check MAY become required on main
```

Never configure a future guessed check name into branch protection.

Required checks are added only after remote verification.

## 23. CI concurrency

### PR

Use concurrency groups so new pushes can cancel superseded non-deployment CI for the same PR/branch.

### Deployment

Serialize per environment where migrations/resource changes make concurrent deployment unsafe.

A new deployment request does not blindly cancel an in-progress production migration or other non-interruptible release step.

## 24. GitHub Actions hardening

Workflow baseline:

- explicit minimal `permissions` block;
- third-party Actions pinned to immutable commit SHA where practical;
- official/actions still version-reviewed and preferably SHA-pinned in protected workflows;
- shell commands fail on errors and avoid accidental secret echoing;
- downloaded tools/artifacts are pinned/verified where practical;
- action dependency updates reviewed through dependency tooling;
- no dynamic execution of PR-controlled scripts with elevated deployment credentials.

## 25. Dependency review

When dependency manifests exist, PR CI uses GitHub dependency review/supply-chain visibility for supported ecosystems.

A dependency change should surface:

- newly introduced known vulnerability;
- dependency/source change;
- material license risk where policy becomes applicable.

Severity/license enforcement thresholds are configured only when there is an accepted policy; they are not invented as arbitrary governance in this foundation.

## 26. Dependabot / dependency update automation

Once real manifests exist, configure supported ecosystems for security/version updates, including as supported at that time:

- uv/Python;
- pnpm/npm workspace;
- GitHub Actions;
- Docker;
- future IaC ecosystem.

Exact package-manager version support is verified when configuration is added. If pnpm 11 is not yet supported by a GitHub automation feature, that limitation is recorded and handled through scheduled maintenance/another selected mechanism instead of producing a false PASS.

Bot PRs run the same relevant CI as human dependency PRs.

## 27. CodeQL / SAST

CodeQL activates when real production source exists and language/build topology can be configured truthfully.

It is not created as an empty workflow during Engineering Foundation.

A CodeQL finding policy is severity/risk based. Tool output is reviewed; “scanner ran” is not equivalent to “application secure”.

Language-native static checks complement CodeQL:

- Ruff/mypy/backend tests;
- ESLint/TypeScript/client tests;
- provider/IaC/container scanners when those artifacts exist.

## 28. Secrets and PR security

CI must be designed so normal PR validation does not require production secrets.

Dependabot/untrusted PR restrictions are treated as a design input, not bypassed.

Real provider integration tests requiring secrets may run:

- after trusted merge in DEV;
- on manually approved trusted branch/job;
- or in another bounded safe workflow.

They must not leak secrets into logs/artifacts.

## 29. OIDC and deployment identity

For cloud providers that support it, deployment workflows use GitHub OIDC to obtain short-lived credentials bound to repository/workflow/environment claims.

Static long-lived deployment keys are fallback only.

Deployment jobs reference the GitHub Environment (`dev`, `uat`, `prod`) so environment protections/credentials apply before privileged work begins.

## 30. Build artifacts

Server/web builds are reproducible from locked source and produce identifiable artifacts.

When OCI images activate:

- multi-stage build where useful;
- minimal runtime image;
- non-root runtime where practical;
- no build secrets copied into final layers;
- image tagged for navigation and promoted by immutable digest;
- release SHA/build metadata embedded/attached;
- vulnerability scan added before production promotion when image exists.

CI artifacts have explicit retention; they do not become indefinite shadow stores of test/user data.

## 31. Artifact provenance

Once releasable artifacts exist, use build provenance/attestation appropriate to the GitHub/repository capabilities.

The target is to answer:

```text
which source commit built this?
which workflow built it?
which locked dependencies/toolchain were used?
which artifact digest was promoted?
```

Attestation is evidence of provenance, not evidence that code is semantically correct.

## 32. DEV deployment

When remote DEV exists:

- successful accepted-main build creates/promotes artifact;
- deployment references GitHub `dev` environment;
- migration job executes in controlled order if needed;
- post-deploy smoke verifies basic health/version/migration identity;
- deploy result records artifact/SHA.

Auto-deploy from `main` is preferred after it proves stable.

## 33. UAT promotion

UAT uses an exact previously built candidate.

Gate may include, as applicable:

- DEV success;
- migration rehearsal;
- API/system E2E;
- web/mobile candidate compatibility;
- provider smoke;
- applicable specialist PSV/release checks;
- operator/user acceptance.

UAT evidence belongs to the exact candidate, not a moving branch label.

## 34. PROD promotion

PROD requires explicit release promotion once real users exist.

Baseline:

- GitHub `prod` environment;
- protected deployment job;
- exact candidate artifact/digest;
- exact migration revision;
- release notes/version identity when active;
- preflight/rollback-forward-repair plan for risky change;
- post-deploy smoke/observability check.

A production deploy is not triggered from an unreviewed feature branch.

## 35. Mobile CI/CD

GitHub Actions remains source/quality orchestration authority.

EAS Build/Submit may perform native build/sign/distribution because it is specialized for Expo; exact use is selected during mobile scaffold.

Rules:

- EAS profile config is versioned;
- build identity ties back to source SHA;
- signing secrets remain provider/CI secrets;
- development, UAT/internal and production build profiles are separated;
- native E2E uses built artifacts;
- app-store submission is a release action, not normal PR CI.

EAS Workflows may supplement this model, but DANTE does not need two independent duplicated CI policy graphs. GitHub remains the canonical repository integration/deployment orchestration record unless a later explicit decision changes it.

## 36. Performance tests

Performance tests are not run on every PR unless they become cheap/stable/high-signal.

Use tiers:

- micro/unit performance only for proven hot logic;
- DB/query benchmarks for regressions when real schema/data shapes exist;
- load/capacity tests at release/capacity boundaries;
- SC-032/backpressure and Physical benchmark obligations at their direct execution boundary.

Performance numbers require stable dataset/environment evidence; an uncalibrated laptop run is not a production capacity claim.

## 37. Recovery/resilience tests

Recovery tests activate at their accepted boundary.

Examples from PSV:

- anti-resurrection restore;
- migration/restore rehearsal;
- PowerSync stalled replication/reconciliation;
- Restate crash/replay/outage after activation;
- R2/S3 object recovery;
- observability outage non-interference.

They are distinct suites/evidence and remain `NOT RUN` until actually executed.

## 38. Flaky test policy

A flaky required test is a defect in the delivery system.

Rules:

- retry may collect diagnostic evidence but must not normalize permanent flakiness;
- repeatedly flaky tests are owned/fixed or explicitly quarantined with tracked reason;
- quarantine cannot hide a critical correctness/security gate indefinitely;
- nondeterministic provider tests are isolated from deterministic unit/integration evidence.

## 39. Test failure diagnostics

CI failures should retain bounded safe artifacts useful for diagnosis:

- test reports;
- sanitized logs;
- screenshots/traces for browser/mobile E2E;
- migration logs without credentials/data payloads;
- version/environment metadata.

Never upload broad DB dumps or secret-rich environment snapshots for convenience.

## 40. Local vs CI parity

Every required CI check should have a documented local equivalent where technically practical.

CI may provide ephemeral services/runners, but validation logic should not exist only as opaque YAML shell fragments.

If a workflow contains non-trivial reusable logic, move that logic into a repository-owned script/tool that can run locally and in CI, while the workflow remains the orchestration layer.

## 41. Definition of CI-ready scaffold

The initial production scaffold is CI-ready when:

```text
locked installs work from clean checkout
format/lint/type commands run
unit tests run
production builds compile
real PostgreSQL integration harness works when persistence exists
migration checks work when migrations exist
generated contract drift check works when API contract exists
workflows emit stable observed check names
no PR job needs production secrets
```

Only then should corresponding checks be promoted into protected-main requirements.

## 42. Primary-source basis

Current foundation direction was checked on 2026-08-19 against official documentation including:

- GitHub deployment environments and deployment controls: `https://docs.github.com/en/actions`
- GitHub OIDC reference: `https://docs.github.com/en/actions/reference/security/oidc`
- GitHub dependency/supply-chain security: `https://docs.github.com/en/code-security/concepts/supply-chain-security/`
- FastAPI multi-file applications: `https://fastapi.tiangolo.com/tutorial/bigger-applications/`
- SQLAlchemy async behavior: `https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html`
- Alembic autogeneration: `https://alembic.sqlalchemy.org/en/latest/autogenerate.html`
- Expo development builds/monorepo/E2E guidance: `https://docs.expo.dev/`

External documentation supports tooling facts. Actual DANTE PASS evidence remains repository execution evidence only.

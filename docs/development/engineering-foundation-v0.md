# Engineering Foundation v0

- Status: **CLOSED / ACCEPTED**
- Scope: backend/repository engineering baseline before first production implementation
- Product: **DANTE**
- Frontend internal engineering: **DEFERRED to dedicated frontend workstream**

## 1. Purpose

Engineering Foundation v0 defines the engineering contract under which DANTE production code is created and evolved.

It is downstream from the closed Domain, Logical and Physical models and upstream from production implementation.

```text
Domain / Logical / Physical
          ↓
Engineering Foundation v0
          ↓
production scaffold
          ↓
concrete implementation
```

It does not create production code, schema, API/Auth or direct validation evidence.

## 2. Quality model

The standard is production-grade without copying complexity that exists only because very large organizations already have large distributed teams.

The foundation optimizes for:

1. semantic fidelity to accepted Domain/Logical truth;
2. one canonical persistence authority;
3. explicit dependency and ownership boundaries;
4. reproducible local/CI environments;
5. safe schema and data evolution;
6. environment isolation;
7. immutable/traceable releases;
8. least-privilege delivery and secret handling;
9. high-signal automated validation;
10. growth without forced microservices or repository fragmentation.

## 3. Inherited non-negotiable boundaries

Implementation preserves, among others:

```text
Person != Account != Principal != Actor
Authority != AuthZ decision
Consent != Authority
Visibility != Authority
provider state != canonical DANTE state
derived projection != canonical truth
absence / unknown != false
MaterialStateRef != ETag/MVCC/provider revision
idempotency != semantic identity
AI / solver output != accepted canonical effect
```

`WL-H01..WL-H12` remain active.

PostgreSQL remains the sole canonical persistence authority. PowerSync/SQLite, R2/S3, Restate, solver and telemetry are bounded mechanisms under the already-accepted Physical model.

## 4. Repository strategy

### Decision

DANTE uses one **product monorepo**.

```text
apps/        runnable/deployable applications
packages/    genuinely shared cross-application artifacts/contracts
infra/       local/remote infrastructure definitions
tooling/     repository engineering utilities
tests/       true cross-application/system black-box tests
docs/        durable product/architecture/engineering authority
prototypes/  explicitly non-production work
.github/     GitHub automation/integration controls
```

Deployable application boundaries:

```text
apps/backend
apps/web
apps/mobile
```

`apps/backend` is the server-side application boundary. FastAPI is an inbound adapter/process host, not the identity of the whole backend.

Repository extraction is allowed later only for a measured independent lifecycle/security/ownership/scale boundary.

The current GitHub repository is retained. Creating a new repository for production implementation is not part of the accepted plan. A rename from the historical repository name `lifeos` to `dante` is a separate governance operation.

## 5. Backend application architecture

DANTE begins as a **capability-first modular monolith**.

Core rules:

- one deployable backend while product/team size does not justify distributed services;
- capability modules reflect behavior/change cohesion, not one table/route/Logical owner each;
- Domain/application meaning remains separate from FastAPI, SQLAlchemy and provider SDKs;
- concrete dependency wiring belongs to the composition root;
- module private persistence/adapters are not cross-module APIs;
- cross-module atomic transactions remain allowed where accepted semantics require them;
- no universal `Repository[T]`, `BaseService`, service locator, global mutable DB session or `shared/common/utils` dumping ground.

Detailed rules: `application-structure-v0.md`.

## 6. Frontend boundary

This workstream fixes only that:

```text
apps/web
apps/mobile
```

are sibling applications in the same product monorepo and remain governed clients of the backend contract.

It **does not** select or freeze their package manager, task graph, detailed source tree, test runner, E2E stack, mobile build service usage or shared-UI strategy. Those decisions belong to the dedicated frontend workstream/branch after current frontend design work is ready.

Existing accepted product choices such as Next.js/React and Expo/React Native are inherited context, not re-selected here.

## 7. Environment model

DANTE lifecycle contexts:

```text
LOCAL
individual developer context

DEV
shared remote integration environment

UAT
production-like release-candidate/acceptance environment

PROD
real released environment and real user data
```

Rules:

- environments are not Git branches;
- protected `main` is the integrated source truth;
- remote environment state, identity, credentials and secrets are isolated;
- provider-native account/project/subscription isolation is preferred where practical and security-relevant;
- lower environments do not possess production credentials;
- production data is not copied raw into DEV;
- remote provider is intentionally deferred.

Activation:

```text
LOCAL   first implementation
DEV     when remote integration becomes useful
UAT     when real release candidates exist
PROD    at production-readiness
```

## 8. Release identity and promotion

Future server artifacts are immutable and traceable to at least:

```text
source commit SHA
build identifier
OCI/artifact digest
release/version when active
migration head when applicable
```

Target server lifecycle:

```text
accepted main
→ build/test
→ immutable artifact
→ DEV
→ exact release candidate
→ UAT
→ exact candidate
→ PROD
```

Build-once/promote-exact-artifact is the default where the platform permits it.

## 9. Backend runtime/toolchain

```text
Python supported line        3.14.x
initial bootstrap pin        3.14.7
package/environment manager  uv
manifest                     apps/backend/pyproject.toml
lockfile                     apps/backend/uv.lock (committed)
interpreter declaration      apps/backend/.python-version
source layout                apps/backend/src/dante
formatter/linter             Ruff
type checker                 mypy strict baseline
test runner                  pytest
property/state-space tests   Hypothesis where meaningful
```

Exact dependency versions are resolved/locked during scaffold. Unbounded `latest` is not a production/CI contract.

## 10. Developer platform

Canonical server-side semantics are Linux.

For Windows development:

```text
Windows 11 host
        ↓
WSL2 / Linux
        ↓
repo checkout in WSL filesystem
Python / uv / Git / backend process
        ↓
Docker Desktop WSL2 backend for stateful infra
```

PyCharm is a supported primary IDE workflow using a WSL interpreter and can provide normal run/debug/test integration. Repository commands/configuration remain IDE-neutral so another supported IDE does not change the engineering contract.

Backend runs directly in WSL/Linux during the normal inner loop. Docker Compose runs stateful LOCAL dependencies. Future remote backend packaging uses OCI containers.

## 11. LOCAL PostgreSQL platform

Canonical LOCAL persistence is real PostgreSQL 18.4.

DANTE owns a reproducible local database build/configuration. It must make exact PostgreSQL/extension provenance inspectable and must not rely on a mutable community “all extensions” image.

The first LOCAL database has the full selected extension envelope installed and enabled:

```text
PostGIS             3.6.4
pgvector            0.8.6
pg_trgm             enabled
unaccent            enabled
pg_stat_statements  enabled + shared_preload_libraries configured
native FTS          available
```

“Enabled” means database/server capability is present from the first baseline. Application features remain free not to use a capability until their implementation arrives.

PgBouncer 1.25.2 remains a selected target and is activated/tested at the connection-pooling boundary rather than forced into every first-line LOCAL request.

## 12. Persistence architecture

```text
SQL toolkit / ORM         SQLAlchemy 2.0 stable line
PostgreSQL driver         psycopg 3
I/O model                 async at DB/provider/HTTP boundaries where useful
Domain/application logic  synchronous/pure by default
migration authority       Alembic
```

Rules:

- SQLAlchemy mappings are persistence models, not canonical Domain identity;
- complex SQL/Core is allowed when clearer/safer than forced ORM navigation;
- one `AsyncSession` is bounded to one concurrent use-case/task scope;
- sessions are injected and never global;
- application/use-case boundary owns transaction commit/rollback;
- adapters do not silently commit inside a larger semantic transaction;
- no universal generic CRUD repository;
- persistence ports are capability/use-case shaped where a boundary adds real value.

## 13. Schema/migration governance

Deployed schema is represented by Alembic revision history.

Hard rules:

1. no production schema management through application `metadata.create_all()`;
2. every durable schema change has a reviewed migration;
3. autogenerate is assistance/candidate generation only;
4. merged/applied revisions are immutable;
5. manual remote DDL that is not reconciled into migration history is forbidden;
6. empty PostgreSQL → head is continuously tested;
7. metadata/schema drift is detected in CI;
8. release migration execution is serialized and separate from ordinary application startup;
9. risky evolution uses expand → migrate → contract;
10. old mobile/client compatibility is part of contract/removal timing.

Migration review classifies:

- data-loss risk;
- table rewrite risk;
- lock duration/strength;
- index construction behavior;
- constraint validation behavior;
- old/new application coexistence;
- backfill cost/resumability;
- rollback versus forward-repair truth.

Use PostgreSQL online/staged mechanisms such as concurrent index creation and `NOT VALID`/later validation where technically appropriate.

Large data migrations/backfills use bounded, restartable, idempotent jobs with checkpoints and validation instead of one giant migration transaction.

## 14. Database privilege model

When implemented, PostgreSQL privilege classes are separated by responsibility:

```text
owner          owns schema objects; not ordinary application runtime
migrator       controlled DDL/release migration capability
runtime        normal backend application capability only
replication    PowerSync/replication capability when active
backup         recovery capability when active
```

Exact grants are implementation work, but normal API runtime must not possess schema-owner power merely for convenience.

## 15. Copy, backup and recovery model

Logical-copy tooling:

```text
pg_dump / pg_restore
```

is used for portable logical copies, controlled migration tests and bounded/sanitized clone workflows.

Recovery-grade production posture remains the already-selected:

```text
pgBackRest 2.59.0
+ WAL archive / PITR
+ AWS S3 Standard eu-south-1
+ accepted retention/Object Lock posture
```

That recovery stack remains dormant until the fixed recovery/production boundary or real rehearsal need.

Rules:

- backup is not the normal “rollback button” for every schema migration;
- risky changes require a truthful forward/rollback/recovery plan;
- once recovery activates, backup verification and periodic restore rehearsal are required;
- raw production data is not copied into DEV by default;
- production-derived acceptance/debug clones require explicit minimization/sanitization and authorization;
- PostgreSQL major upgrades use a separate platform procedure (`pg_upgrade`, dump/restore, logical replication or another reviewed supported path), not normal application migration semantics.

## 16. Configuration and secrets

Backend configuration is typed with `pydantic-settings`, validated before serving work and immutable after bootstrap.

Configuration classes are separated:

```text
non-secret deployment configuration
secret material
build/release identity
governed domain/business configuration
```

Domain/business semantics must not migrate into environment variables as a second truth authority.

LOCAL may use ignored `.env.local`; a safe `.env.example` is committed.

Remote hierarchy:

```text
minimize secrets
→ workload/federated identity
→ provider secret manager
→ least privilege
→ rotation / revocation / audit
```

GitHub OIDC is preferred for CI-to-cloud identity where supported. Long-lived deployment credentials are fallback only.

Full contract: `config-and-secrets-v0.md`.

## 17. Testing architecture

Testing is organized by risk/boundary, not a single suite or vanity coverage number.

Required as applicable:

```text
unit/domain
application/use-case
property/invariant
state-machine/lifecycle
architecture dependency
real PostgreSQL integration
migration
concurrency/expected-state/idempotency
provider contract
HTTP/API contract
privacy/non-interference
system/E2E
security/supply chain
performance/resilience/recovery/PSV
```

Real PostgreSQL tests use the DANTE-owned PostgreSQL 18.4 image/envelope. SQLite is never evidence of PostgreSQL backend correctness.

Test data is synthetic/deterministic by default.

Coverage is tracked, but a numeric gate is introduced only after real code provides a meaningful denominator. Critical semantic paths must have direct tests independent of aggregate percentage.

Test cost tiers:

```text
PR
fast/high-signal mandatory validation

accepted main / DEV
heavier integration/provider/system smoke

scheduled/nightly
larger property/state/concurrency/fuzz corpus where useful

UAT/release
migration rehearsal, E2E, performance, failure injection, recovery/security and applicable PSV
```

Flaky tests are defects to investigate/fix or explicitly quarantine; repeated retries are not accepted as evidence of correctness.

## 18. CI/CD

GitHub Actions is the primary repository CI/CD orchestration layer.

Principles:

- split workflows/jobs by meaningful responsibility;
- run fast/high-signal checks early and parallelize independent work;
- use deterministic locked installs;
- use conservative change/path filtering only after correctness is proven;
- cancel superseded non-deployment PR runs where safe;
- serialize environment deployments/migrations where concurrent execution is unsafe;
- normal PR validation has no production secrets/deployment identity;
- `GITHUB_TOKEN` permissions are explicit/minimal;
- protected workflows pin external Actions to immutable full commit SHAs;
- only approved/trusted Action sources are allowed when repository policy supports enforcement;
- a check becomes required on `main` only after its real stable emitted context and blocking value are verified;
- one-developer reality does not create fake required human review; independent review rules can activate when real independent maintainers exist.

GitHub-hosted runners are the default. Self-hosted runners require a measured hardware/private-network/cost/environment need and a separate security/maintenance decision.

## 19. Security and supply chain

When corresponding artifacts/source exist:

- Dependency Review evaluates dependency changes;
- a severity/license enforcement policy is selected against real dependencies rather than invented before manifests exist;
- CodeQL Python activates for real production Python source;
- secret scanning/push protection is used where repository capability supports it;
- OCI/container scanning activates with real images;
- release artifacts are promoted by immutable digest;
- production release artifacts receive build provenance/attestation;
- production release boundary includes an SBOM/dependency inventory;
- evidence/artifact retention is class/policy-bound rather than infinite.

Artifact attestation proves provenance, not semantic correctness.

## 20. Infrastructure-as-code posture

Remote durable infrastructure must eventually be reproducible from version-controlled desired state.

`infra/iac/` is reserved for that contract, but neither cloud/compute provider nor IaC engine is selected here.

The first remote infrastructure scope must select/pin them against actual DANTE deployment requirements. Manual console state must not become the only production representation.

## 21. Deferred decisions

Intentionally deferred:

```text
frontend internal architecture/toolchain/testing/release implementation
cloud/compute provider
IaC engine
artifact registry
remote environment sizing
backend capability module map
concrete database schema/migrations
API route/version surface
AuthN/AuthZ mechanism
exact numeric coverage thresholds
specialist service implementation beyond accepted activation triggers
```

A defer requires a later explicit bounded decision; it is not permission to improvise.

## 22. Closure and next boundary

Engineering Foundation v0 is **CLOSED**.

Next sequence:

```text
repository identity decision
(keep current repo; decide/execute recommended `lifeos → dante` rename or explicitly defer)
        ↓
production repository/backend scaffold
        ↓
LOCAL PostgreSQL + migration harness
        ↓
concrete Logical → PostgreSQL implementation
        ↓
first persistence/application vertical slice
```

Before any implementation write, re-run mandatory bootstrap and exact Git write gate.

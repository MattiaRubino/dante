# Workstream — Production Backend Scaffold

- Status: **ACTIVE / CP1 CLOSED / CP2 CLOSED / CP3 CLOSED / DIRECT QA PASS / CP4 M1–M4 COMPLETE / M5 NEXT**
- Branch: `feature/backend-scaffold`
- Decision baseline PRE-SCOPE: `9f7c21857cf7a9c7300053370954c4b93f9bd96a`
- CP1 closure implementation HEAD: `02d113d772cdb247faebb3cef4d857d125266da3`
- CP2 implementation/repair HEAD before closure docs: `2d79c89d78b9031a1fe4323bbdcdb4b359fa87d6`
- CP3 original materialization PRE-SCOPE: `a09936d168de48909d948425387b168d016911e8`
- CP3 lock materialization HEAD: `17c00d2ac24d2efecfc52f7fa5f707f5b15c36cd`
- CP3 implementation/direct-QA HEAD: `35cf6440bc121a38342f6bbee72e210435a788a4`
- CP4 design PRE-SCOPE: `495e484c6ac729f24dc43dc2dbba8cc4d359a568`
- CP4 M4 PRE-SCOPE / tested post-merge HEAD: `ba0d994e983cf3e5add6ad640c238999f418e236`
- CP4 M4 main consumed: `ff46eb16b971b1fde96eef9047b09faa02e1a5db`
- CP4 M4 two-parent merge: `6a8122249f13f9b8553f511c47b4185c6e3e6540`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Engineering Foundation v0: **CLOSED / CONSUMED / NOT REOPENED**
- Concrete Logical → PostgreSQL schema: **OUT OF SCOPE UNTIL SCAFFOLD QA**
- Detailed CP1 contract: `docs/development/backend-cp1-contract.md`
- Detailed CP2 contract: `docs/development/backend-cp2-postgres-contract.md`
- Detailed CP3 contract: `docs/development/backend-cp3-persistence-contract.md`
- Detailed CP4 contract: `docs/development/backend-cp4-ci-contract.md`

## 1. Purpose

This workstream turns the closed Engineering Foundation into the first real production backend scaffold.

It exists so implementation can proceed in small, directly verifiable checkpoints rather than creating the entire backend/database/CI surface in one opaque write.

The scaffold is infrastructure and application bootstrap only. It does not authorize concrete Domain/Logical persistence mapping or business vertical slices.

```text
ENGINEERING FOUNDATION v0
        CLOSED
          ↓
PRODUCTION BACKEND SCAFFOLD
        ACTIVE
          ↓
CP1 Python/backend process + typed config
        CLOSED / DIRECT QA PASS
          ↓
CP2 reproducible LOCAL PostgreSQL
        CLOSED / DIRECT QA PASS
          ↓
CP3 persistence + migrations + real PostgreSQL harness
        CLOSED / DIRECT QA PASS
          ↓
CP4 quality / CI enforcement
        M1–M4 COMPLETE / M5 NEXT
          ↓
CP5 scaffold QA / closure
          ↓
CONCRETE LOGICAL → POSTGRESQL
        NEXT WORKSTREAM BOUNDARY
```

## 2. Quality bar

DANTE targets a production-grade engineering standard suitable for a serious long-lived product and future team growth.

For this workstream, **maximum quality does not mean maximum complexity**.

The required standard is:

- explicit architecture and ownership boundaries;
- reproducible clean-machine bootstrap;
- pinned/reviewed runtime and dependency state;
- real Linux/PostgreSQL execution semantics;
- strong typing and deterministic validation;
- secure configuration and secret handling;
- migration-first schema evolution;
- tests that prove the relevant boundary rather than mocks that merely look green;
- CI checks only after the underlying command actually exists and is trustworthy;
- excellent local debugging/IDE ergonomics without IDE dependence;
- small, understandable components that can evolve without accidental coupling;
- no placeholder folders, fake abstractions or unused infrastructure merely to resemble a large-company repository.

A simpler design is preferred when it preserves the same correctness, operability, security and future migration options.

## 3. Current verified state

Repository/workstation evidence:

```text
GitHub repository                     MattiaRubino/dante
active branch                         feature/backend-scaffold
repository rename                     COMPLETE
local workspace                       /home/mattia/projects/dante

Windows 11 host                       PASS
WSL2                                  PASS
Ubuntu 24.04 LTS                      PASS
repository on Linux filesystem        PASS
Git + GitHub CLI                      PASS
uv                                    0.12.5 / PASS
Python 3.14.7 Linux x86_64            PASS
Docker Desktop WSL2 backend           PASS
Ubuntu-24.04 Docker integration       PASS
Docker Compose                        PASS
Docker daemon access without sudo     PASS
hello-world Linux container           PASS
Docker data location on D:            PASS
```

Detailed clean-machine/onboarding instructions are in:

`docs/development/local-backend-workstation-bootstrap.md`

CP1 is materially implemented and directly validated:

```text
apps/backend production project       CREATED / REMOTE
backend virtual environment            CREATED BY uv sync
FastAPI process/bootstrap              CREATED / DIRECT STARTUP PASS
backend typed settings                 CREATED / TESTED
uv.lock                                COMMITTED / REMOTE VERIFIED
Ruff                                   DIRECT PASS
mypy strict                            DIRECT PASS
pytest                                 25/25 PASS
CP1 statement coverage                 100.00%
CP1 branch coverage                    100.00%
uv build                               PASS
real /health/live HTTP                 PASS
real /health/ready HTTP                PASS
```

CP2 is materially implemented and directly validated:

```text
DANTE PostgreSQL LOCAL image           CREATED / REMOTE / BUILD PASS
PostgreSQL                             18.4 / DIRECT PASS
PostGIS package                        3.6.4 exact / DIRECT PASS
pgvector package                       0.8.6 exact / DIRECT PASS
fresh initdb                           PASS
selected extension envelope            5/5 PASS
PostGIS capability                     PASS
pgvector capability                    PASS
pg_trgm capability                     PASS
unaccent capability                    PASS
native PostgreSQL FTS                  PASS
pg_stat_statements preload             PASS
pg_stat_statements real collection     PASS
named-volume persistence               PASS
destructive volume reset               PASS
fresh extension reinitialization       PASS
Windows DBeaver connectivity           PASS
```

CP3 is materially implemented and directly validated:

```text
SQLAlchemy/psycopg persistence         CLOSED / DIRECT QA PASS
Alembic migration harness              CLOSED / DIRECT QA PASS
real PostgreSQL integration harness    CLOSED / DIRECT QA PASS
runtime/migrator application roles     CLOSED / DIRECT QA PASS
CP3 transaction tests                  CLOSED / DIRECT QA PASS
CP3 DB outage/recovery tests           CLOSED / DIRECT QA PASS
PostgreSQL acceptance                  18/18 PASS
full backend pytest                    50/50 PASS
full-run coverage                      97.42% evidence only; not threshold
uv build                               PASS
concrete business schema               NOT STARTED
```

CP4 is materially implemented through M4, but remote PR calibration is not yet claimed:

```text
CP4 contract                           CREATED / UPDATED / REMOTE
uv required-version                    ==0.12.5 / MATERIALIZED
Backend CI workflow                    MATERIALIZED
Dependency Review workflow             MATERIALIZED
Dependabot uv + github-actions          MATERIALIZED
Actions full-SHA pins                  MATERIALIZED
uv checksum verification               MATERIALIZED
finite CI timeouts                     MATERIALIZED
M3 local fast suite                    32/32 PASS
M3 local PostgreSQL suite              18/18 PASS
M4 main reconciliation                 COMPLETE
M4 post-merge regression               DIRECT PASS
main behind_by                         0
required status checks                 0 / unchanged
remote PR calibration                  NOT RUN / M5 NEXT
CodeQL post-main activation            DEFERRED / NOT RUN
```

## 4. Execution strategy

Do not create the complete scaffold in one undifferentiated write.

Use ordered checkpoints. Each checkpoint receives its own exact Git write gate, local direct validation and remote exact-delta QA before the next checkpoint is authorized.

```text
CP1  Python/backend process + typed config                       CLOSED / DIRECT QA PASS
 ↓
CP2  reproducible LOCAL PostgreSQL infrastructure                CLOSED / DIRECT QA PASS
 ↓
CP3  persistence + migration + real-PostgreSQL harness           CLOSED / DIRECT QA PASS
 ↓
CP4  repository quality/CI enforcement                           M1–M4 COMPLETE / M5 NEXT
 ↓
CP5  full scaffold QA + closure/handoff
```

A checkpoint may be split further if implementation evidence shows that doing so improves reviewability or fault isolation.

## 5. CP1 — Backend Python/process/config foundation — CLOSED

### Goal

Materialize the smallest real backend project that can be installed reproducibly, started under Linux/WSL, configured through the accepted typed settings boundary and tested without yet depending on PostgreSQL.

### Detailed authority

The complete CP1 design and implementation evidence live in:

`docs/development/backend-cp1-contract.md`

That document is the authority for:

- CP1-01 dependency/version policy;
- CP1-02 `pyproject.toml`, Ruff, mypy, pytest and coverage policy;
- CP1-03 FastAPI application factory and typed Settings contract;
- the complete `DANTE_*` variable registry and meaning;
- LOCAL `.env.local` loading semantics;
- health/readiness semantics;
- OpenAPI/docs environment behavior;
- standard commands;
- test obligations;
- implementation findings and corrections;
- exact resolved dependency evidence;
- direct acceptance evidence;
- deferred-item triggers;
- permanent configuration-documentation discipline.

Do not reconstruct those decisions from conversation memory when the contract exists.

### Materialized CP1 shape

```text
apps/backend/
├── .python-version
├── pyproject.toml
├── uv.lock
├── .env.example
├── README.md
│
├── src/
│   └── dante/
│       ├── __init__.py
│       ├── bootstrap/
│       │   ├── __init__.py
│       │   └── app.py
│       └── platform/
│           ├── __init__.py
│           └── config/
│               ├── __init__.py
│               └── settings.py
│
└── tests/
    ├── test_bootstrap.py
    └── test_settings.py
```

### CP1 final state

```text
CP1-01 dependency/version policy        CLOSED / IMPLEMENTED
CP1-02 pyproject/tooling policy          CLOSED / IMPLEMENTED
CP1-03 FastAPI/settings/health policy    CLOSED / IMPLEMENTED
CP1 source/manifests                     REMOTE
CP1 uv.lock                              REMOTE / VERIFIED
CP1 direct QA                            PASS
```

Final direct project graph on 2026-08-20:

```text
fastapi             0.141.1
pydantic            2.13.4
pydantic-settings   2.15.0
uvicorn             0.52.4
httpx2               2.12.0
mypy                 2.3.1
pytest               9.1.1
pytest-cov           7.1.0
ruff                 0.16.3
```

Important evidence-driven corrections during CP1:

- Pydantic's mypy plugin was enabled after plain strict mypy produced false-positive `BaseSettings()` constructor errors;
- one narrow `type: ignore[misc]` remains only on the deliberate runtime frozen-settings mutation probe;
- `httpx` was replaced by `httpx2` after current Starlette `TestClient` behavior emitted a deprecation warning that DANTE correctly promoted to an error;
- warnings-as-errors and global mypy strictness were preserved;
- `.coverage` is ignored as a generated local artifact.

### CP1 explicitly did not create

```text
modules/ capability tree
kernel/ primitives without proven shared meaning
empty observability/security/clock/identifier layers
SQLAlchemy mappings
persistence adapters
Alembic migrations
PostgreSQL connection code
business/domain schema
business HTTP routes
backend OCI Dockerfile
PowerSync
Restate
R2
OR-Tools integration
PgBouncer runtime path
cloud/IaC/provider resources
frontend implementation
```

The accepted application structure remains the architectural target, but empty layers are not materialized for ceremony.

## 6. CP2 — Reproducible LOCAL PostgreSQL infrastructure — CLOSED

CP2 closed on 2026-08-20 after its complete approved direct acceptance contract passed on the canonical Windows 11 + WSL2 + Docker Desktop workstation.

### Detailed authority

The durable CP2 design, implementation findings, operating model and direct closure evidence live in:

`docs/development/backend-cp2-postgres-contract.md`

Do not reconstruct CP2 from chat history when that contract exists.

### Materialized CP2 shape

```text
infra/
├── local/postgres/
│   ├── Dockerfile
│   └── initdb/010-extensions.sql
└── compose/
    ├── local.yaml
    └── README.md
```

The repository also ignores the workstation-local Compose secret file through `.gitignore`.

### Final selected LOCAL database envelope

```text
Docker Compose
        ↓
DANTE-owned PostgreSQL build/config
        ↓
PostgreSQL 18.4
+ PostGIS 3.6.4
+ pgvector 0.8.6
+ pg_trgm
+ unaccent
+ pg_stat_statements preload + extension
+ native PostgreSQL FTS capability
```

Direct closure evidence includes:

```text
Compose config validation                 PASS
immutable postgres:18.4-trixie digest     PASS
clean/no-cache image build                PASS
exact PostGIS/pgvector package pins       PASS
fresh cluster init                        PASS
010-extensions.sql                        PASS
five selected extensions                  PASS
functional capability probes              PASS
pg_stat_statements actual collection      PASS
normal down/up persistence                PASS
down --volumes destructive reset          PASS
fresh post-reset reinitialization          PASS
Windows DBeaver 127.0.0.1:5432            PASS
```

The first clean build exposed a real TLS trust-store prerequisite: the pinned PostgreSQL base contained the PGDG signing key but did not have Debian `ca-certificates` installed in the final filesystem. The accepted repair installs the Debian trust store before using the PGDG historical archive over HTTPS and preserves both TLS verification and PGDG signed-repository verification. The repaired no-cache build passed directly.

PgBouncer remains selected but is not forced into every day-one LOCAL connection. Its activation belongs to the concrete pooling/compatibility validation boundary.

### CP2 final state

```text
DANTE PostgreSQL image       PASS
PostgreSQL 18.4              PASS
PostGIS 3.6.4                PASS
pgvector 0.8.6               PASS
pg_trgm                      PASS
unaccent                     PASS
pg_stat_statements           PASS
native FTS                   PASS
named-volume persistence     PASS
explicit reset               PASS
Windows GUI connectivity     PASS
CP2                          CLOSED / DIRECT QA PASS
```

CP2 does not imply application persistence, Alembic, privilege separation, Logical mapping, restore/PITR or Physical HG/PSV PASS.

## 7. CP3 — Persistence, migrations and real PostgreSQL harness — CLOSED / DIRECT QA PASS

### Detailed authority

The complete accepted CP3 design, materialized boundary and closure evidence live in:

`docs/development/backend-cp3-persistence-contract.md`

Do not reconstruct CP3 from conversation history when that contract exists.

### Accepted architecture

```text
Settings / DatabaseSettings
        ↓
one AsyncEngine per process
        ↓
one async_sessionmaker per process
        ↓
one AsyncSession per application operation/task
        ↓
explicit transaction boundary
        ↓
PostgreSQL 18.4
```

Key rules:

- `postgresql+psycopg` async SQLAlchemy boundary;
- `pool_pre_ping=True`;
- `autobegin=False`, `expire_on_commit=False`, `autoflush=True`;
- outer application operation owns commit/rollback;
- persistence adapters never commit implicitly;
- no generic `Repository[T]` / generic Unit of Work;
- liveness is process-only;
- readiness performs a bounded real PostgreSQL probe for the CP3 outage model;
- no hidden SQL/transaction retry;
- no long external/AI I/O while holding an unnecessary DB transaction.

### Alembic/schema governance

```text
application schema     dante
version table          dante.alembic_version
one canonical DAG/head
technical baseline     20260820_01
```

Alembic authenticates as `dante_migrator`, explicitly performs `SET ROLE dante_owner`, governs only the `dante` schema and does not treat `public` extension/provider objects as DANTE-owned schema.

`metadata.create_all()` is not deployment authority.

### PostgreSQL identity model

```text
dante_owner      NOLOGIN object owner
dante_migrator   LOGIN / NOINHERIT / SET dante_owner allowed / ADMIN denied
dante_runtime    LOGIN / NOINHERIT / no owner membership / DML-only posture
```

The runtime has no default DDL, TRUNCATE, TEMP, owner escalation, migration-history access or routine EXECUTE capability.

### Materialized dependency resolution

```text
SQLAlchemy       2.0.52
psycopg          3.3.4
Alembic          1.19.1
pytest-asyncio   1.4.0
```

The lock was generated directly with `uv` on the canonical WSL workstation and pushed at:

```text
17c00d2ac24d2efecfc52f7fa5f707f5b15c36cd
```

### Real PostgreSQL acceptance harness

PostgreSQL-marked tests use the exact CP2-built image:

```text
dante-postgres-local:18.4
```

They start one disposable loopback-only cluster per pytest PostgreSQL session, then create fresh provisioned/migrated databases inside that isolated cluster.

This is intentionally stronger than using the ordinary LOCAL cluster because PostgreSQL roles are cluster-global. Acceptance provisioning must not change the developer's real `dante_runtime` / `dante_migrator` credentials.

The harness therefore proves the same DANTE image/envelope while keeping the ordinary LOCAL database and roles untouched.

The cluster readiness predicate uses `SHOW server_version_num = 180004`, avoiding package/distribution suffixes while retaining an exact PostgreSQL 18.4 assertion.

Outage/recovery acceptance uses stop/start of the same disposable container. This closes live connections while preserving the database state needed to prove readiness recovery without restarting the backend process.

### CP3 final state

```text
CP3-01 stack/version design              CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-02 connection/config/lifecycle       CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-03 transaction architecture          CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-04 Alembic/schema governance         CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-05 PostgreSQL privileges             CLOSED / MATERIALIZED / DIRECT QA PASS
CP3-06 real PostgreSQL harness/matrix    CLOSED / MATERIALIZED / DIRECT QA PASS
CP3 uv.lock                              REMOTE / GENERATED BY uv / VERIFIED
CP3 direct QA                            PASS
```

No concrete Logical owner/table mapping is authorized by CP3. The technical probe objects created by tests exist only inside disposable acceptance databases and are not canonical schema.

### Direct closure evidence

Implementation/direct-QA HEAD:

```text
35cf6440bc121a38342f6bbee72e210435a788a4
```

Directly recorded on the canonical WSL/Docker workstation on 2026-08-20:

```text
uv lock --check                         PASS
uv tree --locked --depth 1              PASS
uv sync --locked                         PASS
ruff format --check .                    PASS — 23 files already formatted
ruff check .                             PASS
mypy                                    PASS — 20 source files
pytest -m "not postgres"                PASS — 32/32
pytest -m postgres                       PASS — 18/18 in 15.61s
full pytest                              PASS — 50/50 in 24.72s
full-run coverage                        97.42% evidence only; not threshold
uv build                                 PASS
sdist + wheel                            PASS
fresh DB → Alembic head                  PASS
head → base → head                       PASS
alembic check / no DANTE drift           PASS
privilege allow/deny matrix              PASS
runtime identity/search_path             PASS
stale pooled-connection recovery         PASS
real DB outage live 200 / ready 503      PASS
DB recovery ready 200, no app restart    PASS
commit / rollback / flush / SAVEPOINT    PASS
```

Remote exact-scope QA from the original CP3 PRE-SCOPE to the executable QA HEAD:

```text
PRE-SCOPE       a09936d168de48909d948425387b168d016911e8
QA HEAD         35cf6440bc121a38342f6bbee72e210435a788a4
ahead_by        45
behind_by       0
changed paths   27
expected paths  27
unexpected      0
deleted         0
```

The 97.42% coverage figure is run evidence, not a permanent arbitrary project threshold.

### Evidence-driven hardening finding

`docker pause` was directly shown to represent a stronger frozen/blackholed-peer condition: TCP may remain open while PostgreSQL cannot respond, and driver cancellation/cleanup may exceed the Python-level readiness timeout.

CP3 therefore does not claim a bounded wall-clock readiness result for a frozen/blackholed peer. That stronger scenario remains a separate hardening item; it is not hidden by the accepted stop/start outage test.

## 8. CP4 — Quality and CI enforcement — M1–M4 COMPLETE / M5 NEXT

### Detailed authority

The complete accepted CP4 design, materialized boundary, security posture, sequence and acceptance matrix live in:

`docs/development/backend-cp4-ci-contract.md`

Do not reconstruct CP4 from conversation history when that contract exists.

### Materialized architecture

```text
Backend CI
├── Backend Quality
├── Backend PostgreSQL
└── Backend CI Gate
    ├── always executes after mandatory upstream jobs resolve
    └── PASS iff every mandatory upstream result == success

Dependency Review
└── separate repository-wide workflow/check candidate
```

Materialized files:

```text
apps/backend/pyproject.toml
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
.github/dependabot.yml
```

Exact uv authority:

```text
workstation uv                 0.12.5
pyproject required-version     ==0.12.5
```

Materialized immutable Action pins:

```text
actions/checkout
3d3c42e5aac5ba805825da76410c181273ba90b1  # v7.0.1

astral-sh/setup-uv
c771a70e6277c0a99b617c7a806ffedaca235ff9  # v9.0.0

actions/dependency-review-action
a1d282b36b6f3519aa1f3fc636f609c47dddb294  # v5.0.0
```

The setup-uv path includes explicit checksum verification for uv 0.12.5 rather than disabling integrity checking.

Finite job timeouts:

```text
Backend Quality      15 minutes
Backend PostgreSQL   30 minutes
Backend CI Gate       5 minutes
Dependency Review    10 minutes
```

Key frozen rules remain:

- GitHub-hosted `ubuntu-24.04` runner initially;
- no workflow-level `paths` filtering on future required workflows;
- `pull_request` to `main`, `push` to `main` and manual execution for Backend CI;
- superseded PR validation may be cancelled; accepted-main validation is not cancelled merely because a newer main commit exists;
- workflow token permissions default to none and are granted minimally per job;
- checkout jobs receive only `contents: read` and disable persisted checkout credentials;
- ordinary PR CI receives no PROD/deployment identity or secrets;
- `pull_request_target` is not used for normal validation;
- no arbitrary coverage threshold;
- architecture-linter dependency remains deferred until a meaningful package graph exists;
- CodeQL default setup remains a separate post-backend-main direct-validation boundary.

### M1–M3 evidence

Before M4, the materialized CP4 surface passed its approved local/non-mutating checks and remote exact-delta/readback QA.

Direct backend regression evidence retained from M3:

```text
uv                               0.12.5
fast/non-PostgreSQL pytest       32/32 PASS
PostgreSQL acceptance            18/18 PASS
required status checks           0 / unchanged
```

YAML existence is not remote CI PASS. Exact emitted check names and GitHub Actions behavior remain unproven until M5.

### M4 — main reconciliation — DIRECT PASS

M4 consumed:

```text
main
ff46eb16b971b1fde96eef9047b09faa02e1a5db

M4 PRE-SCOPE / tested post-merge HEAD
ba0d994e983cf3e5add6ad640c238999f418e236

two-parent merge commit
6a8122249f13f9b8553f511c47b4185c6e3e6540
```

The merge imported 14 non-overlapping `main` paths byte-identically and semantically reconciled the four shared current-truth files:

```text
README.md
docs/PROJECT-STATUS.md
docs/README.md
docs/ROADMAP.md
```

Remote relation after reconciliation:

```text
main → feature/backend-scaffold
behind_by       0
ahead_by        97
main ancestor   YES
```

M4 PRE-SCOPE → reconciled HEAD contained exactly the 18 expected paths and no unexpected backend/CI/database mutation.

The canonical workstation then reran the accepted regression suite on exact HEAD `ba0d994e983cf3e5add6ad640c238999f418e236`. The user directly confirmed every command passed:

```text
git status --short                       CLEAN
uv --version                             0.12.5
uv lock --check                          PASS
uv sync --locked                         PASS
ruff format --check .                    PASS
ruff check .                             PASS
mypy                                    PASS
pytest -m "not postgres"                PASS — 32/32
uv build                                PASS
docker build --pull dante-postgres...   PASS
pytest -m postgres -vv                   PASS — 18/18
final git status                         CLEAN
final HEAD                               ba0d994e983cf3e5add6ad640c238999f418e236
```

Therefore:

```text
CP4-M1   COMPLETE
CP4-M2   COMPLETE
CP4-M3   COMPLETE
CP4-M4   COMPLETE / DIRECT PASS
CP4-M5   NEXT / NOT STARTED
```

### What M4 does not prove

M4 does not claim:

```text
GitHub Actions remote green
exact emitted check contexts
Backend CI Gate remote semantics
Dependency Review uv.lock visibility
Dependency Review deliberate-policy failure
required status checks
repository full-SHA setting enforcement
CodeQL PASS
CP4 closure
```

Those remain M5–M9 work.

## 9. CP5 — Scaffold QA and closure

Before the scaffold workstream can close, directly prove at minimum:

```text
exact changed paths                            PASS
clean locked backend dependency bootstrap      PASS
Python 3.14.7 project interpreter              PASS
backend process starts under Linux/WSL         PASS
typed config tests                             PASS
Ruff/mypy/pytest actual commands                PASS
DANTE PostgreSQL image builds                  PASS
PostgreSQL 18.4 starts/health                   PASS
selected extension envelope                    PASS
pg_stat_statements preload/extension            PASS
basic psycopg/SQLAlchemy async connection       PASS
Alembic base → head                             PASS
real PostgreSQL integration harness             PASS
initial CI emitted contexts observed remotely   PASS where activated
```

Do not convert this into false blanket validation. Direct Physical HG/PSV obligations remain NOT RUN unless the specific required scenario is actually exercised.

After CP5 closure, the next bounded scope is concrete Logical → PostgreSQL implementation.

## 10. Persistent non-goals for this workstream

Until explicitly reopened by a later boundary, do not add:

- concrete 57-owner table mapping;
- business capability modules merely to reserve names;
- product HTTP/API surface;
- AuthN/AuthZ implementation;
- frontend internals/toolchain;
- cloud provider/IaC engine;
- DEV/UAT/PROD infrastructure;
- PowerSync implementation;
- Restate activation;
- R2 implementation;
- OR-Tools implementation;
- pgBackRest/AWS recovery activation;
- production deployment pipeline;
- event sourcing, Redis, Kafka or other already-excluded infrastructure by convenience.

## 11. Exact resume point for the next chat

A new conversation must not redesign Engineering Foundation, repeat CP1/CP2 work, redesign CP3-01..CP3-06, reopen the closed CP4 design without contradictory evidence or jump directly into concrete PostgreSQL business schema mapping.

Resume in this exact order:

```text
1. Read current project truth, this handoff and backend-cp4-ci-contract.md.
2. Verify feature/backend-scaffold remote/local HEAD and clean tree.
3. Treat CP1, CP2 and CP3 as CLOSED / DIRECT QA PASS.
4. Treat CP4-M1 through CP4-M4 as COMPLETE; M4 post-main regression is DIRECT PASS.
5. Treat current main ff46eb16... as already reconciled into the backend branch; verify it has not advanced before PR creation.
6. Do not repeat broad CI/toolchain research by default.
7. Open a fresh exact write/PR gate for CP4-M5 before creating the real calibration PR or mutating PR metadata.
8. CP4-M5: open the real PR to main, observe Backend Quality / Backend PostgreSQL / Backend CI Gate / Dependency Review runs, inspect jobs/logs and record exact emitted contexts/sources.
9. Do not configure required checks during M5.
10. If M5 is green, open a separate bounded M6 calibration gate for deliberate red behavior.
11. M6 must prove aggregate-gate failure semantics and real Dependency Review behavior on a policy violation/uv.lock delta.
12. M7 restores green and proves recovery.
13. Only after M5–M7 evidence propose the separate M8 repository/ruleset gate for required contexts/full-SHA enforcement where supported.
14. M9 records CP4 closure evidence only after the acceptance matrix is truthfully satisfied or an item is explicitly deferred as unsupported/out of boundary.
15. Then proceed to CP5 full scaffold QA/closure.
16. Keep concrete Logical → PostgreSQL owner/table mapping deferred until scaffold closure.
```

### Immediate next action

**CP4-M5 is the next boundary. Do not create the calibration PR, deliberate-red changes or repository/ruleset mutations without a fresh exact gate.**
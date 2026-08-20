# Backend CP2 PostgreSQL Technical Contract

- Status: **CLOSED / DIRECT QA PASS**
- Workstream: `docs/workstreams/backend-scaffold.md`
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Parent checkpoint: **CP1 CLOSED / DIRECT QA PASS**
- CP2 design decisions: **APPROVED / IMPLEMENTED / DIRECTLY VERIFIED**
- Design/source verification date: **2026-08-20**
- Direct closure date: **2026-08-20**
- Implementation authority: **EVERY FURTHER WRITE STILL REQUIRES ITS OWN EXACT GATE**

## 1. Purpose

This document is the durable technical and acceptance contract for **CP2 — reproducible LOCAL PostgreSQL infrastructure**.

CP2 exists to prove a real PostgreSQL environment before DANTE adds application persistence code. It deliberately isolates database infrastructure from SQLAlchemy, psycopg, Alembic and Logical-to-physical schema work so failures can be attributed to the correct layer.

CP2 did not earn PASS because files existed or a container started. It closed only after direct Docker/PostgreSQL/capability/persistence/host-connectivity evidence succeeded on the canonical WSL/Docker Desktop workstation.

## 2. Quality rule

The CP2 target is production-grade engineering discipline for LOCAL infrastructure without pretending LOCAL is production.

Required properties:

- real PostgreSQL 18.4 semantics;
- DANTE-owned reproducible image definition;
- immutable upstream base identity;
- exact selected PostGIS and pgvector package versions;
- no random all-extensions image;
- deterministic fresh-cluster initialization;
- persistent Docker-managed local state;
- explicit destructive reset semantics;
- minimal localhost exposure;
- no production credentials;
- direct capability evidence rather than presence-by-assumption;
- no application persistence abstractions before the database itself is proven.

Maximum quality does not mean compiling the entire GIS dependency stack from source or adding unused infrastructure.

## 3. CP2 boundary

CP2 materializes:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/010-extensions.sql
infra/compose/local.yaml
infra/compose/README.md
```

and the repository ignore rule needed for the workstation-local PostgreSQL password.

CP2 does not materialize:

```text
SQLAlchemy
psycopg
Alembic
application DB settings
application DB connection code
runtime/migrator/owner/backup/replication roles
business/domain tables
Logical → PostgreSQL mappings
PgBouncer runtime
backend containerization
cloud infrastructure
CI database workflows
```

Those boundaries return only after CP2 direct PASS, under their own later checkpoint authority.

## 4. Decision 1 — DANTE-owned image strategy

### 4.1 Base image

Approved base intent:

```text
postgres:18.4-trixie
```

Immutable OCI index identity captured directly on the canonical workstation on 2026-08-20:

```text
sha256:a02db8cac496f15b094798a38254f14d6e00741f709360e5e00bb6668ea31636
```

Dockerfile authority:

```dockerfile
FROM postgres:18.4-trixie@sha256:a02db8cac496f15b094798a38254f14d6e00741f709360e5e00bb6668ea31636
```

The human-readable tag records intent; the digest records actual immutable base identity.

The index digest is intentionally used rather than pinning only the current `linux/amd64` child manifest so supported developers on another architecture can resolve the corresponding platform image from the same immutable index.

### 4.2 Extension packages

Exact direct packages:

```text
postgresql-18-postgis-3
3.6.4+dfsg-2.pgdg13+1

postgresql-18-pgvector
0.8.6-1.pgdg13+1
```

The Dockerfile installs these from the official PostgreSQL APT historical archive distribution:

```text
trixie-pgdg-archive
```

This archive contains all released versions rather than only the current candidate package, allowing the exact approved versions to remain addressable after newer PGDG builds appear.

The image reuses the PostgreSQL Official Image PGDG signing key already present under `/usr/local/share/keyrings/postgres.gpg.asc`; it does not download a second trust root.

The base image's final filesystem did not include the Debian `ca-certificates` package. CP2 therefore installs the Debian Trixie trust store before contacting the PGDG historical archive over HTTPS, verifies that the CA bundle exists, and preserves normal TLS certificate verification plus PGDG `signed-by` verification.

The build verifies the installed package versions with `dpkg-query` and verifies that the PostGIS/vector extension control files exist.

### 4.3 Explicit non-strategies

CP2 does not:

- use `postgis/postgis` as the DANTE runtime base;
- compile PostGIS/pgvector or GEOS/PROJ/GDAL from source;
- use floating extension package versions;
- run `apt upgrade`;
- install a second PostgreSQL server;
- add unselected extension bundles;
- disable TLS certificate verification;
- allow unauthenticated APT packages.

The objective is reproducible ownership of the DANTE database image without unnecessary supply-chain complexity.

## 5. Decision 2 — LOCAL Compose topology

Compose project:

```text
dante-local
```

Service:

```text
postgres
```

No manual `container_name` is used. Compose project/service identity owns generated container/network names and future container DNS remains `postgres`.

### 5.1 Network exposure

Published host endpoint:

```text
127.0.0.1:5432 -> container 5432
```

The port is bound to loopback rather than all host interfaces.

Verified CP2 consumers:

- WSL/Linux host tools;
- DBeaver on Windows.

PyCharm Database Tools remains a supported equivalent host GUI path, but DBeaver supplied the direct CP2 Windows boundary evidence.

A future Compose service would connect internally using `postgres:5432`; the backend remains direct-in-WSL during CP2.

### 5.2 Database/bootstrap identity

Fresh cluster environment:

```text
POSTGRES_DB=dante
POSTGRES_USER=postgres
POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
```

`postgres` is a synthetic LOCAL bootstrap administrator only. It must not be treated as the future application runtime identity.

Runtime/migrator/owner/backup/replication privilege classes return at the persistence/recovery boundaries where their semantics can be tested honestly.

### 5.3 LOCAL secret

Workstation-local file:

```text
infra/compose/secrets/postgres_password.local
```

The repository ignores:

```text
infra/compose/secrets/*.local
```

The Compose secret mounts the password as:

```text
/run/secrets/postgres_password
```

The real secret is never committed. On the first workstation it was generated with high-entropy random material, created with mode `0600`, and directly verified as ignored by Git. It must not be reused in DEV/UAT/PROD.

### 5.4 Persistent data

Compose named volume:

```text
postgres-data
```

Container mount for PostgreSQL 18:

```text
/var/lib/postgresql
```

PostgreSQL 18 official images changed the data-volume boundary from the historical `/var/lib/postgresql/data` layout. CP2 deliberately follows the PostgreSQL 18 image contract.

Lifecycle semantics:

```text
docker compose ... down
→ containers/network removed
→ PostgreSQL named volume retained


docker compose ... down --volumes
→ containers/network removed
→ PostgreSQL named volume destroyed
```

Therefore:

```text
RECREATE != RESET
```

Both sides of this distinction were directly proven during CP2 closure.

### 5.5 Health

The service healthcheck uses TCP:

```text
pg_isready -h 127.0.0.1 -p 5432 -U postgres -d dante
```

TCP is intentional. During the PostgreSQL Official Image's temporary init server, `listen_addresses` is disabled; the healthcheck therefore cannot report healthy merely because the internal bootstrap server/socket exists while init scripts are still executing.

Health proves that PostgreSQL accepts TCP connections. It does not replace extension/capability acceptance SQL.

### 5.6 Restart posture

No automatic `restart: always` or `restart: unless-stopped` policy is added for LOCAL. The developer controls when the database consumes workstation resources.

## 6. Decision 3 — cluster configuration and initialization

### 6.1 Required startup configuration

Compose starts PostgreSQL with:

```text
shared_preload_libraries=pg_stat_statements
compute_query_id=on
```

These are runtime server arguments rather than `ALTER SYSTEM` mutations or a custom copied `postgresql.conf`.

No performance tuning is invented at CP2. In particular CP2 does not set arbitrary values for:

```text
shared_buffers
work_mem
max_connections
pg_stat_statements.max
pg_stat_statements.track
pg_stat_statements.track_planning
```

### 6.2 Fresh-cluster extensions

`/docker-entrypoint-initdb.d/010-extensions.sql` activates exactly:

```sql
CREATE EXTENSION postgis VERSION '3.6.4';
CREATE EXTENSION vector VERSION '0.8.6';
CREATE EXTENSION pg_trgm;
CREATE EXTENSION unaccent;
CREATE EXTENSION pg_stat_statements;
```

Target database:

```text
dante
```

CP2 does not modify `template1` and does not invent a custom extension schema before concrete physical schema/privilege work exists.

`IF NOT EXISTS` is deliberately absent. A fresh-cluster bootstrap that encounters unexpected prior extension state must fail visibly rather than silently accepting an unknown object/version.

### 6.3 Init scripts are not migrations

The PostgreSQL Official Image runs `/docker-entrypoint-initdb.d` only against an empty data directory.

Therefore:

```text
new volume
→ initdb
→ 010-extensions.sql

existing initialized volume
→ init scripts do not rerun
```

Schema evolution is not implemented through edits to initdb scripts. Alembic/migration governance returns at CP3.

If fresh initialization fails during future LOCAL setup:

1. inspect the actual error;
2. correct the cause through an authorized change;
3. explicitly destroy the disposable LOCAL volume when reset is intended;
4. create a fresh cluster;
5. rerun the applicable acceptance checks.

No fake automatic rollback/resume layer is added around initdb.

## 7. Decision 4 — operating model

Canonical commands are documented in `infra/compose/README.md` and run from repository root.

Configuration validation:

```bash
docker compose -f infra/compose/local.yaml config --quiet
```

Build:

```bash
docker compose -f infra/compose/local.yaml build postgres
```

Canonical clean-build proof:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

Start/wait:

```bash
docker compose -f infra/compose/local.yaml up -d --wait
```

Preserving stop:

```bash
docker compose -f infra/compose/local.yaml down
```

Destructive reset:

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

The password must exist before Compose execution that consumes the secret definition.

## 8. CP2 direct acceptance contract — SATISFIED

CP2 remained **NOT PASS** until every applicable requirement below had direct evidence. All approved CP2 acceptance requirements were directly satisfied on 2026-08-20.

### 8.1 Repository/build evidence

```text
exact authorized changed paths                         PASS
remote readback                                         PASS
Compose model parses                                   PASS
immutable base digest resolves                         PASS
clean/no-cache PostgreSQL image build                  PASS
installed PostGIS package exact                        PASS
installed pgvector package exact                       PASS
```

Direct built-image evidence:

```text
PostgreSQL binary
18.4 (Debian 18.4-1.pgdg13+1)

postgresql-18-postgis-3
3.6.4+dfsg-2.pgdg13+1

postgresql-18-pgvector
0.8.6-1.pgdg13+1

PostGIS/vector extension control files
PASS
```

### 8.2 Fresh-cluster evidence

The first accepted bootstrap started with the Compose named volume absent and directly proved:

```text
container/service starts                               PASS
Compose health becomes healthy                         PASS
fresh initdb completes                                 PASS
010-extensions.sql completes                           PASS
CREATE EXTENSION x5                                    PASS
```

Server version query:

```sql
SHOW server_version;
```

Observed:

```text
18.4 (Debian 18.4-1.pgdg13+1)
```

### 8.3 Extension inventory

Observed direct inventory:

```text
pg_stat_statements  1.12
pg_trgm             1.6
postgis             3.6.4
unaccent            1.1
vector              0.8.6
```

Exactly the five selected CP2 extensions were present in the acceptance query, with the exact selected PostGIS and pgvector versions.

### 8.4 Capability probes

Direct functional results:

```text
PostGIS_Full_Version()                  PASS — POSTGIS 3.6.4 reported
'[1,2,3]'::vector(3)                    PASS — [1,2,3]
similarity('dante','dante')             PASS — 1
unaccent('città')                       PASS — citta
native PostgreSQL FTS                   PASS — true
```

FTS is a native PostgreSQL capability; CP2 does not pretend it is a separately installed extension.

### 8.5 `pg_stat_statements` proof

Direct configuration evidence:

```text
shared_preload_libraries = pg_stat_statements
compute_query_id = on
```

Functional collection probe:

```sql
SELECT 424242 AS dante_pgss_probe;
```

Observed in `pg_stat_statements`:

```text
SELECT $1 AS dante_pgss_probe | calls = 1
```

This proves actual statistics collection rather than extension presence alone.

### 8.6 Persistence proof

Disposable QA state:

```text
cp2_persistence_probe
dante-cp2-persisted
```

After:

```text
docker compose ... down
docker compose ... up -d --wait
```

the marker was still present with the exact value:

```text
dante-cp2-persisted
```

Named-volume persistence across container/network recreation therefore passed directly.

### 8.7 Destructive reset proof

After:

```text
docker compose ... down --volumes
docker compose ... up -d --wait
```

Docker directly reported removal and recreation of `dante-local_postgres-data`.

Post-reset SQL proved:

```text
public.cp2_persistence_probe   ABSENT
five selected extensions      PRESENT
postgis                       3.6.4
vector                        0.8.6
container health              HEALTHY
```

This directly proves the difference between container recreation and cluster reset, plus deterministic fresh extension reinitialization.

### 8.8 Windows host connectivity

DBeaver on Windows directly connected through:

```text
Host      127.0.0.1
Port      5432
Database  dante
User      postgres
Password  workstation-local ignored secret
```

The GUI query:

```sql
SELECT current_database(), current_user, version();
```

returned:

```text
current_database = dante
current_user     = postgres
version          = PostgreSQL 18.4 ...
```

This is direct Windows-host boundary evidence and is not inferred from container health.

## 9. CP2 final state — CLOSED / DIRECT QA PASS

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

The final LOCAL database after the reset proof is a fresh healthy cluster with the selected extension envelope initialized and no persistence QA table retained.

## 10. Direct-validation limits

CP2 evidence does **not** imply PASS for:

```text
SQLAlchemy/psycopg application connectivity
Alembic migrations
runtime/migrator privilege separation
Logical → physical schema mapping
migration rehearsal
restore/PITR
concurrency/idempotency harnesses
PowerSync
Restate
PgBouncer
production deployment
Physical HG/PSV obligations not specifically exercised
```

Those remain NOT RUN unless their exact scenario is directly executed later.

## 11. Source-verification record

Version-sensitive design evidence was refreshed on **2026-08-20** using primary upstream sources, including:

- PostgreSQL official release/documentation;
- PostgreSQL Official Docker Image source/documentation;
- Docker Compose specification/CLI documentation;
- PostgreSQL PGDG APT repository/archive documentation;
- official PGDG package pools for PostGIS and pgvector;
- PostGIS project release/support information;
- pgvector upstream release/package information.

The immutable PostgreSQL OCI index digest was captured directly with:

```bash
docker buildx imagetools inspect postgres:18.4-trixie
```

Observed platform child on the first workstation:

```text
linux/amd64
sha256:4cc13dede823cab4e05290c7fb3350fb4e599ecabd9b07e6706b5d5e8f5bc929
```

The Dockerfile intentionally pins the index digest rather than this platform-specific child digest.

## 12. Exact resume point

CP2 is closed. Resume in this order:

```text
1. Pull the CP2 closure documentation HEAD to the canonical WSL checkout.
2. Verify feature/backend-scaffold remote/local HEAD and a clean working tree.
3. Treat CP1 and CP2 as CLOSED / DIRECT QA PASS unless new direct evidence contradicts them.
4. Begin CP3 READ-ONLY design/research for persistence, migrations and a real-PostgreSQL harness.
5. Re-check current official versions/compatibility for SQLAlchemy 2.x, psycopg 3 and Alembic before freezing CP3 dependencies.
6. Define typed DB settings, async engine/session ownership, transaction boundaries, migration authority and real PostgreSQL test lifecycle.
7. Define the first runtime/migrator privilege split only where CP3 can directly test it.
8. Keep concrete Logical-owner/table mapping out of CP3.
9. Present a fresh exact CP3 Git write gate before any CP3 repository write.
10. Proceed to CP4 only after CP3 direct acceptance passes.
```

No CP3/application/schema write is authorized by this CP2 closure record alone.

## 13. Direct implementation finding — PGDG archive TLS trust bootstrap

The first canonical clean/no-cache image build on 2026-08-20 failed before any PostGIS or pgvector package installation.

Observed failure boundary:

```text
https://apt-archive.postgresql.org/pub/repos/apt
SSL connection failed: certificate verify failed
```

The subsequent `Unable to locate package` messages were downstream effects of the PGDG archive index not being downloaded; they were not evidence that the approved package versions were absent.

Direct diagnosis used the exact pinned PostgreSQL base image. It proved:

```text
base OCI digest
sha256:a02db8cac496f15b094798a38254f14d6e00741f709360e5e00bb6668ea31636

ca-certificates in final base filesystem
NOT INSTALLED

PGDG signing key
PRESENT at /usr/local/share/keyrings/postgres.gpg.asc
```

An ephemeral diagnostic container then installed Debian Trixie `ca-certificates` and verified the same archive TLS endpoint with OpenSSL:

```text
Verification: OK
Verify return code: 0 (ok)
```

A second ephemeral proof preserved HTTPS and the existing PGDG `signed-by` keyring policy, refreshed the archive index successfully, and proved that the exact approved package versions are present in `trixie-pgdg-archive`:

```text
postgresql-18-postgis-3 | 3.6.4+dfsg-2.pgdg13+1
postgresql-18-pgvector  | 0.8.6-1.pgdg13+1
```

Therefore the accepted repair is intentionally narrow:

```text
Debian Trixie repositories
→ install ca-certificates
→ verify non-empty system CA bundle
→ switch PGDG source to HTTPS trixie-pgdg-archive
→ keep signed-by=/usr/local/share/keyrings/postgres.gpg.asc
→ install exact PostGIS/pgvector package pins
```

Explicitly rejected responses to this finding:

```text
disable TLS certificate verification
allow unauthenticated APT packages
replace HTTPS with an insecure bypass
change approved extension versions
abandon the official PGDG archive
source-build the GIS/vector stack merely to avoid the trust-store prerequisite
```

After the authorized repair was pulled, the same canonical clean-build command was rerun:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

It completed successfully and exported `dante-postgres-local:18.4`. The built-image version/control-file inspection then passed, so the TLS finding is **RESOLVED / DIRECTLY VERIFIED**.

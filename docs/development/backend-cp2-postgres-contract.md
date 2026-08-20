# Backend CP2 PostgreSQL Technical Contract

- Status: **ACTIVE IMPLEMENTATION / DIRECT QA NOT YET EARNED**
- Workstream: `docs/workstreams/backend-scaffold.md`
- Branch: `feature/backend-scaffold`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Parent checkpoint: **CP1 CLOSED / DIRECT QA PASS**
- CP2 design decisions: **APPROVED**
- Design/source verification date: **2026-08-20**
- Implementation authority: **EVERY FURTHER WRITE STILL REQUIRES ITS OWN EXACT GATE**

## 1. Purpose

This document is the durable technical and acceptance contract for **CP2 — reproducible LOCAL PostgreSQL infrastructure**.

CP2 exists to prove a real PostgreSQL environment before DANTE adds application persistence code. It deliberately isolates database infrastructure from SQLAlchemy, psycopg, Alembic and Logical-to-physical schema work so failures can be attributed to the correct layer.

CP2 does not earn PASS because files exist or a container starts. It closes only after direct Docker/PostgreSQL/capability/persistence/host-connectivity evidence succeeds on the canonical WSL/Docker Desktop workstation.

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

Those boundaries return only after CP2 direct PASS.

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

The build verifies the installed package versions with `dpkg-query` and verifies that the PostGIS/vector extension control files exist.

### 4.3 Explicit non-strategies

CP2 does not:

- use `postgis/postgis` as the DANTE runtime base;
- compile PostGIS/pgvector or GEOS/PROJ/GDAL from source;
- use floating extension package versions;
- run `apt upgrade`;
- install a second PostgreSQL server;
- add unselected extension bundles.

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

Expected consumers at CP2:

- WSL/Linux host tools;
- DBeaver on Windows;
- PyCharm Database Tools on Windows.

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

The real secret is never committed. It is generated with high-entropy random material under a restrictive local umask and must not be reused in DEV/UAT/PROD.

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

If fresh initialization fails partway during CP2 development:

1. inspect the actual error;
2. correct the cause through an authorized change;
3. explicitly destroy the disposable LOCAL volume;
4. create a fresh cluster;
5. rerun acceptance.

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

First CP2 clean-build proof:

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

## 8. CP2 direct acceptance contract

CP2 remains **NOT PASS** until every applicable requirement below has direct evidence.

### 8.1 Repository/build evidence

```text
exact authorized changed paths                         REQUIRED
remote readback                                         REQUIRED
Compose model parses                                   REQUIRED
immutable base digest resolves                         REQUIRED
clean/no-cache PostgreSQL image build                  REQUIRED
installed PostGIS package exact                        REQUIRED
installed pgvector package exact                       REQUIRED
```

### 8.2 Fresh-cluster evidence

Start from no `postgres-data` volume and prove:

```text
container/service starts                               REQUIRED
Compose health becomes healthy                         REQUIRED
fresh initdb completes                                 REQUIRED
010-extensions.sql completes                           REQUIRED
```

Server version query:

```sql
SHOW server_version;
```

Expected:

```text
18.4
```

### 8.3 Extension inventory

Run:

```sql
SELECT extname, extversion
FROM pg_extension
WHERE extname IN (
    'postgis',
    'vector',
    'pg_trgm',
    'unaccent',
    'pg_stat_statements'
)
ORDER BY extname;
```

Required names:

```text
pg_stat_statements
pg_trgm
postgis
unaccent
vector
```

Required exact selected versions:

```text
postgis  3.6.4
vector   0.8.6
```

### 8.4 Capability probes

PostGIS:

```sql
SELECT PostGIS_Full_Version();
```

pgvector:

```sql
SELECT '[1,2,3]'::vector(3);
```

pg_trgm:

```sql
SELECT similarity('dante', 'dante');
```

Expected result: `1`.

unaccent:

```sql
SELECT unaccent('città');
```

Expected result: `citta`.

Native PostgreSQL FTS:

```sql
SELECT
    to_tsvector('simple', 'dante personal operating system')
    @@ plainto_tsquery('simple', 'dante');
```

Expected result: `true`.

FTS is a native PostgreSQL capability; CP2 must not pretend it is a separately installed extension.

### 8.5 `pg_stat_statements` proof

Configuration:

```sql
SHOW shared_preload_libraries;
SHOW compute_query_id;
```

Required:

```text
shared_preload_libraries contains pg_stat_statements
compute_query_id = on
```

Functional collection proof:

```sql
SELECT 424242 AS dante_pgss_probe;

SELECT query, calls
FROM pg_stat_statements
WHERE query LIKE '%dante_pgss_probe%';
```

The probe must be observable in statistics. Merely creating the extension is insufficient evidence.

### 8.6 Persistence proof

Create a disposable QA object/value, for example:

```sql
CREATE TABLE cp2_persistence_probe (
    marker text PRIMARY KEY
);

INSERT INTO cp2_persistence_probe(marker)
VALUES ('dante-cp2-persisted');
```

Then:

```text
docker compose ... down
docker compose ... up -d --wait
```

After container recreation, query:

```sql
SELECT marker FROM cp2_persistence_probe;
```

Required value:

```text
dante-cp2-persisted
```

Then remove the QA table after the persistence proof unless the subsequent reset proof deliberately uses its existence as the reset marker.

### 8.7 Destructive reset proof

Run:

```text
docker compose ... down --volumes
docker compose ... up -d --wait
```

Required:

- prior persistence probe no longer exists;
- fresh cluster is healthy;
- all five selected extensions are present again;
- PostGIS/vector exact extension versions are still correct.

This directly proves the difference between container recreation and cluster reset.

### 8.8 Windows host connectivity

DBeaver or PyCharm Database Tools on Windows must connect using:

```text
Host      127.0.0.1
Port      5432
Database  dante
User      postgres
Password  local secret file contents
```

Run from the GUI connection:

```sql
SELECT current_database(), current_user, version();
```

Required:

```text
current_database = dante
current_user     = postgres
PostgreSQL       = 18.4 line
```

This is direct host-boundary evidence and is not inferred from container health.

## 9. Expected CP2 final state

Only after all direct acceptance passes may documentation state:

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

Until then the status remains implementation/QA active.

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

After CP2 files are remotely materialized and read back, proceed in this order:

```text
1. Pull the exact CP2 implementation HEAD to the canonical WSL checkout.
2. Confirm working tree clean before local-only secret creation.
3. Generate infra/compose/secrets/postgres_password.local and verify Git ignores it.
4. Run Compose config validation.
5. Run the clean/no-cache PostgreSQL image build.
6. Inspect installed package versions from the built image.
7. Start from a fresh volume and wait for Compose health.
8. Run server-version, extension inventory and capability probes.
9. Prove pg_stat_statements configuration + real collection.
10. Prove data persistence through down/up recreation.
11. Prove destructive reset semantics with down --volumes.
12. Prove Windows DBeaver/PyCharm host connectivity.
13. Record final direct evidence through a separate exact documentation gate.
14. Proceed to CP3 only after CP2 CLOSED / DIRECT QA PASS.
```

No CP3/application/schema work is authorized by this contract.

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

This finding does not earn the clean-build requirement. After the repository repair is pulled, the same canonical command must be rerun:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

Only a successful post-repair build can advance CP2 beyond the image-build acceptance boundary.

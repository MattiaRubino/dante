# TEMPORARY BOOTSTRAP — Concrete Logical → PostgreSQL

- Status: **TEMPORARY SESSION-BOOTSTRAP / DELETE AFTER REAL WORKSTREAM HANDOFF EXISTS**
- Branch: `feature/logical-postgresql`
- Branch origin / protected-main anchor: `fd3bc8dd918cf6aadeff4572221af68612c3cb42`
- Product: **DANTE**
- Repository: `MattiaRubino/dante`
- Purpose: allow a fresh AI/session to reconstruct the exact backend continuation point without relying on conversation memory.

> This file is intentionally disposable. It is NOT the durable design/specification for the PostgreSQL mapping. After the new session has completed read-only reconstruction and a real `docs/workstreams/...` handoff for this workstream has been approved and written, delete this bootstrap file in an explicit gated scope.

## 1. Exact continuation point

Protected `main` has already integrated the complete production backend scaffold.

```text
main
fd3bc8dd918cf6aadeff4572221af68612c3cb42

CP1  CLOSED / DIRECT QA PASS
CP2  CLOSED / DIRECT QA PASS
CP3  CLOSED / DIRECT QA PASS
CP4  CLOSED / DIRECT REMOTE QA PASS
CP5  CLOSED / DIRECT INTEGRATED QA PASS

PR #24 backend scaffold               MERGED
post-merge Backend CI on PR #24       PASS
PR #27 post-merge doc reconciliation  MERGED
post-merge Backend CI on PR #27       PASS

PRODUCTION BACKEND SCAFFOLD
CLOSED / INTEGRATED IN PROTECTED main

CONCRETE LOGICAL → POSTGRESQL
NOT STARTED / NEXT BACKEND IMPLEMENTATION BOUNDARY
```

This branch was created directly from that exact protected-main commit. No business schema, business migration, repository mapping, API slice or domain/application implementation has started here.

## 2. Mandatory authority rule

Repository truth outranks conversation memory.

When sources conflict, use the current project precedence defined by `docs/development/operating-rules.md` and `docs/development/agent-operating-manual.md`:

1. current `main` code/migrations/tests and accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current workstream sources;
5. historical evidence / closed branches / Git history;
6. conversation memory.

Closed Product, Domain, Logical, Physical and Engineering Foundation decisions are consumed by implementation. Do not reopen them merely because a convenient PostgreSQL/ORM shape would differ. Reopen only an affected decision when concrete contradictory implementation evidence requires it, under an explicit gate.

## 3. Mandatory fresh-session bootstrap

Before proposing schema/mapping or any repository write, read and verify in this order:

```text
README.md
→ docs/README.md
→ docs/PROJECT-STATUS.md
→ docs/ROADMAP.md
→ docs/development/agent-operating-manual.md
→ docs/development/operating-rules.md
→ docs/development/documentation-and-handoff.md
→ docs/development/branching-and-environments.md
→ docs/development/repository-engineering-safety.md
→ this temporary bootstrap
```

Then consume the closed workstreams and their complete physical parts where applicable:

```text
docs/workstreams/domain-model.md + all canonical continuation parts required by it
docs/workstreams/logical-model.md + logical-model-part-2.md ... logical-model-part-9.md
docs/workstreams/pre-physical-coherence.md
docs/workstreams/physical-model.md
docs/workstreams/engineering-foundation.md
docs/workstreams/backend-scaffold.md
```

Then inspect the current Logical sources under `docs/logical-model/`, including all split logical documents/parts that the closed Logical workstream marks as canonical. In particular, do not read only Part 1 of a size/tool-split logical document; reconstruct the complete logical payload.

Then read Physical-consuming implementation authorities, starting from:

```text
docs/physical-model/README.md
docs/physical-model/pm-02-primary-mapping-overview-v1.md
docs/physical-model/pm-03-semantic-hard-gate-preflight-v1.md
docs/physical-model/final-stack-capability-matrix-v1.md
docs/physical-model/final-stack-audit-v1.md
```

and all linked mapping/evidence/validation sources that those current authorities require for PostgreSQL-consuming implementation.

Finally inspect the real backend implementation and tests on this branch/current main, especially:

```text
apps/backend/
infra/local/postgres/
infra/compose/
.github/workflows/backend-ci.yml
.github/workflows/dependency-review.yml
```

including current SQLAlchemy metadata/session/lifespan/provisioning/Alembic/testing conventions before proposing business persistence.

## 4. Closed semantic constraints to preserve

The new implementation must preserve the accepted DANTE meaning, including at minimum:

```text
life central, not task/calendar centric
planned != actual
user authority / authorship
historical and material truth
privacy + provenance
honest uncertainty
progressive complexity
personal-first, not personal-only
AI != product authority
possibility != action != decision != preference
Effort != Execution != Outcome != Goal Progress
Person != Account != Principal != Actor
provider state != canonical DANTE state
derived projection != canonical truth
absence / unknown != false
idempotency != semantic identity
client local state != canonical accepted effect
```

`WL-H01..WL-H12` remain active and constrain implementation. Locate and read their exact current definitions before mapping schema.

The Logical Model is closed with **57/57 owners classified**. This DOES NOT mean 57 tables, 57 repositories, 57 services or 57 modules. Do not mechanically translate Logical ownership units into physical objects.

## 5. Accepted persistence / backend baseline

Current accepted baseline to consume, not redesign by default:

```text
architecture                     capability-first modular monolith
Python                           3.14.7 initial exact scaffold runtime
package / lock authority         uv
format/lint                      Ruff
typing                           mypy strict
tests                            pytest; Hypothesis where meaningful
canonical backend semantics      Linux / WSL2 on Windows
LOCAL stateful infra             Docker Compose

canonical persistence            PostgreSQL 18.4
application schema               dante
ORM / SQL toolkit                SQLAlchemy 2.0 stable
PostgreSQL driver                psycopg 3
migrations                       Alembic

PostgreSQL capabilities
PostGIS                          3.6.4
pgvector                         0.8.6
pg_trgm                          selected / materialized
unaccent                         selected / materialized
pg_stat_statements               selected / materialized
native PostgreSQL FTS            selected
```

PostgreSQL is the sole canonical persistence and material-history authority.

Existing CP3 database posture includes explicit owner/migrator/runtime identities, least-privilege runtime behavior, explicit transaction ownership, async SQLAlchemy/psycopg, Alembic baseline and real PostgreSQL acceptance tests. Read the actual code/contracts before extending them.

Selected specialist components such as PgBouncer, PowerSync, Restate, R2, pgBackRest/S3, OR-Tools and observability targets remain bounded/dormant unless a real capability activates them. Do not turn selection into activation by convenience.

## 6. First task for the new session — READ ONLY

The first task is NOT to create tables or migrations.

Perform a complete read-only reconstruction and report:

1. exact current `main` and `feature/logical-postgresql` relation;
2. complete mandatory bootstrap read;
3. exact Logical owner/reference/invariant/history/provenance constraints that affect physical persistence;
4. exact active `WL-H01..WL-H12` obligations;
5. Physical target/mapping decisions already accepted for PostgreSQL;
6. existing CP3/CP5 persistence conventions that new schema must extend rather than duplicate;
7. candidate decomposition strategy for the concrete mapping;
8. unresolved questions/true decision points, distinguishing them from already-closed decisions;
9. a proposed staged workstream/checkpoint plan for review BEFORE any schema write.

The initial mapping phase should reason about, at minimum:

```text
owner/group → physical representation
canonical identity / keys
references / FK semantics
required vs optional / unknown semantics
uniqueness
check constraints
state and lifecycle constraints
planned vs actual separation
history / temporal/material truth
provenance / authorship
delete / tombstone / retention semantics
transactional consistency boundaries
query/index requirements
JSONB only where structurally justified
PostGIS / vector / FTS only where semantically justified
migration ordering / reversibility posture
least-privilege runtime implications
real PostgreSQL acceptance strategy
```

Do not choose a physical shape merely because SQLAlchemy makes it convenient.

## 7. Expected development direction after mapping approval

The intended broad sequence is:

```text
closed Logical + Physical authorities
        ↓
read-only concrete mapping analysis
        ↓
review/freeze the first bounded physical slice
        ↓
Alembic migration(s)
        ↓
SQLAlchemy persistence mapping
        ↓
real PostgreSQL tests / constraints / migration acceptance
        ↓
application persistence adapter / vertical capability slice
        ↓
API boundary
        ↓
frontend consumption
        ↓
end-to-end acceptance
```

Prefer capability-by-capability vertical slices after the necessary physical foundation exists. Do not build the entire future database merely to feel complete.

## 8. Git / write discipline for this branch

No write is authorized by the existence of this bootstrap file.

Before EVERY new remote write scope, present the exact gate required by current operating rules:

```text
BRANCH
feature/logical-postgresql

PRE-SCOPE
<exact current SHA>

CREATE
<exact paths>

UPDATE
<exact paths>

DELETE
<exact paths>

PURPOSE
<bounded purpose>

EXPLICITLY OUT OF SCOPE
<exact non-scope>
```

Obtain explicit user approval. Immediately before the first write verify `current HEAD == approved PRE-SCOPE`; if not, STOP, inspect and re-gate.

After writes, prove exact changed paths/status, remote payload readback, ahead/behind relation and applicable tests/checks before calling PASS/CLOSED.

`main` remains protected. Normal integration is bounded branch → PR → required checks → protected-main merge. Current required checks include `Backend CI Gate` and repository-wide `Dependency Review`, with branch-up-to-date required.

## 9. Explicit non-goals at bootstrap

Until separately approved, do NOT:

- write business tables or business migrations;
- add placeholder capability modules/directories;
- introduce generic Repository/UoW/BaseService abstractions;
- weaken Domain/Logical semantics to fit SQL/ORM convenience;
- activate PowerSync/Restate/R2/OR-Tools/PgBouncer/etc. without a real trigger;
- add microservices, Kafka, Redis, Kubernetes, extra repositories or environment branches;
- change CI/rulesets/CodeQL;
- modify frontend or brand assets;
- rewrite global status/roadmap merely for session bookkeeping;
- merge this branch;
- delete historical evidence.

## 10. Temporary-file retirement protocol

Once the new session has:

```text
READ-ONLY reconstruction complete
+ exact workstream decomposition reviewed
+ real durable workstream handoff path agreed
```

then create the real workstream handoff under `docs/workstreams/` in an explicitly approved gate. The real handoff becomes the branch-local save-game.

After that handoff has been written and remotely verified, delete:

```text
docs/workstreams/logical-postgresql-bootstrap.md
```

in an explicit gated scope. Do not carry this temporary bootstrap into final `main` unless there is a deliberate reason to retain it.

## 11. Resume instruction

A fresh session should say it is aligned only after it has actually read the required current repository sources and verified Git state. It must not rely on this file alone.

First output should be a concise alignment report plus the proposed READ-ONLY mapping/checkpoint plan. **Do not perform schema/migration/source writes until a new exact write gate is presented and explicitly approved.**

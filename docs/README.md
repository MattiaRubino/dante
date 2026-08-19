# DANTE Documentation Index

This directory is the durable documentation authority for DANTE.

## Current authority order

When sources conflict, use this order:

1. current `main` code/migrations/tests and current accepted model/ADR;
2. current durable product/domain/logical/architecture/engineering docs on `main`;
3. active bounded workstream handoff for newer unmerged work;
4. other current sources inside that workstream;
5. historical evidence/closed branches/Git history;
6. conversation memory.

Conversation instructions may clarify intent but do not silently override durable repository truth.

## Current lifecycle status

```text
Product/North Star                 CURRENT
Domain Model                       CLOSED
Logical Model                      CLOSED
Pre-Physical coherence             CLOSED
Physical target                    CLOSED / ACCEPTED
Engineering Foundation v0          CLOSED / ACCEPTED
Production backend scaffold        NOT STARTED
Concrete PostgreSQL schema         NOT STARTED
Direct HG / PSV                    NOT RUN
```

## Mandatory entry points

### Project/current truth

- `../README.md`
- `PROJECT-STATUS.md`
- `ROADMAP.md`

### Development governance

- `development/agent-operating-manual.md`
- `development/operating-rules.md`
- `development/documentation-and-handoff.md`
- `development/branching-and-environments.md`
- `development/repository-engineering-safety.md`

### Engineering Foundation — closed

- `workstreams/engineering-foundation.md` — closure/handoff and exact next boundary
- `development/engineering-foundation-v0.md` — master engineering contract
- `development/repository-layout-v0.md` — monorepo/path ownership
- `development/application-structure-v0.md` — backend modular architecture
- `development/environments-and-promotion-v0.md` — LOCAL/DEV/UAT/PROD
- `development/config-and-secrets-v0.md` — backend configuration/secrets
- `development/toolchain-and-dx-v0.md` — Python/WSL2/PyCharm/Docker/PostgreSQL local developer baseline
- `development/testing-and-ci-v0.md` — backend testing/CI/security/supply-chain baseline

### Architecture

- `architecture/README.md`
- `architecture/system-overview.md`
- `architecture/technical-decisions.md`

### Domain / Logical / Physical

Use the model indexes and their linked accepted sources. For any Physical-consuming implementation, at minimum reread:

- PM-11 accepted target;
- PM-12 selected stack/operational posture;
- post-selection validation register.

Historical evidence remains historical. Do not rewrite it to pretend it knew later decisions.

## Engineering Foundation final decisions

The closed backend/repository baseline is:

```text
one product monorepo
apps/backend + apps/web + apps/mobile
backend capability-first modular monolith
Python 3.14.x / initial 3.14.7
uv / Ruff / mypy strict / pytest / Hypothesis
Windows 11 host supported via WSL2/Linux backend semantics
PyCharm WSL interpreter supported; repo remains IDE-neutral
Docker Compose for LOCAL stateful infrastructure
PostgreSQL 18.4 with full selected extension envelope enabled from first LOCAL DB
SQLAlchemy 2.0 stable line + psycopg 3 + Alembic
risk-governed migrations / logical copy / recovery separation
typed pydantic-settings configuration
workload identity + secret manager + OIDC target
risk-layered real-PostgreSQL testing
GitHub Actions / protected main / supply-chain hardening
```

Frontend internal tooling/testing/release implementation is explicitly deferred to the dedicated frontend workstream.

Cloud/compute provider and IaC engine are explicitly deferred until first remote infrastructure.

## Repository identity

Production implementation continues in the existing repository. Creating a new repo is not the plan.

Repository identity governance is complete:

```text
historical repository   MattiaRubino/lifeos
current repository      MattiaRubino/dante
rename                   COMPLETE
```

Historical/closed documents may still record the pre-rename repository decision as historical truth. Current-truth documents and new implementation work use `MattiaRubino/dante`.

## Exact next handoff

```text
1. Mandatory bootstrap from current repository truth.
2. Open a fresh exact Git write gate for production scaffold.
3. Scaffold apps/backend + LOCAL PostgreSQL/migration/test/config/CI baseline only.
4. Run scaffold QA.
5. Only then begin concrete Logical → PostgreSQL implementation.
```

No production application code or concrete schema is authorized merely by Engineering Foundation closure; every next write still requires its own exact scope.

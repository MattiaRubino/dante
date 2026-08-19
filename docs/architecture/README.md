# DANTE Architecture Index

- Status: **CURRENT**

## 1. Architecture state

```text
Domain Model                  CLOSED
Logical Model                 CLOSED
Pre-Physical coherence        CLOSED
Physical target               CLOSED / ACCEPTED
Engineering Foundation v0     CLOSED / ACCEPTED
Production implementation     NOT STARTED
Direct PSV                    NOT RUN
```

## 2. Current architecture entry points

- `system-overview.md` — current system/component/authority overview
- `technical-decisions.md` — current accepted technical decision register
- `../workstreams/engineering-foundation.md` — closed Engineering Foundation handoff
- `../development/engineering-foundation-v0.md` — complete backend engineering contract

For implementation, also consume the Domain/Logical/Physical indexes and accepted detailed sources.

## 3. Current system direction

DANTE is a single product with three top-level application boundaries in one monorepo:

```text
apps/backend
apps/web
apps/mobile
```

Backend begins as a capability-first modular monolith.

PostgreSQL 18.4 is the sole canonical persistence authority.

Selected specialist components remain bounded and activate only at their real implementation/release triggers.

## 4. Engineering Foundation decisions

Backend baseline includes:

- Python 3.14.x / initial 3.14.7;
- uv;
- WSL2/Linux canonical backend workflow on Windows;
- PyCharm WSL interpreter supported, repository IDE-neutral;
- Docker Compose for LOCAL stateful dependencies;
- real PostgreSQL 18.4 with full selected extension envelope enabled from first LOCAL DB;
- SQLAlchemy 2.0 stable line + psycopg 3 + Alembic;
- capability-specific persistence/application boundaries;
- migration risk governance and logical-copy/recovery separation;
- pydantic-settings typed configuration;
- workload identity/secret manager/OIDC target;
- real-PostgreSQL risk-layered testing;
- GitHub Actions + protected-main/supply-chain baseline;
- LOCAL/DEV/UAT/PROD environment model with provider deferred.

## 5. Explicit deferrals

Engineering Foundation does not freeze:

- web/mobile internal architecture/toolchain/testing/release details;
- cloud/compute provider;
- IaC engine;
- registry/provider sizing;
- concrete backend capability-module map;
- database tables/columns/migrations;
- API route/version surface;
- AuthN/AuthZ mechanism.

These open only at their implementation boundaries.

## 6. Repository identity

Continue in the existing repository. Do not create a new implementation repo.

Repository rename `lifeos → dante` is the recommended next small governance operation before production scaffold unless explicitly deferred.

## 7. Architecture reopen discipline

Closed Domain/Logical/Physical/Foundation decisions are not casually reselected during implementation.

A concrete implementation contradiction may justify an explicit affected-scope reopen. Convenience or a preferred library behavior is not sufficient reason to weaken accepted semantics.

## 8. Next architecture-consuming work

```text
repository rename decision/action
        ↓
production apps/backend scaffold
        ↓
scaffold QA
        ↓
concrete Logical → PostgreSQL mapping/schema
        ↓
first backend vertical slice
```

Direct HG/PSV evidence remains NOT RUN until real harness/artifacts execute the required scenarios.

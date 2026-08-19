# Application Structure v0

- Status: **CLOSED / ACCEPTED**
- Scope: backend internal architecture and application boundaries
- Frontend internal architecture: **DEFERRED**
- Production code: **NOT CREATED**

## 1. Architectural style

DANTE backend begins as a **capability-first modular monolith** with enforceable dependency boundaries.

```text
MODULAR MONOLITH
!= unstructured monolith
!= one giant service layer
!= one module per table
!= one module per Logical owner
!= future extraction forbidden
```

One deployable backend preserves operational simplicity and local ACID transactions while internal boundaries preserve future extraction options.

Extraction requires evidence such as independent scaling, security isolation, availability, ownership, release cadence or technology lifecycle that outweighs distributed-system cost.

## 2. Backend target shape

Target inside `apps/backend/src/dante/`:

```text
dante/
├── bootstrap/
│   ├── app.py
│   ├── lifespan.py
│   └── wiring.py
│
├── kernel/
│   └── <small stable cross-capability primitives only>
│
├── platform/
│   ├── config/
│   ├── database/
│   ├── observability/
│   ├── security/
│   ├── clock/
│   └── identifiers/
│
└── modules/
    └── <capability>/
        ├── domain/
        ├── application/
        ├── ports/
        ├── adapters/
        │   ├── inbound/
        │   │   └── http/
        │   └── outbound/
        │       ├── persistence/
        │       └── integrations/
        └── public.py
```

This is a dependency model, not a mandate that every capability contains every folder. Empty layers are omitted.

## 3. Capability module rule

A module groups behavior/change cohesion, not storage nouns.

Forbidden mechanical mappings:

```text
57 Logical owners → 57 Python modules
1 table → 1 module
1 HTTP route → 1 module
1 UI screen → 1 backend module
```

The concrete module map is created during implementation by consuming the closed Domain/Logical clusters and the first real vertical slices.

## 4. Dependency direction

Conceptually:

```text
DOMAIN
  ↑
APPLICATION → PORTS
  ↑            ↑
ADAPTERS ──────┘

BOOTSTRAP / COMPOSITION ROOT
wires concrete implementations
```

Rules:

- `domain/` knows Python/domain primitives only;
- `application/` orchestrates use cases and depends on domain + explicit ports;
- `ports/` express required external capabilities only where the abstraction protects a real boundary/test seam;
- inbound adapters translate transport/runtime input to application calls;
- outbound adapters implement database/provider/tool boundaries;
- `bootstrap/` owns FastAPI composition, concrete wiring and lifecycle resources;
- `platform/` owns bounded shared technical infrastructure, not business meaning.

## 5. Domain purity

Domain/application semantics are not coupled by identity to:

- FastAPI request/response objects;
- SQLAlchemy mapped rows/sessions;
- Pydantic transport DTOs;
- provider SDK objects;
- OpenTelemetry span objects;
- Restate runtime objects;
- PowerSync protocol objects;
- Cloudflare/AWS resource identifiers.

Pydantic may validate/serialize technical boundaries without forcing all Domain objects to inherit from Pydantic models.

SQLAlchemy mappings may resemble Domain state without becoming canonical Domain identity.

## 6. Kernel rule

`kernel/` contains only genuinely stable cross-capability primitives whose shared meaning is proven.

```text
kernel small
kernel low-change
kernel != shared/common/utils
```

A helper used in two places is not automatically kernel material.

## 7. Cross-module interaction

A module's private implementation is not another module's API.

Allowed, chosen per use case:

1. explicit narrow application/public interface;
2. typed command/query interface;
3. in-process event where temporal decoupling is genuinely valuable;
4. explicit read model/query interface;
5. stable kernel value type.

Forbidden:

```text
module A imports module B persistence adapter
module A mutates B SQLAlchemy row directly
module A reaches into B private internals for convenience
service-locator lookups
```

Cross-module PostgreSQL transactions remain allowed where accepted multi-owner semantics require truthful atomicity. Module boundaries do not force fake distributed workflows.

## 8. Public interfaces

`public.py` is a narrow exported application surface, not a second framework.

It may expose:

- typed application requests/results;
- stable application interfaces;
- stable events;
- already-accepted cross-module value/reference types.

It must not expose:

- SQLAlchemy models/sessions;
- FastAPI request objects;
- provider clients;
- private persistence adapters;
- private module implementation merely for convenience.

## 9. Application use-case boundary

Consequential operations are use cases, not CRUD methods.

A use case owns, as applicable:

- semantic target resolution;
- expected/material-state checks;
- Authority/AuthZ/governance enforcement via appropriate boundaries;
- transaction scope;
- idempotency/equivalence handling;
- canonical state transition;
- history/provenance obligations;
- outbox/effect staging;
- reconciliation/result semantics.

HTTP verb/path does not define canonical operation identity.

## 10. Persistence architecture

### SQLAlchemy role

SQLAlchemy 2.0 stable line is the baseline persistence toolkit against PostgreSQL 18.4.

Use ORM and/or Core/reviewed SQL where each is clearest. Recursive, search, geospatial, vector or reporting queries are not forced through object navigation if explicit Core/SQL is safer and easier to reason about.

### Repository rule

No universal generic repository abstraction:

```python
Repository[T].get(id)
Repository[T].save(entity)
Repository[T].delete(id)
```

as the semantic model of DANTE.

Persistence interfaces are shaped by capability/use-case invariants when an abstraction is useful, e.g. operations whose names express the semantic intent rather than generic CRUD.

### Session / transaction boundary

- session scoped to one application operation/request/job;
- session injected, never global;
- one `AsyncSession` is never shared across concurrent tasks;
- commit/rollback controlled by the application/use-case transaction boundary;
- adapters do not silently commit behind a caller that owns a larger transaction;
- implicit/lazy DB I/O is avoided in domain/application logic;
- explicit Unit-of-Work abstraction is optional and only accepted if it clarifies, rather than hides, PostgreSQL transaction semantics.

## 11. Async policy

```text
HTTP/provider/database I/O
async where supported and useful

pure domain/application calculation
synchronous by default
```

Async is an I/O tool, not a style requirement propagated into pure code.

## 12. FastAPI boundary

FastAPI is an inbound HTTP adapter/process host.

Routes:

- translate HTTP/auth/request state into application input;
- call application interfaces;
- translate results/errors to stable transport contracts;
- do not own core business orchestration;
- do not open ad-hoc sessions outside the established persistence boundary;
- do not derive canonical effect identity from URL/method alone.

Global middleware is limited to true cross-cutting transport concerns such as request identity, security headers, observability context and bounded error translation.

## 13. Error model

Implementation distinguishes at least:

```text
domain/application rejection
expected-state/conflict failure
authorization/governance denial
not-found / intentionally undisclosed
invalid transport input
provider/external failure
transient infrastructure failure
internal defect
```

HTTP status is a transport projection, not canonical semantic identity.

Error body, status, timing and side effects must preserve WL-H12 non-interference requirements.

## 14. Schema/change boundary

Persistence mappings and migrations obey `engineering-foundation-v0.md` and `testing-and-ci-v0.md`:

- Alembic migration authority;
- autogenerate candidate only;
- immutable applied revisions;
- migration risk classification;
- expand/migrate/contract;
- bounded resumable backfills;
- explicit lock/rewrite review;
- schema drift checks;
- separate runtime/migrator privileges.

## 15. Background work

### Class A

The already-selected PostgreSQL transactional outbox + bounded worker lives inside the modular backend when a real Class-A async use case appears.

Outbox record and canonical state transition are in the same transaction where semantics require atomicity.

Worker entrypoints call the same application boundaries as HTTP; they do not create a duplicate business implementation.

### Class B

Restate remains selected but dormant until the fixed first real Class-B durable-workflow trigger.

When activated, Restate handlers are runtime/inbound adapters invoking application use cases. Restate runtime state does not become canonical DANTE history.

## 16. Provider/object integrations

Provider SDKs live in outbound adapters.

Example when ContentArtifact bytes activate:

```text
ContentArtifact semantics
        ↓ port
R2 adapter
        ↓
raw object bytes
```

Provider locator/state remains distinct from canonical DANTE identity/metadata/provenance.

Integration Hub modes must remain explicit; import, sync, live read, retrieval and action/tool integration are not collapsed into one ambiguous provider interface.

## 17. Observability boundary

Backend emits privacy-minimized operational signals through the accepted observability boundary.

From first real service scaffold, design for:

- request/operation correlation identity;
- release SHA/build identity;
- structured logs;
- safe metric/trace context;
- default sensitive-payload redaction;
- no telemetry ID used as DANTE NativeRef/MaterialStateRef/provenance identity.

Business behavior does not depend on Grafana availability.

## 18. Architecture enforcement

Documentation is not enough. Once source exists, automated architecture checks enforce at least:

```text
domain --X--> FastAPI
domain --X--> SQLAlchemy
domain --X--> provider SDKs
module A --X--> module B private adapters/internals
production --X--> prototypes
```

Use the lightest reliable enforcement mechanism; exact package/import-lint tool is selected during scaffold against the concrete Python graph.

## 19. Frontend relationship

`apps/web` and `apps/mobile` are sibling clients of the governed backend contract.

This document does not define their internal architecture/toolchain. Frontend decisions belong to the dedicated frontend workstream.

Backend authority remains authoritative for consequential canonical effects; client-side behavior/validation cannot become a bypass.

## 20. Extraction rule

No component becomes a service because a folder became large.

Extraction requires a written case covering:

- independent operational/ownership boundary;
- data ownership/consistency consequence;
- API/version consequence;
- failure and availability modes;
- observability/security consequence;
- independent deployment benefit;
- migration path;
- why modular-monolith isolation is insufficient.

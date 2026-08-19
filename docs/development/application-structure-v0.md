# Application Structure v0

- Status: **Engineering Foundation branch baseline — pending closure**
- Scope: internal architecture of future API/web/mobile production applications
- Production code: **NOT CREATED BY THIS DOCUMENT**

## 1. Architectural style

DANTE begins as a **capability-first modular monolith** with explicit dependency boundaries.

This choice combines:

- one deployment/runtime boundary while the product is young;
- local ACID transactions where accepted semantics require them;
- simple operational topology;
- explicit internal modules that can later be extracted only if a measured independent lifecycle appears.

```text
MODULAR MONOLITH
!= unstructured monolith
!= one giant service layer
!= one module per database table
!= one module per Logical owner
!= future microservices forbidden forever
```

A future extraction requires evidence such as independent scaling, security isolation, ownership, release cadence, availability or technology needs that outweigh distributed-system cost.

## 2. Backend target tree

Target shape inside `apps/api/src/dante/`:

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

This is a dependency model, not a mandate that every module contains every folder. Empty layers are omitted.

## 3. Capability module rule

Modules are selected from behavior/change cohesion, not from database nouns.

A module should own a stable business/application capability boundary. The first concrete module map is created during implementation after consuming the closed Domain/Logical clusters and real vertical slices.

Forbidden mechanical mappings:

```text
57 Logical owners -> 57 Python modules
1 table -> 1 module
1 API route -> 1 module
1 screen -> 1 backend module
```

Several accepted owners may belong to one capability, and one owner may participate in several use cases without becoming a generic technical root.

## 4. Backend dependency direction

Within one capability:

```text
DOMAIN
  ^
  |
APPLICATION -----> PORTS
  ^                 ^
  |                 |
ADAPTERS -----------+

BOOTSTRAP / COMPOSITION ROOT
may depend on concrete implementations to wire them
```

Practical rule:

- `domain/` knows Python/domain primitives only;
- `application/` orchestrates use cases and depends on domain + abstract ports;
- `ports/` define required external capabilities when an abstraction is genuinely useful;
- inbound adapters translate transport/provider input into application calls;
- outbound adapters implement persistence/provider/tool boundaries;
- `bootstrap/` wires FastAPI, concrete adapters, lifecycle and process resources;
- `platform/` contains bounded technical infrastructure shared by modules, not business meaning.

## 5. Domain purity

Domain/application semantics must not be coupled by identity to:

- FastAPI request/response objects;
- SQLAlchemy sessions/mapped rows;
- Pydantic HTTP DTOs;
- provider SDK objects;
- OpenTelemetry span objects;
- Restate runtime objects;
- PowerSync protocol objects;
- Cloudflare/AWS identifiers.

Pydantic remains the selected backend validation/serialization technology at technical boundaries. This does not require every domain object to inherit from `BaseModel`.

SQLAlchemy persistence mappings similarly do not become Domain objects merely because fields are similar.

## 6. Kernel rule

`kernel/` exists only for genuinely stable primitives used across capabilities whose meaning is already cross-cutting in accepted architecture.

Candidate classes of responsibility may include reference/value primitives derived from accepted Logical contracts, but only when implementation proves the shared need.

Hard rule:

```text
kernel size should stay small
kernel change frequency should be low
kernel must not become shared/common/utils
```

A helper used by two modules is not automatically kernel material.

## 7. Cross-module interaction

A module's private implementation is not a public API to other modules.

Allowed interaction mechanisms, chosen per use case:

1. explicit application/public interface exposed through `public.py`;
2. typed command/query interface;
3. in-process domain/application event where temporal decoupling is actually useful;
4. explicit read model/query interface for cross-capability reads;
5. shared stable kernel value type.

Forbidden:

```text
module A importing module B's persistence adapter
module A mutating module B's SQLAlchemy row directly
module A reaching into B's private package because it is convenient
cross-module service locator lookups
```

Cross-module database transactions remain possible inside the modular monolith when accepted multi-owner semantics require atomicity. Module boundaries must not force truthful atomic operations into fake distributed workflows.

## 8. Public interfaces and semantic ownership

`public.py` is a narrow exported application surface, not a second API framework.

It may expose:

- typed requests/results;
- application interfaces;
- stable events;
- identifiers/value types already accepted as cross-module.

It must not expose:

- SQLAlchemy models;
- database sessions;
- FastAPI request objects;
- provider clients;
- internal repositories;
- private domain implementation merely for convenience.

## 9. Application use-case boundary

Consequential operations are application use cases, not CRUD methods.

A use case owns, as applicable:

- input validation beyond transport shape;
- semantic target resolution;
- expected/material-state checks;
- Authority/AuthZ/governance enforcement through appropriate ports/services;
- transaction scope;
- idempotency/equivalence handling;
- canonical state transition;
- outbox/effect staging;
- result/reconciliation semantics;
- provenance requirements.

This preserves the Phase-8 governed-operation/effect contract rather than letting HTTP verbs define semantic operations.

## 10. Persistence architecture

### SQLAlchemy role

SQLAlchemy 2.0 is the selected persistence toolkit for the implementation baseline against PostgreSQL.

Use ORM and/or Core where each is appropriate; the project does not require ideological ORM-only or SQL-only usage.

Complex recursive/search/geospatial/vector/reporting queries may use explicit SQLAlchemy Core or reviewed SQL when that is clearer and safer than forcing object navigation.

### Repository pattern

DANTE does **not** define one generic repository abstraction.

Ports/repositories are capability-specific and exist only where they protect a meaningful application boundary or test seam.

Bad default:

```python
Repository[T].get(id)
Repository[T].save(entity)
Repository[T].delete(id)
```

as the universal application model.

Preferred direction: interfaces shaped by the use cases/invariants they support.

### Session / Unit of Work

- database session is scoped to an application operation/request/job;
- session is injected, never fetched from hidden global state;
- `AsyncSession` is never shared concurrently;
- transaction commit is controlled at an explicit application boundary;
- adapters do not silently commit behind a caller that owns a larger semantic transaction;
- lazy database I/O is avoided in application/domain code.

An explicit Unit-of-Work abstraction may be used if it clarifies transaction ownership across adapters. It must not obscure actual PostgreSQL transaction semantics.

## 11. Async policy

Async is used where it improves I/O concurrency; it is not propagated into pure code for style.

```text
HTTP/provider/database I/O boundary
async where supported/appropriate

pure domain calculation/invariant
normal synchronous function by default
```

Background concurrency must preserve session/transaction isolation. One `AsyncSession` per concurrent task/use case is the baseline.

## 12. FastAPI boundary

FastAPI is an inbound HTTP adapter and process host.

`APIRouter`s are composed from capability HTTP adapters into the application at bootstrap.

Routes:

- translate HTTP/auth/request state into application input;
- call application interfaces;
- translate application result/errors into stable transport contracts;
- do not contain core business orchestration;
- do not open ad-hoc database sessions outside the established dependency boundary;
- do not define canonical operation identity merely from URL/method names.

Global middleware is restricted to true cross-cutting transport concerns such as request IDs, security headers, observability context and bounded error handling.

## 13. Error model

The implementation will distinguish at least:

```text
domain/application rejection
conflict / expected-state failure
authorization/governance denial
not found / intentionally undisclosed
invalid transport input
provider/external failure
transient infrastructure failure
internal defect
```

Transport status codes are projections of these results, not the canonical semantic model.

Error responses and timing must preserve WL-H12 non-interference requirements; hidden resource existence must not leak through convenient error detail.

## 14. Web application structure

Target direction:

```text
apps/web/
├── src/
│   ├── app/            Next.js routing/composition
│   ├── features/       user-facing capability slices
│   ├── components/     web-only reusable presentational components
│   ├── lib/            precise technical integrations only
│   └── config/         validated public/server configuration boundary
├── public/
└── tests/
```

Rules:

- Next.js `app/` routing does not become the business architecture;
- business-facing UI behavior is grouped by feature/capability;
- server-only and browser-safe code have explicit boundaries;
- secrets never enter browser bundles;
- generated API client is consumed from `packages/api-client`;
- raw fetch calls are not duplicated ad hoc across features when the governed client exists;
- server components/actions do not bypass backend authority to reach canonical persistence directly.

The web client never receives direct PostgreSQL credentials.

## 15. Mobile application structure

Target direction:

```text
apps/mobile/
├── app/                Expo Router navigation when scaffolded
├── src/
│   ├── features/
│   ├── components/
│   ├── platform/
│   ├── config/
│   └── sync/           only when offline/sync implementation activates
├── assets/
├── tests/
└── .maestro/
```

Rules:

- navigation paths do not define Domain ownership;
- device/platform capability adapters are isolated from feature meaning;
- PowerSync/SQLite implementation remains behind a bounded sync/data interface;
- local SQLite is explicitly noncanonical;
- consequential offline mutations re-enter backend revalidation before PostgreSQL commit;
- mobile secrets do not exist: any value in the binary is considered public/extractable.

Expo **development builds** are the canonical production-grade development path once the mobile production app is scaffolded. Expo Go may remain useful for trivial exploration but is not the required production runtime.

## 16. Shared TypeScript policy

Share code only if the abstraction is truly platform-neutral.

Good candidates:

- generated API types/client;
- design tokens;
- pure validation/calculation utilities with identical semantics;
- lint/type configuration.

Bad candidates by default:

- one universal React component set wrapping both DOM and native;
- navigation abstraction merely to make APIs look identical;
- environment-specific platform behavior hidden behind broad `utils`;
- server-only business rules duplicated into clients as authoritative enforcement.

Client-side validation improves UX; backend validation/governance remains authoritative for consequential canonical changes.

## 17. Contract generation

Generated API client policy:

```text
FastAPI/Pydantic transport schemas
→ deterministic OpenAPI
→ pinned generator
→ packages/api-client
→ web/mobile compile against generated package
```

CI will eventually check:

1. OpenAPI generation is deterministic;
2. committed generated client matches source contract;
3. TypeScript package builds/types cleanly;
4. breaking contract changes trigger explicit review;
5. mobile compatibility requirements are respected.

Generated client types do not become the Domain Model.

## 18. Background work

### Class A

The selected PostgreSQL transactional outbox + bounded worker belongs inside the modular backend/application infrastructure when a real bounded async use case appears.

Worker entrypoints share the same application/module boundaries as HTTP entrypoints. A worker must not create a second business-logic implementation.

### Class B

Restate remains dormant until the already-fixed first real Class-B trigger. When activated, Restate handlers are inbound/runtime adapters that invoke application use cases; runtime state does not become canonical DANTE history.

## 19. Object/provider integrations

Provider SDKs live in outbound adapters.

For example, when activated:

```text
ContentArtifact application semantics
        ↓ port
R2 adapter
        ↓
raw object bytes
```

The provider client is not imported into domain objects. Object locator/provider state remains distinct from canonical ContentArtifact identity/metadata as already accepted.

Integration Hub modes remain explicit; a generic provider adapter cannot collapse import, sync, live read, retrieval and action/tool integration into one ambiguous interface.

## 20. Observability boundary

Application code emits structured operational signals through the selected observability abstraction/instrumentation boundary.

Requirements from the first real service scaffold:

- request/operation correlation identity;
- source release SHA/build identity;
- structured logs;
- metrics/traces where material;
- default redaction/no sensitive payload logging;
- no use of telemetry IDs as DANTE NativeRef/MaterialStateRef/Provenance identity.

Domain/application code does not branch business behavior on Grafana availability.

## 21. Architecture enforcement

Documentation alone is insufficient.

Once source exists, architecture tests/lint rules must enforce at least:

```text
domain does not import FastAPI/SQLAlchemy/provider SDKs
packages do not import apps
production apps do not import prototypes
module private internals are not cross-imported
client code does not import server-only modules
```

The exact import-boundary tool is selected during scaffold based on the concrete package graph; a lightweight custom/static test is preferred over a heavy framework if it proves the rule reliably.

## 22. Extraction rule

No component becomes a separate service because a folder became large.

Extraction requires a written case covering:

- independently valuable operational boundary;
- data ownership and consistency consequence;
- API/versioning consequence;
- failure modes;
- observability/security consequence;
- deployment/ownership benefit;
- migration path;
- why modular-monolith isolation is no longer sufficient.

Until then, local module boundaries are the professional default.

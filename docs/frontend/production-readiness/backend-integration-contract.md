# DANTE — Frontend / Backend Integration Contract v0

- Status: **CURRENT PRE-PRODUCTION BOUNDARY**
- Backend endpoints: **NOT DEFINED BY THIS DOCUMENT**

## 1. Objective

Make mock → real-backend replacement a bounded adapter change instead of a UI rewrite.

```text
UI component
↓
feature/application adapter
↓
frontend repository/data-source port
↓
transport client
↓
DANTE backend API
```

Direct component `fetch()`/SDK calls are not the target architecture.

## 2. Model separation

```text
Canonical Domain meaning
!= PostgreSQL / SQLAlchemy shape
!= API transport DTO
!= frontend view model
```

The backend remains authoritative for canonical DANTE semantics. The frontend receives transport contracts and maps them to purpose-built view models. A view model may combine, omit or derive presentation information without becoming canonical truth.

## 3. Data-source ports

Each feature exposes intent-specific data-source operations rather than one universal generic repository. Example categories include continuity projection, signals projection, timeline projection, capture and resolution.

The prototype may use mock adapters. Production may use HTTP/sync adapters. Both must satisfy the same frontend-facing contract.

## 4. Runtime validation

Static TypeScript types are insufficient at an untrusted network boundary. Production transport responses must be runtime-validated or generated from a validated contract before entering feature/application code.

Validation failure is an integration error, not an `empty` state.

## 5. Server state vs UI state

Server/source-backed data must use a production server-state layer with explicit:

- cache keys/identity;
- freshness/staleness policy;
- deduplication;
- cancellation;
- retry/backoff appropriate to operation type;
- invalidation/refetch rules;
- pagination/windowing where needed.

UI-only state remains outside the server cache.

No specific library is frozen here; the `apps/web` scaffold decision must select one or explicitly justify not needing one.

## 6. Mutations

Every real mutation contract must classify:

- idempotency requirement;
- optimistic update allowed/not allowed;
- expected-state/concurrency behavior;
- retry safety;
- success confirmation;
- partial/async completion semantics;
- failure recovery/undo when meaningful.

Consequential writes must not be made optimistic merely for visual speed.

## 7. Error model

The production transport boundary needs stable machine-readable error categories, not UI parsing of message strings. At minimum distinguish conceptually:

```text
validation/input
unauthenticated
authorized-but-forbidden
not-found / unavailable
conflict / stale expected state
rate/capacity/transient dependency
server/integration failure
```

Exact backend error envelopes remain a backend/API design scope.

## 8. Authentication and authorization

The client may render capability affordances, but backend authorization is authoritative. Hidden/disabled UI is not an authorization control.

The web scaffold must define session/cookie/token/CSRF/CORS/CSP strategy together with the real backend deployment boundary. This document intentionally does not invent those mechanics before the API/runtime scope exists.

## 9. Dates, locale and identity

- transport timestamps use unambiguous instants/offset semantics;
- user locale/timezone formatting happens at the client presentation boundary unless semantics require otherwise;
- stable backend identities are never replaced by list indexes or labels;
- visible translated labels are never persisted as identifiers.

## 10. Provenance and uncertainty

Where DANTE product semantics depend on provenance, freshness or uncertainty, the transport/view-model path must preserve enough information for the UI to represent it honestly. Absence/unknown must not be silently coerced to false/zero.

## 11. Offline/sync boundary

The accepted Physical target may later provide bounded client-safe sync projections. Local/synced copies remain noncanonical. Consequential offline mutations still require the accepted backend revalidation path. Prototype fixtures do not imply PowerSync activation.

## 12. Contract evolution

Breaking transport changes require explicit version/evolution handling. Production should prefer compatible additive evolution and contract tests between backend and client. The frontend view-model contract may evolve independently through explicit adapters.

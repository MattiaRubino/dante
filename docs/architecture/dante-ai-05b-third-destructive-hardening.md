# DANTE AI-05B — Full Retest Failure + Third Bounded Hardening

- **Status:** FULL RETEST FAIL BOUNDED / AI05B-H13..H15 MATERIALIZED / FINAL FRESH RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05B — Concrete Implementation Blueprint
- **Established:** 2026-09-02
- **Candidate:** `docs/architecture/dante-ai-05b-concrete-implementation-blueprint.md`
- **First hardening:** `docs/architecture/dante-ai-05b-first-destructive-hardening.md`
- **Second hardening:** `docs/architecture/dante-ai-05b-second-destructive-hardening.md`
- **PRE-SCOPE:** `9c1867c66372bf3d01f7b2cdc960f23faec22597`
- **Result:** FAIL BOUNDED
- **Architecture reopen:** NONE
- **Database/Alembic change:** NONE
- **Provider/model/SDK selection:** NONE
- **Runtime implementation:** NONE

This third bounded hardening preserves failures found only after applying AI05B-H01..H12 as one effective contract. It does not rewrite earlier failures into success.

---

# 1. Failure set

```text
AI05B-H13  Search and Intelligence public surfaces must define one concrete callable protocol each.
AI05B-H14  Lifecycle coverage must include all runtime/evidence/transport objects introduced by H08..H12.
AI05B-H15  Search navigation/result references must preserve DANTE reference-family semantics; no universal entity_id.
```

No new persistence, framework or infrastructure activation is required.

---

# 2. AI05B-H13 — concrete callable public protocols

Ownership alone is insufficient. Implementation must not invent method shape or trust semantics.

## Search public protocol

`modules/search/public.py` owns the single Search application contract used by HTTP and Intelligence.

Conceptual callable surface:

```text
class SearchService(Protocol):
    async def search(
        self,
        request: SearchExecutionRequest,
    ) -> SearchResult:
        ...

    async def resolve_navigation(
        self,
        request: NavigationExecutionRequest,
    ) -> NavigationResult:
        ...
```

`SearchExecutionRequest` is trusted application input and includes only:

```text
query/filter projection
SearchEligibilityEnvelope
requested SearchFamilyIds after intersection with active registry
current/history intent
bounded page/cursor
requested guarantee
route-owned purpose/surface
```

It cannot accept raw SQL, ORM classes, table names, provider/model routing or caller-supplied Authority/AuthZ decisions.

`SearchResult` owns:

```text
safe hits
safe facets/counts only when non-interference proof exists
pagination
achieved guarantee
limitations/unresolved classification
```

## Intelligence public protocol

`modules/intelligence/public.py` owns the first read-only Ask contract.

Conceptual callable surface:

```text
class IntelligenceService(Protocol):
    async def ask(
        self,
        request: AskExecutionRequest,
    ) -> AskResult:
        ...
```

`AskExecutionRequest` is server-constructed and includes:

```text
trusted WorkContract
trusted request/security context
user question/scope projection
execution deadline
```

It does not accept client-selected provider/model/HarnessProfile/RouteConfigIdentity/Effect authorization.

`AskResult` is already verification/publication-gated and cannot expose raw provider output as the public result.

HTTP adapters translate untrusted Pydantic DTOs into these trusted application requests only after authentication, route-owned purpose/surface resolution and current authorization/eligibility construction.

Binding:

```text
HTTP DTO != APPLICATION REQUEST
SEARCH PUBLIC PROTOCOL != SEARCH POSTGRES ADAPTER
INTELLIGENCE PUBLIC PROTOCOL != PROVIDER ADAPTER
MODEL OUTPUT != AskResult
```

---

# 3. AI05B-H14 — lifecycle completion for H08..H12 objects

AI05B-H07 remains binding. The following newer objects are explicitly covered.

| Object | Create | Persist first vertical | Mutate | Delete/release | Cache/reuse | Retry/replay | Cancel/deadline |
|---|---|---|---|---|---|---|---|
| `SearchEligibilityEnvelope` | per trusted request | no | immutable | request end | no cross-request reuse unless freshly revalidated | no | expires with request/current authorization |
| `SearchFamilyRegistration` | deploy/build config | static artifact only | immutable revision | retire by new config/release | process-local immutable registry allowed | n/a | n/a |
| `SearchExecutionRequest` | per call | no | immutable | call end | no | caller may issue a new call; not transport replay authority | request deadline |
| `SearchResult` | per call | no | immutable projection | after consumer/publication | no semantic cache by default | no blind replay semantics | request deadline |
| `SearchTargetRef` | per hit/result | no independent persistence | immutable | result lifecycle | may be copied as value only | n/a | n/a |
| `AskHttpRequest` | inbound transport | no | immutable after validation | request end | no | transport retry creates a new request unless separately idempotent | disconnect/deadline |
| `AskExecutionRequest` | server-owned per call | no | immutable | request end | no | no blind replay | request deadline |
| `AskResult` | per completed/publishable call | no default persistence | immutable | response lifecycle | no default cross-request cache | no blind replay | publication stops on disconnect |
| `ProviderAttemptRequest` | immediately before one concrete attempt | no | immutable | attempt cleanup | no | each retry/failover creates a new `ProviderAttemptId` | cancellation signal + deadline |
| `ProviderAttemptResult` | per attempt completion/known outcome | operational evidence only as required | immutable | request/evidence retention policy | no semantic cache | not replay authority | may represent cancellation/unknown outcome |
| `ProviderRuntimeEvent` | per normalized provider event | operational evidence only as required | immutable | after bounded buffering/evidence handling | no | dedupe only using bounded transport/attempt evidence | stop publication does not erase late attempt evidence |
| `CancellationSignal` | per RequestExecutionScope | no | one-way state transition | scope end | no | n/a | requested != confirmed != quiesced |
| `RequestExecutionScope` | per request | no | bounded technical state | cleanup at outcome/deadline | no | no cross-request reuse | owns deadline/attached cancellation |
| `RuntimeEvidenceEvent` | at governed runtime boundaries | operational evidence plane only | immutable | evidence retention policy | aggregation may be derived, not semantic reuse | exporter retry must not duplicate semantic application effects | deadline/backpressure must not widen safety |
| `RouteConfigIdentity` | on validated config load/snapshot | artifact/evidence as specified, not Domain state | immutable | retired revision remains traceable where evidence requires | process-local immutable snapshot allowed | n/a | emergency deny can make route unusable without mutating identity |
| `EffectOutcome.NO_EFFECT` | per first-vertical effect finalization | no canonical row | immutable | request end | no | n/a | inherited request deadline |

Any later persistence proposal for these objects requires the normal survival/materiality trigger and may not be inferred from this table.

---

# 4. AI05B-H15 — typed SearchTargetRef, not universal entity identity

Search is cross-cutting, but DANTE explicitly rejects a universal semantic `Entity` root.

A Search result therefore must not collapse all targets into:

```text
entity_id: UUID
```

or infer semantic type from a table name.

Freeze a technical discriminated value contract:

```text
SearchTargetRef
= one of
  NativeTargetRef(NativeRef, native_owner_kind)
  ScopedTargetRef(ScopedRecordRef, scoped_record_kind)
  MaterialStateTargetRef(MaterialStateRef, material_facet)
  ExternalTargetRef(ExternalRef, source_kind)
```

Only variants already supported by accepted DANTE reference semantics may be used.

Rules:

```text
SearchTargetRef != new Domain identity
SearchTargetRef != universal EntityRef
SearchTargetRef != table primary-key wrapper
SearchTargetRef preserves original reference-family meaning
```

A hit may also carry a separate `source_ref`/basis/currentness reference when the navigation target and evidentiary source are not the same thing.

Navigation dispatch uses the discriminated target contract and owning capability public seam. Intelligence cannot reinterpret a UUID by guessing which DANTE owner/table it belongs to.

Architecture tests must reject:

```text
generic EntityId / EntityRef introduced for Search convenience
raw table-name + UUID navigation
loss of NativeRef vs ScopedRecordRef vs MaterialStateRef vs ExternalRef distinction
model-generated target type coercion
```

---

# 5. Updated final-retet obligations

The final fresh AI-05B retest must cover at least B05-01..B05-44 plus:

```text
B05-45 Search public protocol has one owner and concrete callable contract.
B05-46 Intelligence public Ask protocol returns only verification/publication-gated result.
B05-47 HTTP adapters cannot bypass trusted application request construction.
B05-48 every H08..H12 runtime/evidence object has explicit lifecycle coverage.
B05-49 Search result/navigation preserves accepted DANTE reference-family semantics.
B05-50 no generic EntityRef/entity_id/table+uuid abstraction is introduced.
```

Required compounds include:

```text
hidden Search row + pagination/facet/rank + SearchTargetRef navigation
stale Search basis + current AuthZ change + Ask publication
client disconnect + provider ambiguous outcome + unknown usage + evidence exporter failure
config emergency deny + in-flight attempt + late result + publication closed
malicious HTTP authority fields + family hint + provider hint + effect attempt
```

Only a clean fresh pass may proceed to reverse acceptance.

---

# 6. Current status

```text
AI-05B initial candidate                MATERIALIZED
AI05B-H01..H07                          MATERIALIZED
AI05B-H08..H12                          MATERIALIZED
AI05B-H13..H15                          MATERIALIZED
FINAL FRESH DESTRUCTIVE RETEST          REQUIRED
REVERSE AI-05B→05A→04→PRE05→03→02      HOLD
AI-05B CLOSED                           NO
AI-05 WHOLE PHASE CLOSED                NO
DATABASE CHANGE                         NONE
PROVIDER/MODEL/SDK                      OPEN
IMPLEMENTATION                          NONE
```

# DANTE AI-05B — First Destructive Pass + Bounded Hardening

- **Status:** FIRST DESTRUCTIVE PASS FAIL BOUNDED / AI05B-H01..H07 MATERIALIZED / FRESH RETEST REQUIRED
- **Branch:** `feature/ai-architecture`
- **Phase:** AI-05 — Whole-System Acceptance + Implementation Blueprint
- **Sub-phase:** AI-05B — Concrete Implementation Blueprint
- **Established:** 2026-09-02
- **Candidate under test:** `docs/architecture/dante-ai-05b-concrete-implementation-blueprint.md`
- **Candidate commit:** `7ef0dbef5c995a1ce71d0edc853398dc2a90ad69`
- **Upstream:** AI-05A CLOSED / STRUCTURALLY ACCEPTED / BD-01..BD-41
- **Result:** FAIL BOUNDED
- **Architecture reopen:** NONE
- **Database/Alembic change:** NONE
- **Provider/model/SDK selection:** NONE
- **Runtime implementation:** NONE

This document preserves the first destructive AI-05B review as evidence rather than rewriting the initial candidate into an apparent first-pass success.

The review is structural/repository-grounded. It does **not** claim executable provider/runtime tests were run. It attacks whether the candidate is concrete enough to build safely against the current branch and accepted DANTE authorities.

The candidate remains the original materialization. This document is the bounded hardening layer that must be applied when reading it for the fresh retest.

---

# 1. First destructive pass objective

Attack the candidate from five directions simultaneously:

```text
CURRENT REPOSITORY TRUTH
+ CURRENT POSTGRESQL/DICTIONARY TRUTH
+ PRODUCT GLOBAL-SEARCH REQUIREMENT
+ AI-03 RETRIEVAL/PERMISSION GUARANTEES
+ AI-04/AI-05A PRODUCTION/BUILD INVARIANTS
```

The pass asks not merely whether a concept is present, but whether an implementation team could build it without being forced to invent a dangerous missing rule.

Primary evidence inspected includes:

```text
docs/product/v1-global-search-and-command.md
docs/database/dictionary/README.md
docs/database/dictionary/tables/**
docs/database/dictionary/views/**
docs/architecture/dante-ai-03b-retrieval-memory-architecture.md
docs/architecture/dante-ai-04b-concrete-runtime-capability-architecture.md
docs/architecture/dante-ai-04c-production-assurance-control-plane-operations.md
docs/architecture/dante-ai-05a-whole-system-build-boundary-acceptance.md
apps/backend/pyproject.toml
apps/backend/src/dante/bootstrap/**
apps/backend/src/dante/platform/database/**
.github/workflows/backend-ci.yml
```

---

# 2. Result summary

The candidate survives the major architecture boundaries but fails seven implementation-grade details.

```text
AI05B-H01  Search eligibility must be query-time/pushdown enforceable
AI05B-H02  Global Search requires an explicit bounded family registry + materialization gate
AI05B-H03  Provider attempt cancellation/cleanup must be buildable without durable Run fiction
AI05B-H04  Route configuration needs material identity + runtime-delivery proof
AI05B-H05  Resource settlement must represent unknown/late provider usage truthfully
AI05B-H06  Search read transaction ownership must be concrete without leaking SQLAlchemy
AI05B-H07  Every first-vertical runtime/evidence object needs explicit lifecycle coverage
```

None requires:

```text
new Domain root
new Logical owner
Physical/PostgreSQL reopen
new PostgreSQL table/index
Alembic migration
provider selection
AI framework
vector/search database
conversation/Run persistence
```

---

# 3. First pass case disposition

| Case | First pass | Reason |
|---|---|---|
| B05-01 repo path truth | PASS | candidate was built from live branch paths |
| B05-02 Search/Intelligence dependency direction | PASS | private adapter/SQLAlchemy/provider imports remain excluded from Intelligence public/application surface |
| B05-03 deterministic Search without provider | PASS | provider dependency is not required by Search |
| B05-04 hidden-result non-interference | **FAIL BOUNDED** | access context exists conceptually, but exact query-time eligibility/pushdown contract is insufficiently frozen |
| B05-05 current/history semantics | PASS | explicit and inherited from AI-03/DB |
| B05-06 miss != nonexistence | PASS | explicit |
| B05-07 bounded query adapter | **FAIL BOUNDED** | methods are bounded, but the candidate does not yet freeze how concrete searchable families are admitted against the actual materialized DB |
| B05-08 no raw DB authority to model | PASS | dependency rule explicit |
| B05-09 Context != Retrieval / unresolved != unbounded | PASS | explicit |
| B05-10 ContextManifest != BasisManifest | PASS | explicit |
| B05-11 stale-basis fixture | PASS CONTRACT | fixture requirement is concrete; executable proof remains implementation work |
| B05-12 policy revalidation | PASS CONTRACT | required boundaries present; Search pushdown still needs H01 |
| B05-13 provider error translation | PASS CONTRACT | concrete taxonomy/doubles present |
| B05-14 disconnect/cancellation race | **FAIL BOUNDED** | public port names cancellation but attempt identity/cleanup lifetime are not concrete enough |
| B05-15 ambiguous provider submit | PASS WITH H03/H05 | no blind retry is explicit; cleanup/settlement truth needs hardening |
| B05-16 immutable route snapshot | **FAIL BOUNDED** | logical revision exists, material byte identity and delivery proof are missing |
| B05-17 emergency deny | PASS CONTRACT | explicit activation requirement |
| B05-18 provider SDK confinement | PASS | explicit import boundary |
| B05-19 resource ownership | **FAIL BOUNDED** | estimate/admit/settle exists but unknown/late provider usage is not represented strongly enough |
| B05-20 first vertical NO_EFFECT | PASS | explicit |
| B05-21 no PG transaction across provider call | PASS | explicit, but Search read-scope ownership needs H06 |
| B05-22 provider outage degrades Ask only | PASS | explicit separation |
| B05-23 no new generic AI persistence | PASS | DB/Alembic none |
| B05-24 Auth/AuthZ missing => gated | PASS CONTRACT | no bypass; production HTTP remains gated |
| B05-25 no unverified external delta | PASS | non-streaming first public Ask surface |
| B05-26 observability N/A vs missing | PASS CONTRACT | explicit |
| B05-27 evidence planes distinct | PASS | explicit |
| B05-28 BD-41 material composition | **FAIL BOUNDED WITH B05-16** | qualification artifact is good, but config material identity must be cryptographically stable |
| B05-29 premature capability activation | PASS | explicit gates |
| B05-30 architecture imports / eval tooling | PASS CONTRACT | explicit architecture tests |
| B05-31 lifecycle completeness | **FAIL BOUNDED** | matrix covers major objects but not every first-vertical DTO/decision object individually |
| B05-32 reverse consistency | HOLD | cannot be called PASS until bounded hardening is retested from zero |

Additional first-pass cases added because the candidate exposed implementation-specific failure surfaces:

```text
B05-33 current DB materialization vs useful Global Search
→ FAIL BOUNDED / H02

B05-34 route config source file vs deployable immutable artifact
→ FAIL BOUNDED / H04

B05-35 client disconnect + unconfirmed provider cancellation + no durable Run
→ FAIL BOUNDED / H03

B05-36 ambiguous provider attempt + late/unknown usage settlement
→ FAIL BOUNDED / H05

B05-37 Search transaction ownership without AsyncSession leakage
→ FAIL BOUNDED / H06
```

---

# 4. AI05B-H01 — SearchEligibilityEnvelope + query-time non-interference

## 4.1 Failure

The candidate says Search receives a resolved access context and that hidden results must not influence hits/counts/facets/rank. That is necessary but not sufficient for buildability.

AI-03B already rejects the unsafe pattern:

```text
search all private data
→ top-K/rank/count
→ permission filter at the end
```

because hidden rows may influence:

```text
rank
count
facet values
pagination
candidate exhaustion
timing
source existence
```

The current PostgreSQL database is not an automatic row-level policy engine for product semantics. Runtime SELECT availability does not itself prove current Authority/AuthZ/Consent/Visibility eligibility.

Therefore a generic `access_context` field leaves too much implementation freedom.

## 4.2 Hardening

Freeze an immutable request-scoped Search eligibility object:

```text
SearchEligibilityEnvelope
```

Minimum semantics:

```text
principal / represented-party binding
purpose
recipient
surface
Authority/AuthZ/Visibility/Consent basis identities as applicable
current-vs-history eligibility
permitted SearchFamilyIds
family-specific owner/source scope
permitted projection fields
snippet eligibility
facet/count eligibility
sensitivity/disclosure ceiling
source lifecycle exclusions
explicit negative/excluded scopes
revalidation condition
```

Binding rules:

```text
SEARCH ELIGIBILITY ENVELOPE
!= CANONICAL AUTHORITY OWNER

SEARCH ELIGIBILITY ENVELOPE
= request-scoped projection of current authoritative decisions
```

The Search application never invents this authority. It consumes it from the accepted application Auth/AuthZ/Authority/Visibility seam.

## 4.3 Pushdown requirement

For a protected/private family:

```text
ELIGIBILITY MUST CONSTRAIN THE ELIGIBLE UNIVERSE
BEFORE OBSERVABLE RANK/COUNT/FACET/PAGINATION SEMANTICS.
```

A PostgreSQL family query must therefore prove that ineligible rows cannot affect externally observable Search behavior.

Allowed physical techniques may differ by family:

```text
SQL predicate / join pushdown
pre-resolved bounded eligible refs
permission-safe source-local projection
separate permission-safe query family
another directly proven non-interfering mechanism
```

Rejected as a general proof:

```text
query everything
→ rank/top-K/count/facet
→ Python post-filter
```

Post-filtering remains allowed as defense-in-depth or for fields already inside an eligible candidate universe; it is not the sole permission proof for protected discovery.

## 4.4 Auth dependency

The current AI branch does not own the real integrated full-stack Access/Auth vertical.

Therefore:

```text
production Search/Ask HTTP activation
REQUIRES
an authoritative public seam capable of producing the current SearchEligibilityEnvelope.
```

Tests may use explicit synthetic envelopes. No temporary production user header, hard-coded principal or Intelligence-owned authorization database is permitted.

---

# 5. AI05B-H02 — SearchFamilyRegistry + materialization/readiness gate

## 5.1 Failure

Product authority requires one Global Search/Question/Navigation/Command surface across major authorised DANTE data over time.

That product requirement does **not** mean:

```text
GLOBAL SEARCH = GENERIC SQL OVER EVERY DATABASE TABLE
```

The current PostgreSQL materialization proves why this distinction matters.

Current native owner tables such as `person` and `content_artifact` are deliberately stable identity shells. Their materialized columns are stable UUIDv7 NativeRefs; they do not yet contain a generic name/title/body payload merely to make search convenient.

The five current database views are current-state projections for:

```text
schedule placement
actual realization
session timing
routine recurrence
event recurrence
```

They are not a generic product Search index.

Therefore the candidate cannot honestly claim that the current 69-table schema is already a useful keyword Global Search universe.

## 5.2 Hardening

Introduce a DANTE-owned static/application concept:

```text
SearchFamilyId
SearchFamilyRegistration
SearchFamilyRegistry
```

These are Search application configuration/contracts, not Domain identities and not database tables.

Each registration freezes at least:

```text
family_id
owning product/capability boundary
canonical/source semantics
supported public query modes
current/history/source-reread support
maximum truthful guarantee
safe result projection schema
SearchEligibilityEnvelope projection requirements
concrete bounded query implementation identity
source/material-basis/currentness mapping
activation evidence reference
```

Binding:

```text
SEARCH FAMILY ID != TABLE NAME
SEARCH REGISTRY != DATABASE CATALOG INTROSPECTION
SEARCH REGISTRY != GENERIC REPOSITORY
```

The registry is explicit code/config reviewed with the capability it exposes. It is never auto-populated by iterating SQLAlchemy metadata or the 69 Dictionary tables.

## 5.3 Concrete PostgreSQL adapter rule

The private Search PostgreSQL adapter remains one bounded Search infrastructure boundary, but concrete family implementations are hand-written/reviewed.

Conceptually:

```text
PostgresSearchQueryAdapter
    ├ exact/reference navigation query
    ├ <activated family A> current query
    ├ <activated family A> history/source query
    ├ <activated family B> current query
    └ ... only as families are deliberately registered
```

No arbitrary family/table name reaches SQL generation.

No generic:

```text
search_table(table_name, columns, filter)
search_model(model_type, ...)
Repository[T]
model-generated ORM/SQL predicate
```

is permitted.

## 5.4 Build vs product activation

Keep distinct:

```text
SEARCH ENGINE BOUNDARY BUILDABLE
!=
GLOBAL SEARCH PRODUCT SURFACE USEFULLY ACTIVATABLE
```

The Search boundary/contracts/application shell may be implemented before all product families exist.

A family becomes active only when:

```text
accepted product/capability data exists
+ canonical/source semantics are materialized
+ permission-safe eligible universe is provable
+ current/history/source semantics are known
+ bounded query implementation exists
+ tests prove its guarantee
```

The current DB must **not** be expanded with generic title/text/search columns merely to satisfy AI-05B ordering.

If no useful discovery family is materialized at implementation time, the public Global Search product route remains activation-gated. Exact reference/navigation mechanics may still be tested internally but do not masquerade as full Global Search product readiness.

## 5.5 Product completeness remains intact

`docs/product/v1-global-search-and-command.md` remains authoritative for eventual cross-cutting product scope.

Family-by-family activation is an implementation safety mechanism, not a reduction of the Product requirement that major supported domain objects become discoverable through the shared capability.

The first AI vertical remains read-only Search + Ask. Product command/effect behavior remains later and must pass Effect/Policy/approval semantics rather than being silently deleted from the broader product contract.

---

# 6. AI05B-H03 — ProviderAttempt identity, cancellation and bounded cleanup

## 6.1 Failure

The candidate's public `ModelAccessPort.cancel(ProviderAttemptId)` is insufficiently concrete for an in-flight call if the caller only learns the attempt identity after completion, and it leaves unclear who owns late provider evidence after a client disconnect.

AI-04B requires:

```text
client disconnect
!= stream stop
!= ProviderAttempt cancel request
!= ModelInvocation cancel
!= Run cancel

CANCELLATION REQUESTED
!= CANCELLATION CONFIRMED
!= EXECUTION QUIESCED
```

A request-owned Run does not permit the implementation to discard an unconfirmed provider attempt merely because the HTTP socket disappeared.

## 6.2 Hardening — DANTE attempt identity before dispatch

A DANTE technical `ProviderAttemptId` is allocated **before outbound dispatch**.

```text
ProviderAttemptId
= DANTE-owned technical correlation identity for one concrete attempt
!= provider response/call/event ID
!= semantic effect idempotency identity
```

The selected private provider adapter receives an attempt request already carrying this DANTE identity.

## 6.3 Hardening — cancellation signal

First-vertical application port shape becomes conceptually:

```text
ModelAccessPort.invoke(
    ModelInvocationRequest,
    CancellationSignal,
) -> ModelInvocationResult

ModelAccessPort.stream(
    ModelInvocationRequest,
    CancellationSignal,
) -> AsyncIterator[ModelEvent]
```

The `ModelAccessRuntime` resolves one concrete `ProviderAttempt`, allocates its DANTE attempt identity, invokes the selected private provider adapter and supervises timeout/retry/fallback/cancellation.

The private adapter contract supports provider cancellation mechanics against its active attempt/handle where the selected protocol permits it.

An application caller does not manage raw provider SDK handles.

## 6.4 RequestExecutionScope

Materialize a request-local technical owner:

```text
RequestExecutionScope
```

It owns only bounded technical execution lifetime:

```text
deadline
attached tasks
CancellationSignal
active DANTE ProviderAttemptIds
publication-open/closed state
bounded cleanup state
```

It is **not** a Domain object and is not persisted in the first vertical.

Client disconnect semantics:

```text
client disconnect
→ stop/close recipient publication
→ stop optional future work
→ request provider cancellation when current execution policy says safe/appropriate
→ continue bounded in-process cleanup/correlation until
   provider outcome/cancellation confirmation OR execution deadline
```

This bounded cleanup may outlive the socket but not the backend process.

## 6.5 Durability activation boundary

If a future activated provider feature/background mode, commercial accounting rule, audit obligation or consequential operation requires outcome reconciliation to survive process crash, request-local cleanup is insufficient.

That is an independent durability trigger:

```text
must survive process crash
→ durable technical owner required
→ justify Class-A/Class-B/idempotency/reconciliation state
```

The first read-only inline provider mode must keep provider-background execution disabled and may activate only while no such durable requirement exists.

---

# 7. AI05B-H04 — RouteConfigIdentity + deployment delivery proof

## 7.1 Failure

A logical `revision` string is not enough to prove immutable configuration.

Unsafe possibility:

```text
revision = R1
bytes = A
→ qualified

same revision = R1
bytes = B
→ deployed
```

AI-04C explicitly requires:

```text
ACTIVE POINTER != IMMUTABLE CONFIG REVISION
```

Additionally, the current backend build configuration proves a Python package build but does not yet define a production delivery mechanism for `apps/backend/config/intelligence/**`.

AI-05B must not assume that a repo file automatically appears in the deployed runtime artifact.

## 7.2 Hardening — material identity

Freeze:

```text
RouteConfigIdentity
=
logical revision
+ SHA-256 of canonical serialized configuration bytes
```

Conceptual display form:

```text
<revision>@sha256:<digest>
```

Every coherent `RouteConfigSnapshot` records the full material identity, not only the logical revision.

Qualification evidence and production runtime evidence bind to the same identity.

```text
SAME REVISION LABEL + DIFFERENT DIGEST
= DIFFERENT MATERIAL COMPOSITION
= REQUALIFICATION REQUIRED
```

## 7.3 Canonical serialization

The config schema must define deterministic/canonical serialization for hashing. Equivalent in-memory objects are not allowed to produce ambiguous material identities.

The implementation may hash the exact validated canonical JSON representation according to one frozen serializer/version.

The serializer/schema version belongs in the config/evidence identity.

## 7.4 Active selector

Deployment selection is allowed to point only to a full approved material identity, conceptually:

```text
DANTE_INTELLIGENCE_ACTIVE_CONFIG
= <revision>@sha256:<digest>
```

or an equivalent typed deployment selector carrying both values.

Secrets remain separate.

## 7.5 Runtime-delivery proof

Repository source may remain:

```text
apps/backend/config/intelligence/revisions/<revision>.json
```

but production activation is blocked until the implementation/deployment workstream proves how the exact bytes are delivered to runtime.

Required build/deployment evidence:

```text
source config identity
→ build/release artifact
→ runtime-visible config bytes
→ same canonical SHA-256
```

Possible future packaging/mounting mechanisms remain open until the actual backend deployment artifact is selected. AI-05B does not invent a Docker/package-data mechanism that the repository does not yet own.

## 7.6 BD-41 consequence

Qualification artifact must record:

```text
RouteConfigIdentity
HarnessProfile identity
ProviderBinding identity
feature mode
control/security identities
retry/fallback composition
```

Production promotion requires the material identities to match qualified evidence or each delta to carry independent qualification evidence.

---

# 8. AI05B-H05 — ResourceSettlement truth under unknown/late usage

## 8.1 Failure

`estimate → admit → settle` is structurally correct but incomplete for:

```text
provider accepted request
→ network response lost / cancellation unconfirmed
→ usage may exist
→ provider usage evidence absent or arrives later
```

Treating missing usage as zero or automatically releasing a shared/commercial reservation would create false accounting truth.

## 8.2 Hardening

Freeze resource settlement status classes at minimum:

```text
SETTLED_ACTUAL
SETTLED_ESTIMATED
NO_USAGE_PROVEN
PENDING_RECONCILIATION
UNKNOWN_USAGE
RELEASED
```

Binding:

```text
NO USAGE EVIDENCE
!= NO USAGE
```

For an indeterminate provider attempt:

```text
attempt outcome unknown
→ no blind request replay
→ usage/cost state may remain UNKNOWN/PENDING
→ reservation must not be falsely settled/released where shared/commercial accounting is authoritative
```

## 8.3 First-vertical no-ledger envelope

The first technical slice may use request-local estimates/limits when no shared/monthly/commercial quota authority is active.

In that envelope, an unresolved provider usage outcome may be emitted as operational evidence `UNKNOWN_USAGE`; it is not a canonical commercial balance.

Production activation under a real shared/commercial quota requires a durable accounting/reconciliation owner able to survive request/process failure.

That future trigger may legitimately require persistence. It does not justify adding a generic AI usage table now.

---

# 9. AI05B-H06 — SearchReadScopeFactory transaction ownership

## 9.1 Failure

The candidate correctly forbids exposing `AsyncSession` to Intelligence and correctly forbids a DB transaction spanning a provider call, but `SearchReadScope` is only conceptual.

CP3 already binds:

```text
outer application operation owns transaction lifetime
adapter may use persistence mechanics
no generic UnitOfWork / Repository[T]
```

The implementation needs one exact seam that satisfies both requirements.

## 9.2 Hardening

Freeze a Search-specific port:

```text
SearchReadScopeFactory.open(SearchEligibilityEnvelope)
    -> async SearchReadScope
```

On enter, the private PostgreSQL implementation:

```text
creates an AsyncSession from existing DatabaseRuntime.session_factory
begins one explicit read transaction
binds only SearchQueryPort operations for that scope
```

The Search application owns scope lifetime by entering/exiting the Search-specific context.

It never receives the raw `AsyncSession`.

Conceptual flow:

```text
SearchApplication
→ async with SearchReadScopeFactory.open(eligibility) as search_queries
    → bounded current/history/navigation/source reads
→ scope exits
→ result materialized
```

For Ask:

```text
Search read scope OPEN
→ retrieve/materialize permitted result/context basis
→ Search read scope CLOSED
→ provider call may begin
```

Never:

```text
DB TRANSACTION OPEN
→ external provider network call
→ DB TRANSACTION CLOSE
```

## 9.3 Scope is not generic UoW

`SearchReadScopeFactory` is allowed because it is capability-specific and exposes only Search query operations.

Rejected:

```text
UnitOfWork.repositories
Repository[T]
get_session()
raw session pass-through
arbitrary commit/rollback API to Intelligence
```

Search has no business mutation commit authority.

---

# 10. AI05B-H07 — exhaustive first-vertical lifecycle registry

## 10.1 Failure

The initial lifecycle matrix covered the major objects but did not enumerate every first-vertical abstract DTO/decision/evidence object. That leaves implementation ambiguity around reuse/cache/retry/cancel semantics.

AI-05B requires every materialized abstract object to have a lifecycle.

## 10.2 Binding rule

No new first-vertical contract type is accepted unless it is classified under:

```text
CREATE
PERSIST
MUTATE / VERSION
DELETE / EXPIRE
CACHE
RETRY
CANCEL
```

If a field is not applicable, it must say `N/A`, not remain unspecified.

## 10.3 Exhaustive lifecycle groups

### Execution

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `WorkContract` | intake | NO | immutable; derive/supersede | execution scope end | NO | reuse only if protected meaning unchanged | supersession/cancel affects work, object stays immutable |
| `RunId` / run status | execution start | NO first vertical | runtime transition only | cleanup end | NO | new Run/attempt per semantic retry policy | explicit runtime state |
| `RequestExecutionScope` | HTTP/application start | NO | attached-task/cleanup state | quiescence/deadline | NO | N/A | owns request-local cancellation signal |
| `CancellationSignal` | scope creation | NO | one-way not-requested→requested | scope end | NO | N/A | is cancellation coordination object |
| `ExecutionDeadline` | intake/resolution | NO | immutable | scope end | NO | inherited unless new WorkContract | deadline expiry requests stop |

### Search

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `SearchEligibilityEnvelope` | authoritative access projection | NO | immutable; re-resolve on material basis change | request end | NO | re-resolve, never widen silently | N/A |
| `SearchFamilyRegistration` | code/config review | Git/code only | new code/revision | removed/disabled by release | immutable process registry allowed | N/A | N/A |
| `SearchRequest` / family query | request/planning | NO | immutable | request end | NO first slice | rebuild only under same semantics | DB task cancel where possible |
| `SearchHit` | bounded query result | NO | immutable | request end | NO first slice | re-read creates new hit/result | N/A |
| `SearchPage` | bounded query result | NO | immutable | request end | NO first slice | new query/page request | attached DB read cancel |
| navigation/source result | bounded read | NO | immutable | request end | NO first slice | reread if currentness demands | attached DB read cancel |
| `SearchReadScope` | application enters scope | NO | transaction state only | context exit | NO | open new scope, never reuse failed session | cancel/rollback read scope |

### Context / Retrieval

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `ContextPlan` | Ask planning | NO | new plan version on material replan | request end | NO | bounded rebuild | discard outstanding acquisition |
| `InformationNeed` | ContextPlan | NO | explicit refined/new need, not hidden mutation | request end | NO | unresolved may trigger bounded alternative | stop associated acquisition |
| `RetrievalPlan` | need planning | NO | explicit strategy replacement | request end | NO | bounded strategy retry | cancel attached retrieval |
| `ContextFragment` | eligible validated candidate | NO | immutable; replacement is new fragment | request end | NO first slice | source reread creates new fragment | N/A |
| `ContextReadiness` | readiness evaluation | NO | recompute to new result | request end | NO | re-evaluate after bounded retrieval | N/A |
| `ConsumerContext` | delivery projection | NO | rebuild after policy/basis change | invocation/request end | NO first slice | new projection on allowed retry/failover | stop future egress |
| `ContextManifest` | after assembly/exposure | NO first vertical | immutable new manifest per changed exposure | request end | NO | new manifest on changed attempt | N/A |
| `BasisManifest` | after source/basis resolution | NO first vertical | immutable new manifest after revalidation/reread | request end | NO | stale→reread/rebuild | N/A |
| `BasisDependency` | manifest creation | NO | immutable | request end | NO | re-resolve creates new dependency evidence | N/A |

### Policy / Routing / Provider

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `PolicyDecision` | material PEP boundary | NO ordinary first slice | immutable; new decision on revalidation | request end | cached allow forbidden across invalidating change | reevaluate only | N/A |
| route config source revision | reviewed config | Git/release artifact | immutable new revision | retention per release | process load cache by full identity | N/A | emergency deny blocks use |
| `RouteConfigIdentity` | canonical serialization/hash | qualification/release evidence | immutable | retained with evidence | yes by immutable identity | N/A | N/A |
| `RouteConfigSnapshot` | pre-invocation resolution | NO | immutable for invocation | request/attempt end | request/process cache by exact identity allowed | retry uses same snapshot unless policy explicitly re-routes; material change is new composition | emergency deny/current policy may stop new dispatch |
| `ModelInvocationRequest` | ModelAccess runtime | NO | immutable | attempt/invocation end | NO | logical retry creates new ProviderAttempt; request meaning remains bounded | observes CancellationSignal |
| `ProviderAttempt` | before external dispatch | NO canonical persistence | immutable identity/outcome transitions | bounded cleanup end | NO | retry/failover creates NEW attempt ID | request_cancel != confirmed/quiesced |
| `ModelEvent` | provider normalization | NO first vertical | immutable event | cleanup end | bounded buffer only | replay/dedup by transport evidence where safe | publication stop independent |
| `ModelInvocationResult` | invocation completion/normalization | NO | immutable | request end | NO | new result only from governed attempt | N/A |

### Resource / Effect / Publication

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| `ResourceEstimate` | pre-admission | NO | immutable | request end | NO | recompute if route materially changes | N/A |
| `ResourceAdmission` | admission boundary | NO first envelope | immutable decision | request end | NO | new admission on material route/resource change | release reservation if one exists |
| `ResourceSettlement` | after/while outcome resolves | NO when request-local only | explicit status progression if owner supports it | cleanup end or durable owner lifecycle | NO | reconciliation, not blind replay | N/A |
| `EffectIntent` | only if work proposes effect | NO in first vertical | immutable | request end | NO | N/A first vertical | first vertical rejects/nonactivates |
| `EffectOutcome` | Effect boundary | NO first vertical | immutable outcome | request end | NO | governed later per effect semantics | cancellation != undo |
| `PublicationResult` | Safe Publication | NO | immutable | response/evidence end | NO | only recipient-safe retry semantics | disconnect closes publication |

### Evidence

| Object | Create | Persist | Mutate/version | Delete/expire | Cache | Retry | Cancel |
|---|---|---|---|---|---|---|---|
| telemetry event/span/metric | material runtime boundary | observability backend only | append/aggregate per telemetry system | ops retention | exporter buffers bounded | exporter retry bounded, never blocks safety indefinitely unless mandatory evidence class | drop/backpressure rules explicit |
| qualification artifact | qualification run | CI/release evidence store | immutable; new run=new artifact | evidence retention | N/A | rerun creates new artifact | N/A |
| provider conformance evidence | conformance run | CI/release evidence store as required | immutable | evidence retention | N/A | new test run | N/A |

## 10.4 Future-object rule

Any first implementation PR that adds a new material contract object not covered by these groups must either:

```text
map it explicitly to an existing lifecycle class
OR
extend the lifecycle authority in the same reviewed change.
```

A DTO name is not allowed to hide persistence/cache/retry semantics.

---

# 11. Search buildability after H01/H02/H06

The corrected first Search architecture is:

```text
HTTP / Intelligence consumer
        ↓
authoritative current access seam
        ↓
SearchEligibilityEnvelope
        ↓
SearchApplication
        ↓
SearchFamilyRegistry
        ↓
selected ACTIVE registered families only
        ↓
SearchReadScopeFactory
        ↓
private bounded PostgresSearchQueryAdapter
        ↓
permission-safe eligible universe pushdown
        ↓
current/history/source/navigation reads
        ↓
materialized safe Search results
        ↓
read transaction CLOSED
```

Only then may Intelligence use the result as retrieval input.

This keeps:

```text
Global Search product capability
!= one SQL statement
!= one generic table
!= one provider
!= one vector index
```

---

# 12. Ask cleanup after H03/H05

Corrected read-only Ask failure path:

```text
ModelInvocation
→ DANTE ProviderAttemptId allocated
→ resource admission
→ provider dispatch
→ client disconnect
→ publication closes
→ provider cancellation requested where appropriate
→ cancellation not yet confirmed
→ bounded RequestExecutionScope cleanup continues
→ provider result / cancellation confirmation / deadline
→ usage settles as actual/estimated/unknown according to evidence
→ NO blind duplicate provider replay
→ NO durable Run invented
```

If accepted product/commercial/audit semantics require surviving a process crash at any point in that path, the no-store envelope is no longer sufficient and activation stops until the independent durability trigger is designed.

---

# 13. Route/config buildability after H04

Corrected route identity path:

```text
repo source JSON
→ schema validation
→ canonical serialization
→ SHA-256
→ RouteConfigIdentity(revision,digest)
→ qualification artifact binds identity
→ build/release delivery preserves exact bytes
→ runtime resolves active full identity
→ coherent RouteConfigSnapshot
→ provider attempt
```

A deployment that cannot prove the source-to-runtime identity chain is not production-eligible.

---

# 14. Updated implementation dependency constraint

The candidate B0..B11 graph is retained with these stronger prerequisites:

```text
B0 architecture tests

B1 Search contracts/application
   + SearchFamilyRegistry
   + SearchEligibilityEnvelope

B2 first real searchable family readiness
   + SearchReadScopeFactory
   + bounded PG query
   + real PG proof

B3 Search public/inbound surface
   production registration gated by authoritative Auth/AuthZ seam
   and at least one useful activated Search family

B4 Intelligence contracts + ModelAccess fake
   + RequestExecutionScope/CancellationSignal

B5 config/resource/evidence seams
   + RouteConfigIdentity digest
   + UNKNOWN/PENDING resource settlement semantics

B6 provider/model/SDK decision evidence

B7 selected provider adapter
   + DANTE ProviderAttemptId-before-dispatch
   + cancellation/conformance proof

B8 direct eval / qualification
   + exact RouteConfigIdentity
   + same production-owned material composition

B9 read-only Ask

B10 production hardening

B11 activation/system evidence
```

If B2 has no useful materialized product Search family yet, B3 product activation waits. This does not authorize a database shortcut.

---

# 15. Fresh retest battery

The next pass must start from zero against:

```text
AI-05B candidate
+ AI05B-H01..H07
+ current branch repository truth
```

Retest:

```text
B05-01..B05-37
+ B05-38 first-vertical explicit Effect nonactivation cannot be bypassed
+ B05-39 read-only first vertical does not shrink eventual Product Global Search/Command scope
+ compound collision suite
+ reverse AI-05B -> AI-05A -> AI-04 -> PRE-AI05 -> AI-03 -> AI-02
```

Fresh pass must particularly attack:

```text
hidden row affects rank/count despite post-filter
inactive family appears by DB introspection
empty current DB causes fake generic search schema addition
Auth seam unavailable but HTTP route accidentally activates
Search read transaction survives into provider call
client disconnect destroys unconfirmed provider evidence too early
provider cancel requested but provider later completes and bills
same config revision label ships changed bytes
config qualified from repo but absent/different in runtime artifact
unknown usage settles as zero
new DTO lacks lifecycle classification
provider SDK import leaks outside binding adapter
production eval uses materially different config/adapter from qualified path
```

No PASS is claimed by materializing these hardenings. The next step is the fresh destructive retest.

---

# 16. Explicit non-claims

```text
first AI-05B candidate materialized          YES
first destructive pass                      FAIL BOUNDED
AI05B-H01..H07 materialized                 YES
fresh retest                                NOT YET RUN
AI-05B accepted                             NO
whole AI-05 closed                          NO
runtime code implemented                    NO
Search product route activated              NO
useful Search family selected               NO / DEPENDS ON MATERIALIZED PRODUCT DATA
Auth/AuthZ integrated                       NO
provider/model/SDK selected                 NO
route config delivery mechanism selected    NO
new PostgreSQL/Alembic object               NO
```

---

# 17. Exact next action

```text
run a fresh independent B05-01..B05-39 pass
→ run compound collisions
→ if any new bounded failure: harden only that failure
→ rerun full suite from zero
→ reverse-check AI-05B to upstream authority
→ only then materialize AI-05B acceptance/closure
```

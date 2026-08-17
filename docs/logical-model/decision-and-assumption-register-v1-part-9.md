<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-8.md" -->
> **Canonical continuation of the Logical Model Decision and Assumption Register v1.** Earlier decisions and assumptions remain active unless explicitly superseded. This continuation records final Whole-Logical A+B+C+D+E+F decisions, hardenings, rejected alternatives and stage-deferred Physical Model obligations.

# Whole-Logical A+B+C+D+E+F — Decision Register

**Status:** CONTENT PASS — PENDING SEPARATE REMOTE-QA CLOSURE  
**Date:** 2026-08-17

## DEC-WL001 — Accept the integrated A+B+C+D+E+F Logical Model

**Decision:** retain the accumulated layered representation as the Whole-Logical architecture after 57/57 owner classification, full reverse mapping, clean-room reconstruction, fresh destructive/counterfactual testing and technology reconsideration.

**Why:** no Domain owner gap, semantic contradiction or structural blocker was found when the six slices were composed.

**Regression impact:** R3 WHOLE-LOGICAL.

**Status:** RETAIN + HARDEN with WL-H01..WL-H12.

## DEC-WL002 — Preserve the existing LR taxonomy; add contracts, not new universal roots

**Decision:** keep LR-01..LR-13 and the discriminated ReferenceAddress family. WL-H01..WL-H12 harden usage without introducing universal `Entity`, `Relationship`, `Rule`, `Fact`, `WorkItem`, `Terms`, `Projection` or `Command` semantic roots.

**Why:** all 57 current concepts are representable under accepted specific owners/roles/values/policies/relations/history/projections/specialist boundaries.

**Status:** RETAIN.

## DEC-WL003 — Agreement terms bind to a justified material owner/state

**Decision:** material Agreement assent references a justified `MaterialStateRef` of Proposal, Content Artifact, Agreement-owned terms state or another explicit valid owner/facet.

**Rejected:** generic `TermsRef` / universal Terms entity solely for implementation convenience.

**Trace:** INV-WL001 / WL-H01.

**Status:** RETAIN + HARDEN.

## DEC-WL004 — Introduce a logical Governed Operation / Effect Contract

**Decision:** consequential operations are classified by operation family, target semantic owner/facet, material target state where required, effect semantics, inputs/context, purpose, preconditions and governance requirements.

**Boundary:** logical contract vocabulary, not a new Domain `Command`/`Operation` owner.

**Rejected:** free-form action string or HTTP route as canonical Domain meaning.

**Trace:** INV-WL002 / WL-H02.

**Status:** RETAIN + HARDEN.

## DEC-WL005 — Introduce a Projection / Disclosure Surface Contract without ProjectionRef

**Decision:** derived/disclosed surfaces identify bounded source owner/set, projection/facet kind, derivation/profile, material version where required, purpose/context, permitted exposure and source-disclosure boundary.

**Rejected:** universal persistent `ProjectionRef` solely because a representation can be authorized/exposed.

**Trace:** INV-WL003 / WL-H03.

**Status:** RETAIN + HARDEN.

## DEC-WL006 — Unknown/absence semantics are owner-specific

**Decision:** missing representation does not universally mean false/no/inactive/declined/cancelled/non-realization. Explicit negative states are owned by the relevant semantic family; otherwise state remains unknown/unresolved.

**Trace:** INV-WL004 / WL-H04.

**Status:** RETAIN + HARDEN.

## DEC-WL007 — Consequential writes require expected-state semantics

**Decision:** a consequential mutation carries expected `MaterialStateRef` or semantically equivalent precondition when stale-write conflict can materially corrupt meaning.

**Boundary:** ETag/MVCC/provider revision tokens may implement concurrency checks but are not semantically identical to `MaterialStateRef`.

**Trace:** INV-WL005 / WL-H05.

**Status:** RETAIN + HARDEN.

## DEC-WL008 — Idempotency remains transport/effect control, not identity

**Decision:** retries may use bounded idempotency semantics so one intended operation does not produce duplicate effect; reuse with materially different operation must conflict/reject.

**Rejected:** idempotency key becomes NativeRef, Goal ID, Request ID, Decision ID or universal Command identity.

**Trace:** INV-WL006 / WL-H06.

**Status:** RETAIN + HARDEN.

## DEC-WL009 — Multi-owner consistency must be explicit and truthful

**Decision:** where invariants require all-or-nothing changes, later Physical/runtime design must supply an atomic consistency boundary. Where distributed/provider atomicity is impossible, canonical state must expose staged/partial outcome and reconciliation/compensation explicitly.

**Rejected:** hidden partial success represented as complete canonical success.

**Trace:** INV-WL007 / WL-H07.

**Status:** RETAIN + HARDEN.

## DEC-WL010 — Canonical LifeOS state stays separate from provider sync state

**Decision:** LR-09/provider representation, provider revision, apply/sync status and reconciliation remain independent from accepted LifeOS canonical state.

**Rejected:** provider success/failure/current value automatically dictates canonical truth.

**Trace:** INV-WL008 / WL-H08.

**Status:** RETAIN + HARDEN.

## DEC-WL011 — Consequential LR-08 use requires freshness/material-basis semantics

**Decision:** when a canonical effect relies on Candidate Set, Effective Availability/Capacity/Authority/Visibility, knowledge or another derived projection, the effect must revalidate, bind to material derivation basis, or use an appropriate bounded consequential snapshot.

**Rejected:** stale cache/projection directly becomes canonical truth.

**Trace:** INV-WL009 / WL-H09.

**Status:** RETAIN + HARDEN.

## DEC-WL012 — Retention/redaction must not falsify history or reuse identity

**Decision:** where retention policy permits, preserve minimum tombstone/reference/provenance continuity required to distinguish `redacted/unavailable` from `never existed`; NativeRef is never reassigned to another referent.

**Trace:** INV-WL010 / WL-H10.

**Status:** RETAIN + HARDEN.

## DEC-WL013 — Consequential AuthZ decisions need reconstructible provenance

**Decision:** where consequence/audit requires, retain or reconstruct links among actual Actor, represented party, Principal/security context, applicable Authority/Consent/Visibility/material states, technical policy/model version or decision basis and resulting effect.

**Boundary:** AuthZ decision remains technical enforcement evidence; it does not become Authority/Consent/Actor by identity.

**Trace:** INV-WL011 / WL-H11.

**Status:** RETAIN + HARDEN.

## DEC-WL014 — Selective disclosure includes inference/non-interference pressure

**Decision:** all recipient-observable output—data, relation existence, counts, ranking, candidate lists, explanations, errors, timing-relevant behavior and aggregates—must respect the applicable disclosure surface.

**Trace:** INV-WL012 / WL-H12.

**Status:** RETAIN + HARDEN.

## DEC-WL015 — PostgreSQL hybrid remains current Physical Model baseline, not a Logical ontology

**Decision:** retain PostgreSQL hybrid as current preferred baseline entering Physical Model competition.

**Why:** Whole pressure needs mature relational integrity, transactional/concurrency tools, temporal/range capability, query/reporting ergonomics and bounded flexible/provider payload support.

**Boundary:** no schema/table/index/key choice is authorized here.

**Status:** RETAIN + HARDEN / PHYSICAL BENCHMARK REQUIRED.

## DEC-WL016 — TypeDB becomes a mandatory Physical Model benchmark challenger

**Decision:** TypeDB must be included as a serious challenger because native entities/relations/roles/cardinalities are structurally attractive for several n-ary/typed relationship families.

**Why not selected now:** Whole-system superiority over PostgreSQL hybrid is not yet proven across history, concurrency, reporting, provider integration, telemetry and operability.

**Status:** MANDATORY PHYSICAL BENCHMARK CHALLENGER.

## DEC-WL017 — Neo4j remains a serious secondary candidate

**Decision:** do not select Neo4j as canonical primary source at Logical stage, but retain it for Physical benchmark/projection/traversal pressure.

**Reason:** several LifeOS semantics are n-ary/material-state/common-ground structures rather than only source-target edges.

**Status:** PHYSICAL CANDIDATE / NOT SELECTED AS PRIMARY.

## DEC-WL018 — Universal event sourcing is rejected as primary ontology

**Decision:** append-only streams/projections may be bounded history/integration mechanisms later, but canonical LifeOS meaning remains owner-specific and cannot be replaced by `event type + payload` as semantic ontology.

**Status:** REJECT AS PRIMARY ONTOLOGY / RETAIN AS BOUNDED MECHANISM.

## DEC-WL019 — Document storage remains bounded; generic EAV/meta-model remains rejected

**Decision:** document/JSON representation is valid for provider payloads, specialist documents and genuinely flexible extension metadata. It is not a canonical escape hatch for required owner/relation/material-state semantics.

**Generic EAV/generic edge/meta-model:** HARD REJECT for canonical kernel.

**Status:** RETAIN BOUNDED DOCUMENT USE; REJECT GENERIC META-MODEL.

## DEC-WL020 — WD-03 and WD-05 are ready for conditional final discharge

**Decision:** Whole read-only evidence plus this canonical content package is sufficient to discharge the two Domain carry-forward obligations after exact remote Whole QA.

Current state:

```text
WD-03 CLEARANCE READY
WD-05 CLEARANCE READY
```

Activation condition:

```text
approved 9-file Whole content scope verified remotely
+ payload readback 9/9
+ main unchanged
+ separate whole-logical-v1-remote-qa.md closure record
```

Only then:

```text
WD-03 PASS
WD-05 PASS
LOGICAL MODEL CLOSED
PHYSICAL MODEL READY FOR SEPARATE AUTHORIZATION
```

# Whole-Logical Assumption Register

## ASM-WL001 — Physical expected-state enforcement is feasible

**Statement:** one or more later mechanisms can enforce bounded expected-state conflict detection without redefining MaterialStateRef as a storage token.

**Stability:** EVOLVING physically.

**If false:** Physical Model is blocked until an equivalent conflict-safe mechanism is found.

## ASM-WL002 — Multi-owner atomic/staged consistency can be implemented truthfully

**Statement:** operations whose invariants span owners can use transaction/atomic boundary where co-located, or explicit staged/reconciliation state when distributed/provider systems prevent global atomicity.

**Stability:** EVOLVING physically.

**If false:** affected Physical design is rejected.

## ASM-WL003 — Selective disclosure can be enforced without canonical per-recipient duplication

**Statement:** shared canonical reality plus bounded projection/relation/source policy remains technically enforceable.

**Stability:** STABLE logical intent; EVOLVING physical enforcement.

**If false:** Physical Model must improve policy/index/projection design; semantic duplication per recipient remains disallowed unless distinct referents truly exist.

## ASM-WL004 — Bounded tombstone/reference continuity can coexist with retention policy

**Statement:** applicable retention/privacy rules can preserve enough non-sensitive continuity to maintain truthful historical reference where permitted.

**Stability:** POLICY-DEPENDENT.

**If false for a specific data class:** use strongest permitted minimization while preserving non-reuse and never manufacture false historical certainty.

## ASM-WL005 — Consequential derived-state revalidation is operationally feasible

**Statement:** runtime can revalidate or materially bind LR-08 inputs where stale derived state could create incorrect canonical consequence.

**Stability:** EVOLVING.

**If false:** affected derived path cannot authorize consequence directly and must use stronger persisted Evaluation/snapshot semantics.

## ASM-WL006 — Physical technology comparison remains open

**Statement:** PostgreSQL hybrid, TypeDB and bounded graph/event/document mechanisms can be benchmarked without changing accepted Logical ontology.

**Stability:** STABLE logical intent.

**Refresh trigger:** Physical benchmark reveals an accepted invariant cannot be preserved efficiently/reliably by current candidate set.

# Rejected-alternative additions

```text
ALT-WL01 universal Entity / Thing ontology
REJECT — false semantic inheritance

ALT-WL02 universal Relationship / generic edge ontology
REJECT — relation-family collapse

ALT-WL03 universal Rule / Fact / WorkItem roots
REJECT — cross-slice semantic collapse

ALT-WL04 generic TermsRef / ProjectionRef / CommandRef roots
REJECT — implementation addressability does not justify new semantic owner

ALT-WL05 missing row = false convention
REJECT — corrupts unknown/negative-state semantics

ALT-WL06 ETag/MVCC token = MaterialStateRef
REJECT — transport/concurrency token != semantic material state

ALT-WL07 provider state as canonical source truth
REJECT — violates LR-09/reconciliation separation

ALT-WL08 stale LR-08 result as canonical-effect basis
REJECT — freshness/material-basis gap

ALT-WL09 AuthZ engine/store as canonical governance ontology
REJECT — enforcement != Domain governance

ALT-WL10 universal event sourcing as canonical ontology
REJECT — event representation may support history but does not own all semantics

ALT-WL11 document/EAV/property-bag canonical kernel
REJECT — semantic-free fallback

ALT-WL12 PostgreSQL selection without Physical benchmark
REJECT — current baseline must still compete under actual physical workload
```

# Stage-deferred Physical / Runtime decisions

```text
DEFER-WL01 concrete PostgreSQL schema/table/key strategy
DEFER-WL02 TypeDB benchmark schema/query design
DEFER-WL03 Neo4j graph/read projection role
DEFER-WL04 owner-specific vs shared typed-relation physical structures
DEFER-WL05 MaterialStateRef storage/index/version implementation
DEFER-WL06 expected-state token/API mechanics
DEFER-WL07 idempotency store/key lifetime/replay mechanics
DEFER-WL08 transaction/atomicity/staging boundary implementation
DEFER-WL09 provider outbox/inbox/sync/reconciliation mechanics
DEFER-WL10 LR-08 cache/materialization/freshness strategy
DEFER-WL11 retention/redaction/tombstone physical representation
DEFER-WL12 AuthN Principal persistence and session/device context
DEFER-WL13 AuthZ engine/vendor/policy-language selection
DEFER-WL14 canonical-to-AuthZ projection/cache consistency
DEFER-WL15 selective disclosure/RLS/application/sidecar enforcement split
DEFER-WL16 API route/DTO/serialization design
DEFER-WL17 event-stream/outbox/audit log bounded usage
DEFER-WL18 specialist document/telemetry stores
DEFER-WL19 indexes/constraints/partitioning/performance design
DEFER-WL20 migrations and rollout strategy
```

No deferred item may reinterpret accepted semantic ownership merely for implementation convenience.

# Whole decision integrity counters

```text
WHOLE ACCEPTED DECISIONS                20
WHOLE MATERIAL ASSUMPTIONS               6
WHOLE REJECTED ALTERNATIVES              12
WHOLE STAGE-DEFERRED PHYSICAL/RUNTIME    20

UNCLASSIFIED MATERIAL DECISIONS           0
UNREGISTERED MATERIAL ASSUMPTIONS         0
UNSAFE PHYSICAL DEFERRALS                 0
STALE MATERIAL EXTERNAL DEPENDENCIES      0
DOMAIN REOPEN REQUIRED                    0
```

No decision in this continuation authorizes SQL/schema/migrations, API/backend implementation, AuthN/AuthZ runtime, a database migration, provider adapters, frontend changes or modification of `main`.

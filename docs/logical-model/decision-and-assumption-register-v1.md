# LifeOS Logical Model Decision & Assumption Register v1

**Status:** Stage-0H normative foundation + Slice-A + Slice-B decisions  
**Date:** 2026-08-17  
**Purpose:** prevent forgotten rejected designs, hidden assumptions, stale external dependencies and accidental reversals during Logical Model design

---

## 1. Why this register exists

Logical-model work will compare many plausible structures. Without a durable register, teams tend to repeat rejected approaches, forget why a hardening exists, or let temporary assumptions silently become permanent architecture.

This register separates:

```text
ACCEPTED LOGICAL DECISION
REJECTED ALTERNATIVE
WORKING ASSUMPTION
EXTERNAL DEPENDENCY / EVIDENCE
STAGE-DEFERRED PHYSICAL DECISION
```

None of these categories may be silently substituted for another.

---

## 2. Accepted decision record

Every material accepted logical decision should record:

```text
DECISION ID
SLICE / SCOPE
QUESTION
SELECTED CANDIDATE
DOMAIN INVARIANTS PRESERVED
WHY SELECTED
FALSIFICATION SURVIVED
REJECTED ALTERNATIVES
TRACE / TEST REFERENCES
EXTERNAL EVIDENCE USED
ASSUMPTIONS
HARDENINGS
REGRESSION IMPACT CLASS
PHYSICAL DECISIONS DEFERRED
REOPEN TRIGGERS
STATUS
```

A decision is not accepted merely because one candidate was documented first.

---

## 3. Rejected Alternatives Register

Every materially plausible candidate that is rejected must remain discoverable.

Record at least:

```text
ALT ID
QUESTION / SCOPE
CANDIDATE
WHY IT LOOKED PLAUSIBLE
FAILURE EVIDENCE
INVARIANTS / TESTS FAILED
WHETHER REJECTION IS LOGICAL OR ONLY CURRENT-PHYSICAL
CONDITIONS THAT COULD JUSTIFY RETEST
```

Purpose:

- avoid rediscovering and re-proposing already falsified architectures;
- make future reviews understand trade-offs rather than seeing only the winner;
- distinguish a permanently semantically invalid candidate from one rejected only under current evidence;
- expose confirmation bias where all rejected alternatives are caricatures.

At least one rejected candidate should normally be a strong plausible alternative, not an obvious straw man.

---

## 4. Assumption Register

Any material decision that depends on something not guaranteed by the Domain Atlas must identify the assumption.

Record:

```text
ASSUMPTION ID
STATEMENT
SCOPE / DECISIONS DEPENDING ON IT
EVIDENCE
CONFIDENCE
STABILITY
FAILURE CONSEQUENCE
REFRESH TRIGGER
LAST VERIFIED
STATUS
```

Suggested stability vocabulary:

```text
STABLE
slow-changing standard/domain fact

EVOLVING
product/provider pattern likely to change over time

VOLATILE
API/provider/product behavior that may materially change quickly

UNPROVEN
working hypothesis requiring validation before acceptance
```

An `UNPROVEN` assumption cannot support a final PASS where its failure would materially invalidate the representation.

---

## 5. Refresh triggers

Assumptions/evidence must be rechecked when any of these occur:

```text
start of a slice materially depending on them
selection of a preferred candidate
provider/API version change
external standard revision
new product capability introduces conflicting pressure
later slice changes shared infrastructure
whole-logical final regression
material implementation feasibility evidence contradicts the assumption
```

Do not refresh external evidence merely for ceremony when it cannot affect the decision, but do not rely on stale remembered behavior where it can.

---

## 6. External evidence classification

External evidence should be recorded as one of:

```text
STRUCTURAL PRINCIPLE
mechanism/invariant useful beyond one vendor implementation

CURRENT PRODUCT BEHAVIOR
useful but potentially volatile implementation evidence

INTEROPERABILITY CONSTRAINT
must be respected when integration/standard compatibility matters

SPECIALIST BOUNDARY EVIDENCE
shows richer lifecycle/identity belongs to a bounded domain

NEGATIVE BENCHMARK
behavior LifeOS intentionally rejects
```

A current product behavior must not silently become a permanent LifeOS invariant.

---

## 7. Physical-stage deferral register

Logical Model should deliberately defer exact physical choices that are not needed to settle meaning.

Record:

```text
DEFER ID
LOGICAL QUESTION ALREADY RESOLVED
PHYSICAL QUESTION DEFERRED
WHY DEFERRAL IS SAFE
WHAT MUST BE PRESERVED LATER
ACTIVATION STAGE
```

Typical examples may include:

```text
exact PostgreSQL table split
index strategy
partitioning
ORM mapping
API serialization envelope
cache/read-model technology
runtime authorization enforcement mechanism
```

Deferral is invalid if it hides an unresolved logical behavior.

---

## 8. Decision quality checks

Before a material decision is accepted, verify:

1. the selected candidate is not simply the first candidate considered;
2. rejected alternatives include at least one materially plausible option where one exists;
3. assumptions are explicit;
4. external evidence is classified by stability and authority;
5. mutation and counterfactual tests challenged the preferred candidate;
6. simple and worst-case scenarios both survive;
7. the traceability ledger shows which Domain invariants are preserved;
8. later physical implementation still has more than one option where the Logical Model does not require one exact shape;
9. no provider-specific convenience has been promoted into semantic truth;
10. reopen triggers are concrete enough to detect future invalidation.

---

## 9. Seed anti-assumptions

The following must never be treated as implicit assumptions:

```text
one Account = one Person forever
one provider ID = one LifeOS referent
latest provider write = canonical truth
every scheduled block happened
every AI inference is a stable preference
every native referent needs one universal superclass
every cross-domain reference requires a generic semantic Relation
every semantic capability requires standalone persistence
every current product API behavior is permanent
every high-volume history requires event sourcing
every historical requirement requires full bitemporality everywhere
PostgreSQL convenience can redefine Domain meaning
```

If a candidate depends on one of these, it must be rejected or explicitly reformulated.

---

## 10. Register state vocabulary

```text
PROPOSED
UNDER TEST
ACCEPTED WITH HARDENING
ACCEPTED
REJECTED
SUPERSEDED LOGICALLY
STALE EVIDENCE — REFRESH REQUIRED
STAGE-DEFERRED PHYSICAL
BLOCKED
```

Historical accepted/rejected records remain preserved even after a later decision supersedes them.

---

## 11. Final closure requirement

Whole-Logical closure requires:

```text
unclassified material decisions        0
unregistered material assumptions      0
stale material external dependencies   0
rejected candidates without rationale  0
unsafe physical deferrals              0
```

The final clean-room reconstruction must be able to understand why the major representation choices were made using this register plus the traceability ledger, without relying on undocumented conversation history.

---

## 12. Slice A — accepted decisions

### DEC-A01 — Layered Typed Identity & Reference Model

```text
SLICE / SCOPE
A — Identity / Reference

QUESTION
How can heterogeneous native identities be addressed and referenced across LifeOS without a universal semantic Entity/Thing root or role-wrapper identities?

SELECTED CANDIDATE
Layered Typed Identity & Reference Model

CORE LOGICAL SHAPE
native owner identity
+
logical NativeRef addressability
+
Reference Contract
+
separate ExternalRef / Account / Principal identity spaces
+
history-preserving Reconciliation
+
separate Version/material-state reference
+
visibility-safe exposure boundary

WHY SELECTED
preserves Domain ownership while enabling reusable cross-domain addressability;
keeps role/relationship semantics in typed contracts;
survives provider migration, identity correction, privacy and future native-owner extension;
leaves multiple physical implementations available.

TRACE / TEST REFERENCES
TA-01..TA-17
INV-041..INV-060
TC-A01..A10
TC-L01..L12
Slice-A mutation/counterfactual package

REGRESSION IMPACT
R3 WHOLE-LOGICAL

STATUS
ACCEPTED WITH HARDENING — activation conditional on Slice-A remote QA
```

### DEC-A02 — NativeRef is addressability, not ontology

```text
QUESTION
Does common native-reference infrastructure imply a common semantic superclass?

DECISION
NO.

NativeRef identifies which already-justified native identity is addressed.
It creates no independent Domain entity and carries no generic relationship semantics.

STATUS
ACCEPTED WITH HARDENING
```

### DEC-A03 — Reference Contracts own semantic eligibility

```text
QUESTION
Where is the meaning of a heterogeneous reference preserved?

DECISION
In the containing slot/relation Reference Contract, including semantic role and eligible target families.

CONSEQUENCE
polymorphic technical reference != any-object semantic relation

STATUS
ACCEPTED
```

### DEC-A04 — ExternalRef is a separate scoped identity space

```text
QUESTION
How are provider/source IDs represented?

DECISION
As scoped ExternalRef/provider identity mappings distinct from NativeRef.

MINIMUM SCOPE
provider/source
+ realm/tenant/account/integration instance where required
+ provider object type where required
+ opaque external ID
+ version/revision where material

STATUS
ACCEPTED WITH HARDENING
```

### DEC-A05 — identity reconciliation is explicit and correctable

```text
QUESTION
How are duplicate native identities / later identity matches handled?

DECISION
Represent equivalence/redirect/current resolution through explicit Reconciliation/history rather than destructive proof-erasing rewrite.

HARDENING
obsolete/superseded identity handle is not reused;
wrong merge/link can be corrected/revoked;
historical references are not automatically rewritten to claim final knowledge existed earlier.

STATUS
ACCEPTED WITH HARDENING
```

### DEC-A06 — identity != Version/material state

```text
DECISION
NativeRef identifies the continuing referent; material Version/state addressing is a separate logical concern.

STATUS
ACCEPTED WITH Slice-D deferral
```

### DEC-A07 — internal identity != universal disclosure handle

```text
DECISION
LifeOS may maintain one internal native identity while authorized API/product contexts expose scoped handles or no cross-context linkage.

STATUS
ACCEPTED WITH Slice-F/API-security deferral
```

---

## 13. Slice A — rejected / retained alternatives

### ALT-A01 — Universal semantic Entity/Object root

```text
WHY PLAUSIBLE
maximum polymorphism and cross-domain query convenience

FAILURE
reintroduces forbidden universal semantic root;
encourages generic relation/property fallback;
blurs native/product/provider identity.

FAILED
INV-007, INV-008, INV-039, INV-041, INV-045, INV-046

CLASS
LOGICALLY REJECTED

RETEST
only if Domain Atlas itself is legitimately reopened under the Domain reopen gate
```

### ALT-A02 — Owner/role-specific reference families only

```text
WHY PLAUSIBLE
strongest direct type safety and ordinary FK-friendly representation

RESULT
VIABLE STRONG ALTERNATIVE

WHY NOT SELECTED AS LOGICAL BASELINE
repeats common heterogeneous-addressability/reconciliation/provider mechanics;
expands unions/reference families as native owners grow;
Reference Contracts provide equivalent semantic guardrails while retaining reusable addressability.

CLASS
NOT LOGICALLY INVALID

RETEST
if common NativeRef addressability creates material complexity/leakage or Physical Model proves owner-specific references materially superior without logical cost
```

### ALT-A03 — Mandatory global identity-registry root

```text
WHY PLAUSIBLE
single FK target, global lookup, shared history hooks

FAILURE AS LOGICAL REQUIREMENT
risks turning technical registry into ontology;
may force native identity onto role/value/dependent/supply/provider representations that do not justify it.

CLASS
LOGICALLY REJECTED AS REQUIREMENT

RETEST
may reappear as PHYSICAL technical anchor if it preserves DEC-A01/02 and all Slice-A invariants
```

### ALT-A04 — encoded typed IDs as the semantic contract

```text
WHY PLAUSIBLE
Shopify/Atlassian/AWS/OCI/Twilio-style operational convenience

FAILURE
ID format migrations can break semantic consumers; GitHub provides direct negative evidence.

CLASS
LOGICALLY REJECTED

RETEST
encoded type may be a redundant transport hint only if semantic owner/type remains independently contracted
```

### ALT-A05 — provider-ID-driven automatic merge

```text
WHY PLAUSIBLE
simpler ingestion/dedup

FAILURE
provider scope/identity churn, wrong merges, Home Assistant source-of-truth counterexample, Person/privacy risk.

CLASS
LOGICALLY REJECTED
```

---

## 14. Slice A — assumptions / evidence dependencies

### ASM-A01 — multiple physical representations remain feasible

```text
STATEMENT
The accepted logical contract can later be implemented through a technical anchor/registry, owner-specific FK structures, composite typed references or a hybrid without changing Slice-A meaning.

EVIDENCE
PostgreSQL constraint model + candidate analysis

CONFIDENCE
HIGH

STABILITY
EVOLVING until Physical Model validation

FAILURE CONSEQUENCE
targeted Slice-A logical reopen if every feasible physical representation breaks a required invariant

REFRESH TRIGGER
Physical Model start and WD-05 final pressure

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED WORKING ASSUMPTION — not UNPROVEN for logical meaning, but must be physically demonstrated later
```

### ASM-A02 — external identifier scope is provider-contract-specific

```text
STATEMENT
ExternalRef uniqueness cannot use one universal LifeOS scope formula; adapters must honor the provider's documented issuer/tenant/account/resource scope.

EVIDENCE
OIDC, SCIM, Apple, Entra, cloud/provider references

CONFIDENCE
HIGH

STABILITY
STABLE principle / provider details EVOLVING

REFRESH TRIGGER
provider integration design or provider contract change

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED
```

### ASM-A03 — internal identity linkage can require scoped external exposure

```text
STATEMENT
A single internal identity may need context-specific public/API handles to prevent correlation/privacy leakage.

EVIDENCE
OIDC pairwise subjects, SCIM privacy direction, Apple transfer identifiers

CONFIDENCE
HIGH

STABILITY
STABLE principle

FAILURE CONSEQUENCE
API/security design could leak cross-context identity

REFRESH TRIGGER
Slice F and API/security stage

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED WITH LATER IMPLEMENTATION DEFERRAL
```

No Slice-A PASS depends on a material `UNPROVEN` assumption.

---

## 15. Slice A — external evidence register

```text
EVID-A01 OpenID Connect pairwise sub          STRUCTURAL PRINCIPLE / PRIVACY
EVID-A02 SCIM id vs externalId                STRUCTURAL PRINCIPLE / INTEROP
EVID-A03 Auth0 link/unlink identities         CURRENT PRODUCT + STRUCTURAL PRINCIPLE
EVID-A04 Sign in with Apple transfer ID       CURRENT PRODUCT + MIGRATION PRINCIPLE
EVID-A05 Microsoft Entra pairwise sub/oid     CURRENT PRODUCT + STRUCTURAL PRINCIPLE
EVID-A06 Outlook Immutable ID                 CURRENT PRODUCT / SCOPE-LIFETIME PRESSURE
EVID-A07 FHIR Reference/type/targetProfile    STRUCTURAL PRINCIPLE
EVID-A08 FHIR Person pressure                 SPECIALIST BOUNDARY EVIDENCE
EVID-A09 Salesforce polymorphic refs          STRUCTURAL PRINCIPLE
EVID-A10 Shopify GID                          CURRENT PRODUCT / TYPED ADDRESSABILITY
EVID-A11 Asana gid + resource_type            CURRENT PRODUCT / TYPED ADDRESSABILITY
EVID-A12 Atlassian ARI                        CURRENT PRODUCT / GLOBAL SCOPED ADDRESS
EVID-A13 AWS ARN                              INFRASTRUCTURE ADDRESSABILITY
EVID-A14 OCI OCID                             INFRASTRUCTURE ADDRESSABILITY
EVID-A15 Kubernetes UID/resourceVersion       STRUCTURAL PRINCIPLE / VERSION SEPARATION
EVID-A16 Git refs/object IDs                  STRUCTURAL PRINCIPLE / ALIAS-VERSION PRESSURE
EVID-A17 GitHub node-ID migration             NEGATIVE BENCHMARK / OPAQUE ID
EVID-A18 Google People sources/linking        CURRENT PRODUCT / SOURCE-AGGREGATION PRESSURE
EVID-A19 Wikidata merge/redirect/unmerge      STRUCTURAL PRINCIPLE / CORRECTION
EVID-A20 Home Assistant 2026.8 device split   NEGATIVE BENCHMARK / SOURCE-OF-TRUTH
EVID-A21 Twilio SID                           CURRENT PRODUCT / TYPE-PREFIX COUNTERPOINT
EVID-A22 PostgreSQL inheritance constraints   PHYSICAL FEASIBILITY EVIDENCE
```

Canonical details and source URLs: `benchmarks/identity-reference-v1.md`.

---

## 16. Slice A — physical deferrals

```text
DEFER-A01 exact PostgreSQL native-reference anchor/registry shape
DEFER-A02 owner-specific FK vs composite vs hybrid strategy
DEFER-A03 native key data type / generation algorithm
DEFER-A04 index/partition strategy
DEFER-A05 ORM polymorphism mapping
DEFER-A06 public/API identity-handle serialization
DEFER-A07 runtime authorization/identity-resolution enforcement
```

All are `STAGE-DEFERRED PHYSICAL`. None may later weaken NativeRef/Reference Contract/ExternalRef/Reconciliation invariants.

---

## 17. Slice B — accepted decisions

### DEC-B01 — Layered Typed Intention & Execution Model

```text
SLICE / SCOPE
B — Intention / Execution

QUESTION
How can LifeOS preserve candidate future, adopted intent, strategy, action, expected occurrence, recurring policy, proposal/request/decision and dependency semantics without a universal WorkItem/workflow/status ontology?

SELECTED CANDIDATE
Layered Typed Intention & Execution Model

CORE SHAPE
typed semantic owner
+
owner-specific material state/version
+
typed links / semantic acts
+
selective materialization
+
history / lineage
+
derived operational projections

WHY SELECTED
preserves all accepted Domain non-collapse boundaries;
keeps simple cases compact;
retains version/replacement/approval history pressure;
allows shared technical mechanisms without shared lifecycle or ontology;
leaves multiple physical implementations open.

TRACE / TEST REFERENCES
TB-01..TB-18
INV-061..INV-084
TC-B01..B06
TC-N01..N22
Slice-B mutation/counterfactual package

REGRESSION IMPACT
R3 WHOLE-LOGICAL

STATUS
ACCEPTED WITH HARDENING — activation conditional on Slice-B remote QA
```

### DEC-B02 — no universal canonical lifecycle/status

```text
DECISION
Each semantic owner retains owner-specific lifecycle/disposition dimensions.
Product/UI status may be a derived projection.

STATUS
ACCEPTED
```

### DEC-B03 — Possibility maturation creates/link Goal; no retyping

```text
DECISION
Later intentional adoption establishes distinct Goal identity and may link back to the prior Possibility.
Pre-adoption history remains Possibility history.

STATUS
ACCEPTED
```

### DEC-B04 — Proposal/Request/Decision use selective materialization

```text
DECISION
Persist them independently when their own lifecycle/reference/history/audit/authority/version-binding matters.
Do not manufacture standalone records for every trivial synchronous interaction.

STATUS
ACCEPTED WITH HARDENING
```

### DEC-B05 — Decision is resolution, not effect

```text
DECISION
Decision may have zero/one/many effects.
Target state remains owned by the affected concept.
Previously authorized policy may produce permitted effects without a synthetic new Decision per mutation.

STATUS
ACCEPTED
```

### DEC-B06 — material target state matters to approval/applicability

```text
DECISION
Where reviewed content can change materially, Proposal/Decision may bind the consequential target state/version.
Material change does not automatically inherit prior approval.

STATUS
ACCEPTED WITH Slice-D hardening dependency
```

### DEC-B07 — Plan revision and replacement are distinct

```text
DECISION
Ordinary operational edits may remain same Plan identity/material revision.
Materially different execution strategy may create linked replacement/continuation Plan identity.
No field-count threshold defines the boundary.

STATUS
ACCEPTED WITH Slice-D history dependency
```

### DEC-B08 — Dependency is typed contingency; blocked is derived

```text
DECISION
Dependency is LR-03 typed directional contingency between bounded states/results/transitions.
Hierarchy, temporal order and containment do not establish Dependency.
Current blocked/satisfied view is normally derived.

STATUS
ACCEPTED
```

### DEC-B09 — explicit bounded user request may itself authorize requested action

```text
DECISION
AI participation does not force a redundant approval ceremony when the user's explicit request already supplies the applicable bounded authority/intention.
AI-generated details retain source/provenance and cannot silently become user facts/preferences.

STATUS
ACCEPTED WITH Slice-F/runtime governance dependency
```

### DEC-B10 — governed-by material state must be representable

```text
DECISION
When consequence requires, later execution/Occurrence can identify the material Plan/Routine/Policy state that governed it.

STATUS
ACCEPTED WITH Slice-C/D deferral
```

---

## 18. Slice B — rejected / retained alternatives

### ALT-B01 — Universal WorkItem / IntentItem

```text
WHY PLAUSIBLE
simple schema, one search/filter/status system, easy polymorphic UI

FAILURE
false superclass;
universal lifecycle;
Possibility→Goal retyping pressure;
Dependency/hierarchy ambiguity;
Proposal/Request/Decision collapse;
semantic debt moves into kind/status/metadata.

CLASS
LOGICALLY REJECTED

RETEST
only if Domain Atlas is legitimately reopened; technical read-model projections may still unify search/UI without becoming canonical ontology
```

### ALT-B02 — Fully owner-specific persistence/mechanisms

```text
WHY PLAUSIBLE
maximum local semantic and relational specificity

RESULT
VIABLE STRONG ALTERNATIVE

WHY NOT SELECTED AS COMPLETE LOGICAL BASELINE
duplicates common addressability/material-state/version/history mechanics without increasing semantic correctness.

CLASS
NOT LOGICALLY INVALID

RETEST
Physical Model may use it wholly or partly if it preserves DEC-B01 and all cumulative invariants
```

### ALT-B03 — Universal command/event-sourced model

```text
WHY PLAUSIBLE
excellent auditability, event chronology and derived current views

FAILURE AS LOGICAL REQUIREMENT
technical events risk becoming ontology;
current state depends on replay/projection policy;
simple cases and high-volume mutation become unnecessarily expensive;
owner semantics remain necessary anyway.

CLASS
LOGICALLY REJECTED AS UNIVERSAL REQUIREMENT

RETEST
event sourcing may be a bounded physical implementation technique later
```

### ALT-B04 — Universal desired-spec/current-status model

```text
WHY PLAUSIBLE
Kubernetes-like clear intended/current separation

FAILURE
Possibility, Proposal, Request, Decision, Milestone and Dependency are not universally reducible to desired spec/current status.

CLASS
LOGICALLY REJECTED UNIVERSALLY

RETAINED PRINCIPLE
intended != actual
```

---

## 19. Slice B — assumptions / evidence dependencies

### ASM-B01 — material Version mechanism can later preserve Slice-B state bindings without owner collapse

```text
STATEMENT
Slice D can provide a version/material-state mechanism capable of identifying consequential reviewed/governing state while keeping owner identity separate.

EVIDENCE
accepted Domain Version model + GitHub approval/version behavior + AWS/Google workflow revision/execution patterns

CONFIDENCE
HIGH

STABILITY
STABLE logical requirement / physical mechanism DEFERRED

FAILURE CONSEQUENCE
targeted Slice-B/D logical reopen if no sound shared or owner-specific Version representation can satisfy this

REFRESH TRIGGER
Slice D

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED WITH LATER-SLICE PROOF OBLIGATION
```

### ASM-B02 — selective materialization can remain compact and auditable

```text
STATEMENT
LifeOS can materialize Proposal/Request/Decision only when their independent semantic lifecycle/history matters without losing reconstructibility for consequential changes.

EVIDENCE
simple-case counterfactuals + change-review/request workflow benchmarks

CONFIDENCE
HIGH

STABILITY
STABLE principle

FAILURE CONSEQUENCE
revisit materialization threshold/contract, not Domain owner semantics automatically

REFRESH TRIGGER
Slice F and Physical/API design

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED WITH HARDENING
```

### ASM-B03 — derived operational status can satisfy UI/search needs without becoming canonical owner lifecycle

```text
STATEMENT
Product/UI/search can project normalized operational states from owner-specific canonical semantics.

EVIDENCE
existing LifeOS product status design + iCalendar differing status sets + modern work-management products

CONFIDENCE
HIGH

STABILITY
STABLE principle

FAILURE CONSEQUENCE
introduce richer projection/read-model design, not a universal semantic status root

REFRESH TRIGGER
API/product read-model design

LAST VERIFIED
2026-08-17

STATUS
ACCEPTED
```

No Slice-B PASS depends on a material `UNPROVEN` assumption.

---

## 20. Slice B — external evidence register

```text
EVID-B01 Terraform plan/apply                 STRUCTURAL PRINCIPLE
EVID-B02 Kubernetes spec/status              STRUCTURAL PRINCIPLE + ANTI-COPY
EVID-B03 Apache Airflow DAG/DagRun           STRUCTURAL PRINCIPLE
EVID-B04 AWS Step Functions versions/runs    STRUCTURAL PRINCIPLE
EVID-B05 Google Cloud Workflows revisions    STRUCTURAL PRINCIPLE
EVID-B06 GitHub stale approval behavior      CURRENT PRODUCT + STRUCTURAL PRINCIPLE
EVID-B07 SAP approval restart pressure       CURRENT PRODUCT BEHAVIOR
EVID-B08 FHIR Goal/CarePlan/Request/Task     SPECIALIST BOUNDARY + STRUCTURAL PRINCIPLE
EVID-B09 Jira Product Discovery             CURRENT PRODUCT / DISCOVERY-DELIVERY
EVID-B10 Aha! ideas/initiatives/features     CURRENT PRODUCT / DISCOVERY-DELIVERY
EVID-B11 Motion task/schedule separation     CURRENT PRODUCT
EVID-B12 Reclaim habit/conflict rules        CURRENT PRODUCT
EVID-B13 Todoist recurring-task advancement  NEGATIVE BENCHMARK
EVID-B14 iCalendar RFC 5545 status families  INTEROPERABILITY / STRUCTURAL PRINCIPLE
EVID-B15 Stripe PaymentIntent lifecycle      SPECIALIST BOUNDARY EVIDENCE
EVID-B16 Notion generic properties/relations NEGATIVE + EXTENSION EVIDENCE
EVID-B17 BPMN / DMN                          SPECIALIST PROCESS/RULE EVIDENCE
```

Canonical source URLs and dispositions: `benchmarks/intention-execution-v1.md`.

---

## 21. Slice B — physical deferrals

```text
DEFER-B01 exact PostgreSQL owner/table split
DEFER-B02 owner-state/version table strategy
DEFER-B03 exact Proposal/Request/Decision materialization persistence mechanics
DEFER-B04 event sourcing usage, if any
DEFER-B05 API lifecycle/status projections
DEFER-B06 exact Plan replacement/version serialization
DEFER-B07 exact Dependency physical/FK representation
DEFER-B08 exact governed-by Version reference implementation
DEFER-B09 exact Occurrence/Schedule/Session/Actual persistence — Slice C
DEFER-B10 runtime authorization/policy enforcement — Slice F/runtime stage
```

All are `STAGE-DEFERRED PHYSICAL` or explicitly later-slice concerns. None may weaken the Slice-B logical invariants.

---

## 22. Integrated A+B decisions and mechanism reconsideration

This section is normative and records the cumulative checkpoint that ran after Slice B became active.

### Supersession of DEC-B09

`DEC-B09` is preserved above as historical decision text, but its broad wording is **SUPERSEDED LOGICALLY** by `DEC-AB03` below.

```text
OLD / SUPERSEDED
explicit Request may itself authorize the action

CURRENT
explicit Request/instruction may establish requester intent
but does not create Authority/Consent/governance power
```

### DEC-AB01 — Discriminated ReferenceAddress family

```text
SCOPE
Integrated A+B — shared reference/addressability

QUESTION
How can LifeOS address native identities, persistent contextual records, material states and provider identities without treating them as one universal object identity?

SELECTED
ReferenceAddress discriminated family + Reference Contract

SHAPE
ReferenceAddress
  NativeRef
  ScopedRecordRef
  MaterialStateRef
  ExternalRef

RULE
ReferenceAddress is representation vocabulary only.
No variant implies semantic eligibility without the containing Reference Contract.

STATUS
ACCEPTED WITH HARDENING

IMPACT
R3 WHOLE-LOGICAL
```

### DEC-AB02 — canonical Activity/Event identity cannot be storage-demoted

```text
DECISION
Once canonical persisted Activity/Event semantics exist, they retain LR-01 logical identity.
A transient suggestion/input is not automatically a canonical Activity/Event/Possibility.

STATUS
ACCEPTED WITH HARDENING
```

### DEC-AB03 — user instruction may remove redundant confirmation, not governance

```text
DECISION
An explicit user instruction/request may be sufficient evidence of that Actor's bounded intent/instruction and may eliminate a redundant confirmation step.
It does not establish Authority, Consent or governance power over another/shared context.

STATUS
ACCEPTED — supersedes DEC-B09 wording
```

### DEC-AB04 — Dependency endpoint includes material facet/state binding

```text
DECISION
Where the contingency is not about the target as a whole, Dependency endpoint semantics bind:
ReferenceAddress(target)
+ relevant facet/state/result/transition/condition.

No universal expression language is selected.

STATUS
ACCEPTED WITH HARDENING
```

### DEC-AB05 — selective materialization != selective auditability

```text
DECISION
A trivial direct Request/Decision need not have a standalone semantic record, but consequential target change must still retain enough actor/source/basis/history under later Provenance/Version/governance mechanics.

STATUS
ACCEPTED WITH Slice-D/F dependency
```

### DEC-AB06 — cross-owner maturation/replacement uses typed lineage

```text
DECISION
Possibility -> Goal uses typed adoption/origin lineage.
Distinct replacement Plan -> predecessor Plan uses typed replacement/continuation lineage.
Neither may degrade to generic related_to or imply Version identity continuity automatically.

STATUS
ACCEPTED
```

---

## 23. Integrated A+B technology/mechanism candidate reconsideration

The cumulative checkpoint materially changed the reference-addressability constraint. Under LM-WF-21 the selected mechanism received no incumbent preference.

### TECH-AB-A — owner-specific references only

```text
WHY PLAUSIBLE
strongest local type/FK constraints; no universal root

CURRENT RESULT
still a strong Physical Model ingredient

WHY NOT LOGICAL BASELINE
repeats heterogeneous address/history machinery across owners and makes cross-owner slots continually rebuild expanding unions

STATUS
RETAINED ALTERNATIVE — NOT LOGICALLY INVALID

RETEST
Physical Model; or earlier if ReferenceAddress produces material semantic/operational complexity
```

### TECH-AB-B — global Node/Entity registry/interface

```text
WHY PLAUSIBLE
uniform global addressing/refetch and one common target

EVIDENCE
Relay/GraphQL Global Object Identification is a strong working example of a universal Node interface for globally identified/refetchable objects.

WHY REJECTED FOR LIFEOS LOGICAL BASELINE
common addressability would be too easy to interpret as common ontology;
native/scoped-record/material-state/external identity spaces would be pressured to converge;
contradicts LifeOS anti-universal-root discipline if semanticized.

STATUS
REJECTED AS LOGICAL BASELINE

RETEST
a narrow technical registry/interface may be physical/API-only if all ReferenceAddress distinctions and contracts remain explicit
```

### TECH-AB-C — one undifferentiated TypedRef(kind,id)

```text
WHY PLAUSIBLE
compact polymorphic address mechanism

FAILURE
kind/id alone does not strongly preserve native identity vs scoped record vs material state vs provider identity.
Adding those discriminators and contracts converges toward TECH-AB-D.

STATUS
REJECTED AS UNDERSPECIFIED
```

### TECH-AB-D — discriminated ReferenceAddress family + Reference Contract

```text
WHY PLAUSIBLE
common addressability without common ontology;
explicit address spaces;
semantic target eligibility stays in Reference Contract;
can extend later without changing existing address meaning;
keeps physical implementation open.

EXTERNAL STRUCTURAL EVIDENCE
FHIR Reference: typed/limited references and target constraints
FHIR Provenance: version-specific target pressure
Kubernetes ObjectReference: kind/name/namespace/UID plus resourceVersion/fieldPath
Kubernetes metadata: UID != resourceVersion
PostgreSQL inheritance: PK/unique/FK constraints do not magically span child tables
Relay GraphQL Node: useful global-address benchmark but negative ontology benchmark for LifeOS

ANTI-COPY
FHIR/Kubernetes/Relay ontologies are not adopted; only address/type/state separation lessons are used.

STATUS
SELECTED
VERDICT
RETAIN + HARDEN
```

---

## 24. Integrated A+B evidence register

```text
EVID-AB01 FHIR R5 Reference/type/target constraints        STRUCTURAL PRINCIPLE
EVID-AB02 FHIR R5 Provenance version-specific targets     STRUCTURAL PRINCIPLE / STATE ADDRESS
EVID-AB03 Kubernetes ObjectReference                      STRUCTURAL PRINCIPLE
EVID-AB04 Kubernetes UID vs resourceVersion               STRUCTURAL PRINCIPLE
EVID-AB05 PostgreSQL inheritance constraint limitations   PHYSICAL FEASIBILITY EVIDENCE
EVID-AB06 Relay GraphQL Global Object Identification      NEGATIVE ONTOLOGY / API ADDRESS BENCHMARK
```

Verified against current official/primary documentation on 2026-08-17. Refresh when a later decision materially depends on changed behavior/specification or at Whole-Logical final regression.

No integrated A+B PASS depends materially on one volatile vendor behavior.

---

## 25. Integrated assumptions / physical deferrals

### ASM-AB01 — ReferenceAddress remains implementable through multiple physical strategies

```text
STATEMENT
The discriminated logical address family can be preserved by owner-specific FKs, a technical registry/anchor, composite typed references, API/read-model unions or hybrid strategies without creating one semantic root.

CONFIDENCE
HIGH logical plausibility

STABILITY
EVOLVING until Physical Model proof

FAILURE CONSEQUENCE
reopen the logical mechanism under LM-WF-21 before changing Domain semantics

REFRESH TRIGGER
Physical Model start; WD-05 discharge; material later-slice pressure

STATUS
ACCEPTED WITH PHYSICAL PROOF OBLIGATION
```

### DEFER-AB01 — exact physical ReferenceAddress strategy

```text
DEFERRED
registry/anchor vs owner-specific FK vs composite/hybrid

WHY SAFE
address-space semantics and target eligibility are already defined independently of storage

ACTIVATION
Physical Model
```

### DEFER-AB02 — MaterialStateRef construction

```text
DEFERRED
exact identity/storage/history mechanics for materially relevant state references

WHY SAFE
address-space distinction is fixed; Slice D owns exact Version/material-state mechanism

ACTIVATION
Slice D
```

### DEFER-AB03 — Dependency condition expression/composition

```text
DEFERRED
all/any/quorum/alternative/predicate expression mechanism

WHY SAFE
endpoint + material facet/state/result/transition binding is already required; no evidence yet justifies one universal expression language

ACTIVATION
later reasoning/physical design if concrete cases require it
```

No integrated A+B decision relies on a material `UNPROVEN` assumption.

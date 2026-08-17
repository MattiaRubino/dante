# LifeOS Logical Model Decision & Assumption Register v1

**Status:** Stage-0H normative foundation  
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

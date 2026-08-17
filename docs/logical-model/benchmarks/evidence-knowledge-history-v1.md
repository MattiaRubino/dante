# LifeOS Logical Model — Slice D External Benchmark v1

**Verified:** 2026-08-17  
**Scope:** Evidence / Knowledge / History  
**Policy:** external products, standards and database technologies are evidence, not ontology authority

---

## 1. Benchmark questions

Slice D used external evidence to pressure-test:

- stable target identity versus material state;
- provenance versus truth;
- claim/reference qualification;
- effective/world time versus knowledge/transaction time;
- historical time-travel;
- current-state reconstruction;
- version/snapshot identity;
- temporary versus ongoing applicability;
- external/provider revision versus semantic materiality;
- large-scale lineage/history without universal ontology collapse.

---

## 2. W3C PROV

Useful mechanism:

```text
entities
activities
agents
generation / derivation / attribution / revision lineage
```

LifeOS disposition:

```text
BORROW
lineage role separation and derivation discipline

ADAPT
typed bounded provenance segments around LifeOS target/material-state references

REJECT AS KERNEL ONTOLOGY
universal PROV Entity/Activity/Agent mapping for all LifeOS concepts
```

Reason: Provenance solves origin/evolution, not Evidence relevance, Confirmation, current accepted interpretation, Reconciliation or LifeOS domain identity.

---

## 3. W3C Verifiable Credentials 2.0 family

Useful pressure:

```text
cryptographic/verifiable integrity
!= automatic substantive truth of every claim
```

LifeOS disposition:

```text
BORROW
verification/authenticity is a bounded property/evaluation

REJECT
verified=true as universal factual truth
issuer identity as universal source precedence
```

This reinforces:

```text
Provenance != truth
Verification != universal truth
trusted/verified source != canonical state automatically
```

---

## 4. Wikidata statements

Useful mechanism:

```text
statement
property/value
qualifiers
references
rank
multiple/conflicting values
```

LifeOS disposition:

```text
BORROW / ADAPT
qualified assertion/value representation where a bounded family needs it
references/context/conflict as useful patterns

REJECT AS UNIVERSAL KERNEL
all LifeOS semantics as subject-predicate-object statements
rank as universal LifeOS reconciliation/source-precedence rule
```

Wikidata is strong evidence that bare key/value is insufficient for serious knowledge representation. It is also strong evidence that a universal statement graph is a substantial ontology choice, not a neutral storage convenience.

---

## 5. HL7 FHIR R5 — Provenance

Useful mechanism:

- provenance targets may refer to specific resource versions;
- agents/entities/activities around generation/change are explicit;
- Provenance remains distinct from audit and target semantics.

LifeOS disposition:

```text
BORROW
specific material target-state binding
lineage separated from target

REJECT
FHIR resource/version ontology as LifeOS kernel schema
server version ID as automatic LifeOS material state
```

---

## 6. HL7 FHIR R5 — Condition / Observation

Useful applicability pressure:

FHIR Condition represents conditions/problems/diagnoses with concepts such as:

```text
clinical status
onset
abatement/resolution timing
recorded date
```

FHIR Observation exposes an `effective[x]` time/period representing when an observed value is asserted as relevant/true for the subject context.

LifeOS disposition:

```text
BORROW
historical record existence != current applicability
onset/effective period != recorded/learned time
resolved/inactive state does not erase history
point Observation != continuing condition automatically

ADAPT
owner-specific applicability/lifecycle + shared temporal/history contract

REJECT
universal clinical Condition lifecycle/status enum for all LifeOS facts
health ontology as LifeOS kernel
```

This benchmark directly pressures examples such as ongoing celiac context, bounded fracture episode and point/temporary fever information.

---

## 7. SQL Server system-versioned temporal tables

Useful mechanism:

```text
current table + history table
AS OF / temporal querying
automatic row-version history
```

LifeOS disposition:

```text
RETAIN AS POSSIBLE PHYSICAL TECHNIQUE
```

But:

```text
row update/version != semantic material-state revision automatically
transaction/system time != world/effective time automatically
```

Therefore temporal tables may implement part of future history storage but do not define `MaterialStateRef` semantics.

---

## 8. Datomic

Useful mechanism:

```text
immutable facts/assertions
history database
as-of / since
transaction chronology
```

LifeOS disposition:

```text
RETAIN AS STRONG HISTORY ARCHITECTURE EVIDENCE
```

But Datomic transaction/history semantics do not by themselves answer:

```text
when a represented fact applied in the world
which interpretation LifeOS accepted in a bounded context
which evidence was relevant
which source should win
```

Universal immutable assertion storage therefore remains a possible implementation family, not the Logical Model ontology.

---

## 9. Apache Iceberg snapshots / branches / tags

Useful mechanism:

```text
snapshot identity
current head
historical snapshots
branches/tags
retention/time travel
```

LifeOS disposition:

```text
BORROW
stable historical state/snapshot addressability as architectural pressure

REJECT
storage snapshot = semantic MaterialStateRef automatically
```

A LifeOS material state may map to one or several technical snapshots, or several technical snapshots may remain materially equivalent for one semantic purpose.

---

## 10. OpenLineage

Useful mechanism:

```text
Job
Run
Dataset
facets
lineage events
```

LifeOS disposition:

```text
BORROW
role-specific lineage modeling and extensible facets

REJECT
data-engineering taxonomy as LifeOS ontology
```

Important lesson: even a lineage-focused system benefits from typed roles rather than one undifferentiated lineage node.

---

## 11. Negative benchmark patterns

Explicitly rejected as LifeOS kernel defaults:

```text
universal Fact / Claim table or graph
source/reference presence = truth
latest timestamp wins
provider revision = semantic version
ETag/MVCC = MaterialStateRef
all history = one event type stream
one universal valid_from/valid_to model regardless of semantics
current knowledge = latest row
old record = still applicable now
missing end = permanent
one generic confirmed/read/verified/status boolean
private source automatically visible with derived consequence
```

---

## 12. Mechanism reconsideration result

Candidates re-opened under LM-WF-21:

```text
A universal Fact / Claim graph
B universal event-sourced/bitemporal ledger
C fully owner-specific history
D PROV-like global lineage graph
E layered typed epistemic/history model
```

Current verdict:

```text
E SELECTED

ReferenceAddress
RETAIN + HARDEN

MaterialStateRef
PRECISE LOGICAL CONTRACT

A/B/C/D
retain selected mechanisms as bounded/physical ingredients where useful;
not selected as complete Logical Model baseline
```

---

## 13. Freshness / revisit triggers

Re-check before Whole-Logical closure if materially influential external specifications/products have changed.

Reopen this benchmark if:

- a substantially stronger generalized history/knowledge model solves LifeOS owner/state/evidence/reconciliation boundaries without generic semantic collapse;
- the Physical Model proves a selected technique cannot satisfy MaterialStateRef/history queries;
- specialist condition/applicability pressure cannot remain safely bounded;
- privacy/retention requirements make the current historical-reference contract impossible.

Implementation convenience alone is insufficient.
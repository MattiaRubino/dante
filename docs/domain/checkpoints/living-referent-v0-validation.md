# Living Referent v0 — Domain Validation Methodology v3

**Status:** PASS WITH HARDENING — repository closure QA pending  
**Date:** 2026-08-16  
**Baseline review trigger:** second Whole-Domain V3 safety rerun against the accepted LifeOS North Star, inverse reconstruction, simulation coverage and external-product pressure  
**Owning concept:** `../concepts/living-referent.md`

## 1. Review question

The review asks whether LifeOS has a real semantic need for persistent native identity for individually tracked non-human living organisms/specimens, or whether existing Person, Asset, Subject, Observation, Resource, Place and relationship semantics are sufficient.

The result is a targeted reopen because the existing model contains both of these accepted constraints:

```text
Subject
= contextual aboutness role
= does not create identity

Asset
= scoped native identity for individually tracked non-human physical objects
= excludes animals/plants by default
```

Product simulations now require continuity for individual living non-human subjects across care/history contexts. Therefore the former deferred trigger has fired.

---

## 2. Candidate reductio

```text
H0
Use Subject as living identity
→ FAIL
Subject explicitly does not manufacture identity.

H1
Expand Asset to include animals/plants
→ FAIL
Collapses materially different living/object boundaries and contradicts accepted Asset scope.

H2
Create Pet / Animal / Plant roots
→ FAIL
Overmodels product/type vocabulary and duplicates one identity capability.

H3
Create universal LivingThing / BiologicalEntity root
→ FAIL
No demonstrated LifeOS need for a universal biological ontology or Person superclass.

H4
Living Referent = scoped native non-human living identity
triggered only when individual identity materially matters
→ SURVIVES
```

Accepted result:

```text
NEW NATIVE REFERENT
YES — Living Referent

UNIVERSAL LIVING ROOT
NO
```

---

## 3. Canonical definition

> **A Living Referent is the persistent native representation of an individually tracked non-human living organism/specimen whose distinct identity and materially relevant life/care history matter across LifeOS contexts independently from names, species/type labels, ownership/care relations, current Place, Subject role, provider identifiers or any one Observation/Activity.**

Canonical question:

> **Which individually tracked non-human living organism/specimen is this?**

---

## 4. CORE-01..13

### CORE-01 — workflow inversion

Representative workflows were inverted from user/product needs rather than from a proposed table/type hierarchy.

Examples:

```text
pet weight/care history
plant condition/care history
caregiver change
owner change
location change
vet/grooming/care events
longitudinal photos/documents
renaming/classification correction
propagation/replacement
```

The common irreducible requirement is continuity of the specific organism/specimen, not a generic pet/plant module.

**Result: PASS**

### CORE-02 — deep chronology

Tested chronology:

```text
T0 specific organism begins being tracked
T1 renamed
T2 classification corrected
T3 moved
T4 caregiver/owner changes
T5 care/health observations accumulate
T6 related content/events accumulate
T7 organism dies
T8 historical record remains queryable
```

Identity remains stable across ordinary changes. Death does not erase history.

**Result: PASS WITH HARDENING**

### CORE-03 — adversarial reductio

Removing Living Referent forces identity into Subject, Asset or ad-hoc profile records. Broadening it to universal biological ontology creates unsupported complexity.

**Result: PASS**

### CORE-04 — redundancy / merge-split

Living Referent does not duplicate Person, Asset, Subject, Resource, Place or Observation semantics.

Identity reconciliation cases were tested:

```text
two imported records -> same organism candidate
one presumed identity -> actually two organisms
replacement organism incorrectly treated as continuation
```

Correction must preserve prior material attribution/history.

**Result: PASS WITH HARDENING**

### CORE-05 — traceability

Need traces to concrete North-Star-aligned workflows where LifeOS must understand persistent real-life subjects over time rather than only store disconnected observations.

**Result: PASS**

### CORE-06 — independence

Living Referent exists independently of:

```text
name
owner
caregiver
location
Subject role
Resource role
Observation
Activity/Event
Content Artifact
provider record
```

**Result: PASS**

### CORE-07 — external benchmark

Targeted benchmark evidence showed mature adjacent systems commonly preserve identity of the individual living subject/specimen separately from classification vocabulary and care/history records.

External schemas remain evidence only and do not control LifeOS ontology.

**Result: PASS**

### CORE-08 — anti-pattern

Rejected anti-patterns:

```text
Pet as universal identity root
Animal/Plant inheritance explosion
LivingThing superclass over Person
Asset broadened for convenience
Subject wrapper identity
one identity per detected organism regardless of product need
provider ID as canonical identity
```

**Result: PASS**

### CORE-09 — correction / epistemic safety

Taxonomic/name/provider corrections do not silently rewrite identity. AI reconciliation/classification remains proposal/evidence-sensitive.

**Result: PASS WITH HARDENING**

### CORE-10 — scale / history

The model must support one long-lived individually tracked organism without forcing one record per organism in crops/populations where identity does not matter.

**Result: PASS WITH HARDENING**

### CORE-11 — simple / power user

Simple UI can expose natural profiles such as `Pet`, `Plant`, `Tree`, `Bonsai` while the kernel uses one bounded identity semantic. No generic ontology form is required.

**Result: PASS**

### CORE-12 — product value / complexity

One scoped referent removes a concrete semantic gap while avoiding multiple specialist roots.

**Result: PASS**

### CORE-13 — implementation pressure

No persistence representation is accepted here. A later logical model must preserve Living Referent identity distinctly from Person/Asset/Subject and from provider IDs.

**Result: PASS WITH HARDENING**

### CORE gate

```text
CORE-01  PASS
CORE-02  PASS WITH HARDENING
CORE-03  PASS
CORE-04  PASS WITH HARDENING
CORE-05  PASS
CORE-06  PASS
CORE-07  PASS
CORE-08  PASS
CORE-09  PASS WITH HARDENING
CORE-10  PASS WITH HARDENING
CORE-11  PASS
CORE-12  PASS
CORE-13  PASS WITH HARDENING

CORE
PASS WITH HARDENING
```

---

## 5. Mandatory chronology simulations

### Scenario A — companion animal continuity

```text
T0 Luna is tracked as one specific dog.
T1 weight observations accumulate.
T2 caregiver changes.
T3 owner changes.
T4 microchip number is corrected after import error.
T5 Luna moves home.
T6 veterinary Content Artifacts are attached/referenced.
T7 Luna dies.
T8 historical care timeline is consulted years later.
```

Required interpretation:

```text
same Living Referent throughout
rename/owner/caregiver/location/provider correction != new identity
death != historical deletion
```

**PASS**

### Scenario B — plant replacement and container continuity

```text
T0 Plant P1 lives in Pot A.
T1 observations/care history accumulate.
T2 P1 dies.
T3 new Plant P2 is placed in Pot A.
```

Required interpretation:

```text
P2 != P1
same Pot/Place/owner != same organism
```

**PASS WITH HARDENING**

### Scenario C — propagation

```text
T0 Plant P1 produces cutting C1.
T1 C1 is not independently tracked.
T2 later C1 becomes a separately managed specimen with its own history.
```

Required interpretation:

```text
no mandatory new referent at T1
new Living Referent at T2 when distinct identity materially matters
parent/source identity != propagated specimen identity
```

**PASS WITH HARDENING**

### Scenario D — bulk population

```text
10,000 crop plants
tracked by area/count/yield only
```

Required interpretation:

```text
no 10,000 Living Referents required
Quantity/Observation/Place/specialist aggregate semantics may suffice
```

**PASS**

---

## 6. Inverse reconstruction / necessity

Starting from existing kernel semantics, reconstruct whether every required fact can be expressed without Living Referent.

```text
Observation can say dog weight = 18.2 kg
BUT Subject role cannot create native dog identity.

Asset can preserve object identity
BUT accepted Asset excludes living animals/plants.

Person can preserve human identity
BUT must not absorb non-human organisms.
```

Therefore one missing native identity owner remains.

After adding Living Referent, reconstruct the same workflows without requiring any further primitive:

```text
identity                 Living Referent
aboutness                Subject role
measure/assertion        Observation
care work                Activity/Event/Routine/etc. as applicable
owner/holder             Ownership/Possession
care duty                Responsibility
current place            Place relation/context
planning resource role   Resource when truthful
content                  Content Artifact
visibility/governance    Visibility/Authority
history/correction       existing Version/Provenance/Reconciliation semantics
```

No additional required kernel concept survives.

**Result: PASS**

---

## 7. Multi-Actor MA-01..20 synthesis

The review replayed identity sharing, external/accountless Persons, multiple owners/caregivers, responsibility changes, selective disclosure, unequal Authority, private observations, AI access and historical revocation/correction.

Required invariants:

```text
one organism != one copy per actor
owner != caregiver != responsible actor
Ownership != Responsibility != Authority != Visibility
referent visibility != all facet visibility
seeing both endpoints != seeing their relation automatically
private care/history != universally shared state
AI source access != disclosure permission
caregiver change != referent replacement
```

No new actor/relationship primitive is required.

```text
MA-01..20
PASS / PASS WITH HARDENING

MULTI-ACTOR
PASS WITH HARDENING
```

---

## 8. XCON-01..06

```text
XCON-01 Identity
PASS WITH HARDENING
Living Referent is distinct from Person/Asset/Subject and from labels/IDs.

XCON-02 Authority
PASS
No authority semantics are inherited from ownership/care.

XCON-03 Current/history/material state
PASS WITH HARDENING
Current owner/location/life state does not rewrite historical identity/basis.

XCON-04 Relationships / Reasoning
PASS
Existing specific relation families compose without reopen.

XCON-05 Multi-Actor
PASS WITH HARDENING
Shared identity does not imply shared facets/source visibility.

XCON-06 Language
PASS WITH UPDATE
Animal/Plant/Pet remain bounded product/profile vocabulary; Living Referent becomes the kernel term.

XCON
PASS WITH HARDENING
```

---

## 9. Boundary matrix

```text
Living Referent != Person
Living Referent != Asset
Living Referent != Subject
Living Referent != Resource
Living Referent != Place
Living Referent != Content Artifact

name != identity
species/breed/cultivar != identity
provider/tag/microchip ID != canonical identity
owner != identity
caregiver/responsible actor != identity
current location != identity
```

No reopen is required for Ownership or Possession because their accepted definitions already target bounded referents/physical referents rather than Asset-only identity.

No reopen is required for Observation, Resource, Responsibility, Visibility, Authority, Place or Content Artifact; compatibility propagation is sufficient where needed.

---

## 10. LIV-01..34

```text
LIV-01  Living Referent is scoped native non-human living identity.
LIV-02  Individual identity must materially matter over time.
LIV-03  Living Referent != Person.
LIV-04  Living Referent != Asset.
LIV-05  Living Referent != Subject.
LIV-06  Living Referent may play Subject role.
LIV-07  Living Referent != Resource.
LIV-08  Living Referent may play Resource role where truthful.
LIV-09  Animal / Plant / Pet are bounded kinds/profiles, not kernel roots.
LIV-10  Species/breed/cultivar != individual identity.
LIV-11  Name != identity.
LIV-12  Provider ID / tag / microchip != canonical identity.
LIV-13  Ownership != identity.
LIV-14  Possession != identity.
LIV-15  Care Responsibility != identity.
LIV-16  Current Place != identity.
LIV-17  Observation about a Living Referent != its identity.
LIV-18  Activity concerning a Living Referent != its identity.
LIV-19  Content Artifact about a Living Referent != its identity.
LIV-20  Rename does not create a new referent.
LIV-21  Descriptive/taxonomic correction does not automatically create a new referent.
LIV-22  Death does not erase identity/history.
LIV-23  New organism/specimen != continuation merely because container/owner/location is the same.
LIV-24  Propagation/cutting creates a new referent only when distinct identity becomes materially tracked.
LIV-25  Bulk/fungible biological populations do not require one referent per organism.
LIV-26  Identity reconciliation preserves material history.
LIV-27  AI identification/classification != established truth.
LIV-28  AI identity match != canonical merge.
LIV-29  Shared referent != all related information shared.
LIV-30  Visibility of referent != visibility of all care/health/ownership/location/history facets.
LIV-31  Ownership != Responsibility != Authority != Visibility.
LIV-32  Veterinary/botanical specialist ontology is not imported into the general kernel.
LIV-33  Biological genealogy/propagation science remains specialist absent demonstrated product need.
LIV-34  No SQL/API/persistence shape is accepted here.
```

All 34 are REQUIRED canonical hardenings for this v0 closure.

---

## 11. Specialist boundaries

Not accepted as general-kernel semantics in this review:

```text
veterinary diagnosis/treatment ontology
clinical coding
animal pedigree/genetics
breeding
agricultural herd/flock management
crop inventory/population engine
botanical taxonomy engine
propagation genealogy engine
wildlife/ecological population model
biological lab specimen ontology
jurisdiction-specific animal/property law
```

These remain specialist domains unless concrete LifeOS product need demonstrates otherwise.

---

## 12. V3 verdict

```text
LIVING REFERENT v0

PASS WITH HARDENING

CORE
PASS WITH HARDENING

MA-01..20
PASS / PASS WITH HARDENING

MULTI-ACTOR
PASS WITH HARDENING

XCON
PASS WITH HARDENING

NEW NATIVE REFERENT
YES — Living Referent

UNIVERSAL LIVING ROOT
NO

ANIMAL ROOT
NO

PLANT ROOT
NO

SEMANTIC SAFE DEFERRED  0
SEMANTIC UNCLASSIFIED   0
SEMANTIC UNRESOLVED     0
STRUCTURAL REOPEN       0
```

This verdict closes the semantic review only after the approved propagation paths are written and independently fetched/read from remote. Until the dedicated closure continuation records successful post-write QA, Whole-Domain logical readiness remains on HOLD.

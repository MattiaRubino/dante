# Ownership / Possession / Custody v0 — Domain Validation Methodology v3

Status: **PASS WITH HARDENING**

This checkpoint validates the remaining Asset-adjacent ownership / possession / custody pressure without importing a universal property-law model or manufacturing concepts that LifeOS does not need.

## Candidate hypotheses

```text
H0
No canonical ownership/possession semantics; reconstruct from Asset,
Authority, Responsibility, Resource Allocation, location and generic links.

H1
Ownership and Possession are distinct specific contextual relation families.
Custody is a bounded compositional profile/vocabulary rather than a third
independent primitive/root.

H2
Ownership = Asset attribute / owner field.

H3
Ownership = Authority/control.

H4
Possession = Ownership.

H5
Possession = Resource Allocation or Actual use.

H6
Custody is a universal independent relation primitive/root.

H7
One generic Property/Control/Stewardship relation covers all three.
```

Result:

```text
H1 SURVIVES

H0 FAIL
H2 FAIL
H3 FAIL
H4 FAIL
H5 FAIL
H6 FAIL / OVERMODELED
H7 FAIL
```

## Accepted definitions

### Ownership

> **Ownership is the specific contextual relation through which an eligible owner is established as owner of a bounded referent within an applicable ownership context/basis, independently from native identity, possession, custody, responsibility, coordination stewardship, authority, visibility and actual use.**

`Owner` is a contextual role, not a native entity/root.

### Possession

> **Possession is the specific contextual relation through which an eligible possessor actually holds or physically possesses/controls a bounded physical referent within an applicable context, independently from ownership, location, allocation, use, responsibility, authority and custody.**

`Possessor` / `Holder` are contextual roles, not native entity/root identities.

### Custody

Custody does **not** survive as a third independent primitive/root in v0.

Canonical bounded composition:

```text
Possession / holding
+ applicable safeguarding / return Responsibility
+ applicable Authority / Agreement / policy basis where relevant
→ Custody profile / vocabulary
```

Custody is retained as useful domain language when the entrusted/safeguarding character matters, but the reviewed semantics do not justify a standalone universal Custody root.

## Canonical hardenings — OWN-01..38

```text
OWN-01  Ownership is a specific contextual relation family, not an Asset attribute or universal root.
OWN-02  Owner is a contextual role, not a native entity/root.
OWN-03  Ownership != native identity of the owned referent.
OWN-04  Ownership != Possession.
OWN-05  Ownership != Custody.
OWN-06  Ownership != Responsibility.
OWN-07  Ownership != Coordination Stewardship.
OWN-08  Ownership != Authority.
OWN-09  Ownership != Visibility.
OWN-10  Ownership != Membership / Contribution / Resource Allocation / Actual use.
OWN-11  Ownership change does not automatically change Asset identity.
OWN-12  Asset identity continuity does not automatically preserve Ownership.
OWN-13  Proposal / Request / Agreement / Decision do not universally establish Ownership by themselves.
OWN-14  Payment, handover, delivery or possession change do not universally establish Ownership transfer by themselves.
OWN-15  Ownership establishment/transfer basis remains contextual/specialist where required; v0 defines no universal conveyance state machine.
OWN-16  Current Ownership != historical Ownership where chronology matters.
OWN-17  Correction != silent overwrite of consequential Ownership history.
OWN-18  Conflicting Ownership assertions may coexist; no universal newest/provider/creator/manager/possessor/highest-confidence winner applies.
OWN-19  Unknown Ownership != established absence of Ownership.
OWN-20  Multiple owners do not automatically manufacture Collective identity.
OWN-21  Membership != Ownership; Collective Ownership does not imply personal Ownership by every member.
OWN-22  Member Ownership does not automatically establish Collective Ownership.
OWN-23  Co-ownership share/percentage and legal-capacity mechanics are not accepted by v0.
OWN-24  Possession is a distinct specific contextual relation family for actual physical holding/control.
OWN-25  Possessor / Holder are contextual roles, not native entity/root identities.
OWN-26  Possession != Ownership / Custody / Responsibility / Coordination Stewardship / Authority / Visibility.
OWN-27  Possession != Location; location alone does not establish possessor identity.
OWN-28  Possession != Resource eligibility / Resource Allocation / Schedule / Actual use universally.
OWN-29  Planned, assigned or allocated holding does not establish actual Possession.
OWN-30  Possession change does not automatically transfer Ownership; Ownership transfer does not require immediate Possession change universally.
OWN-31  Current Possession != historical Possession where consequential; correction remains non-destructive.
OWN-32  No current Evidence != established non-possession, and conflicting possession assertions may remain unresolved.
OWN-33  Possession is not assumed exclusive; several possessors do not create Collective identity automatically.
OWN-34  Custody is bounded profile/vocabulary, not an independent universal primitive/root in v0.
OWN-35  Possession alone != Custody; Custody requires the applicable entrusted/safeguarding Responsibility and governance basis where relevant.
OWN-36  Custodian != Owner / Possessor / Steward / Responsible Actor automatically; the roles may coincide contextually.
OWN-37  Legal title, jurisdiction-specific property rights, liens/encumbrances, beneficial ownership, IP, forensic chain-of-custody and specialist financial ownership remain outside the kernel decision.
OWN-38  No universal Property/Control/Stewardship wrapper, ownership engine, custody engine, SQL table, API shape or persistence model is accepted by this semantic review.
```

## CORE gate

```text
CORE-01 Workflow inversion             PASS
CORE-02 Deep chronology                PASS WITH HARDENING
CORE-03 Adversarial reductio           PASS WITH HARDENING
CORE-04 Redundancy / merge-split       PASS WITH HARDENING
CORE-05 Traceability                   PASS
CORE-06 Independence                   PASS WITH HARDENING
CORE-07 External benchmark             PASS
CORE-08 Anti-pattern                   PASS WITH HARDENING
CORE-09 Correction / epistemic safety  PASS WITH HARDENING
CORE-10 Scale / history                PASS WITH HARDENING
CORE-11 Simple / power user            PASS
CORE-12 Product value / complexity     PASS WITH HARDENING
CORE-13 Implementation pressure        PASS WITH HARDENING

CORE GATE
PASS WITH HARDENING
```

## Deep chronology

```text
T0  Asset A exists with stable native identity.
T1  Anna is established as owner under the applicable context.
T2  Anna lends A to Luca.
    → Ownership may remain Anna.
    → Possession may become Luca.
T3  Luca is also responsible for safeguarding/return.
    → Custody vocabulary may apply when the entrusted profile is relevant.
T4  A is allocated to Sara for an Activity tomorrow.
    → Allocation does not make Sara current possessor.
T5  Sara uses A while Luca remains the accountable custodian in the wider context.
    → use, possession and custody need not collapse.
T6  A is returned to Anna.
    → Possession changes; Ownership need not.
T7  Anna agrees to sell A and payment occurs.
    → neither Agreement nor payment alone universally defines transfer timing.
T8  applicable ownership basis establishes transfer to Marco.
    → Asset identity remains A unless its own identity invariants changed.
T9  historical ownership/possession/custody basis remains reconstructible.
T10 later evidence corrects one historical possession assertion.
    → correction does not silently rewrite other truthful history.
T11 competing ownership claims arise.
    → conflict may remain unresolved pending applicable Reconciliation.
```

This chronology fails if Ownership is an Asset field, if Possession is Allocation/use, or if Custody is treated as a synonym for any one accepted relation.

## Adversarial reductio

```text
Ownership = Asset attribute                  FAIL
Ownership = Authority                        FAIL
Ownership = Responsibility                   FAIL
Ownership = Possession                       FAIL
Possession = Location                        FAIL
Possession = Resource Allocation             FAIL
Possession = Actual use                      FAIL
Custody = Ownership                          FAIL
Custody = Possession alone                   FAIL
Custody independent universal primitive      FAIL / OVERMODELED
generic Property/Control relation            FAIL
specific Ownership relation                  SURVIVES
specific Possession relation                 SURVIVES
bounded compositional Custody profile        SURVIVES
```

## Multi-Actor gate

```text
MA-01 Identity/account independence       PASS WITH HARDENING
MA-02 Shared fact / actor overlay         PASS WITH HARDENING
MA-03 Responsibility                     PASS WITH HARDENING
MA-04 Coordination Stewardship            PASS WITH HARDENING
MA-05 Common ground                       PASS
MA-06 Authority                           PASS WITH HARDENING
MA-07 Selective disclosure               PASS WITH HARDENING
MA-08 Inference privacy                  PASS WITH HARDENING
MA-09 Partial adoption                   PASS
MA-10 Representation/on-behalf-of        PASS WITH HARDENING
MA-11 Lifecycle/revocation               PASS WITH HARDENING
MA-12 Conflict/adversarial               PASS WITH HARDENING
MA-13 Unequal power                      PASS WITH HARDENING
MA-14 Resource/capacity                  PASS WITH HARDENING
MA-15 Burden distribution                PASS WITH HARDENING
MA-16 Progressive disclosure             PASS
MA-17 AI / automation                    PASS WITH HARDENING
MA-18 Specialist systems                PASS WITH HARDENING
MA-19 Primitive redundancy              PASS WITH HARDENING
MA-20 Actor-scoped attribution          PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
```

## Cross-cluster gate

```text
XCON-01 Identity                         PASS WITH HARDENING
XCON-02 Authority                        PASS WITH HARDENING
XCON-03 current/history/material state   PASS WITH HARDENING
XCON-04 Relationships / Reasoning        PASS WITH HARDENING
XCON-05 Multi-Actor                      PASS WITH HARDENING
XCON-06 Language                         PASS WITH UPDATE

XCON GATE
PASS WITH HARDENING
```

## Adjacent Dependency Sweep

Resolved by this review:

```text
Asset ↔ Ownership identity
Asset ↔ Possession identity
Ownership ↔ Possession
Ownership ↔ Responsibility
Ownership ↔ Coordination Stewardship
Ownership ↔ Authority / Visibility
Ownership ↔ Membership / Collective
Ownership ↔ Resource / Allocation / use
Possession ↔ Location
Possession ↔ Resource Allocation
Possession ↔ Actual use
Possession ↔ Responsibility / Authority
Custody ↔ Ownership
Custody ↔ Possession
Custody ↔ Responsibility
Custody ↔ Coordination Stewardship
Custody ↔ Authority / Agreement / policy basis
```

### SAFE DEFERRED — ownership establishment / transfer specialization

Unresolved: exact reusable transfer/establishment lifecycle beyond the accepted semantic relation.

Why safe: Ownership identity does not depend on one universal transfer state machine.

Owner: future property/transaction specialist review.

Reopen trigger: ordinary LifeOS workflows require a reusable ownership-transfer lifecycle whose material states cannot be represented by Ownership plus accepted Proposal/Request/Agreement/Decision/Actual/Evidence semantics without loss.

Tests: CORE-02/03/04/06/12/13, MA-06/11/12/13, XCON-02/03/04.

### SAFE DEFERRED — co-ownership shares / legal capacity

Unresolved: percentage shares, classes of ownership, Collective/legal-person capacity.

Why safe: v0 supports multiple truthful owners without inventing quantitative/legal mechanics.

Owner: future ownership + organization/legal specialist review.

Reopen trigger: real LifeOS workflows require actionable shares/capacity rules rather than simple multiple-owner attribution.

Tests: CORE-03/04/07/12, MA-01/06/13/18/19/20, XCON-01/02/04/05.

### SAFE DEFERRED — legal property-right taxonomy

Unresolved: title, beneficial ownership, liens, encumbrances, usufruct, security interests, jurisdiction-specific rights.

Why safe: external legal taxonomies are specialist evidence, not LifeOS kernel authority.

Owner: legal/property specialist review.

Reopen trigger: a concrete LifeOS workflow must reason or act on one of these rights and generic Ownership plus specialist adapter semantics is insufficient.

Tests: CORE-03/04/07/08/12, MA-06/13/18/19, XCON-02/04/06.

### SAFE DEFERRED — lending / rental / bailment workflow

Unresolved: reusable loan/rental/bailment lifecycle.

Why safe: Ownership, Possession, Agreement, Responsibility, Schedule and Actual already preserve the essential non-collapse boundary.

Owner: future product/domain workflow review.

Reopen trigger: repeated LifeOS workflows require a durable shared lifecycle with state/history not truthfully reconstructible from accepted concepts.

Tests: CORE-02/03/04/12/13, MA-03/05/06/11/13, XCON-03/04/05.

### SAFE DEFERRED — forensic / evidentiary chain of custody

Unresolved: specialist chain-of-custody event/evidence requirements.

Why safe: general Custody vocabulary must not import forensic evidentiary obligations.

Owner: specialist Evidence/compliance review.

Reopen trigger: LifeOS must support evidence-handling/compliance workflows where custody transitions themselves carry evidentiary validity requirements.

Tests: CORE-02/03/04/07/08/09, MA-06/12/13/18, XCON-03/04/05.

### SAFE DEFERRED — IP / digital / financial ownership

Unresolved: non-physical specialist ownership semantics.

Why safe: they may have distinct invariants from physical Asset-adjacent ownership and must not be assumed equivalent.

Owner: relevant specialist-domain review.

Reopen trigger: a concrete LifeOS workflow requires these forms of ownership and the accepted generic relation loses material semantics.

Tests: CORE-03/04/06/07/12, MA-06/13/18/19, XCON-01/02/04/06.

### SAFE DEFERRED — possession exclusivity / shared control

Unresolved: exclusivity, degrees of control and simultaneous possession mechanics.

Why safe: v0 does not require possession to be exclusive and can retain multiple assertions.

Owner: future possession/product/specialist review.

Reopen trigger: ordinary workflows require enforceable/queryable exclusivity or control-degree semantics beyond contextual possession.

Tests: CORE-03/04/06/12, MA-12/13/19/20, XCON-03/04/05.

### SAFE DEFERRED — persistence / API

Unresolved: direct vs qualified relation persistence, intervals, history, indexes and API payloads.

Owner: logical/physical implementation stages.

Reopen trigger: after semantic scope is accepted and persistence modeling begins.

Tests: CORE-05/10/13, XCON-03/04.

## External benchmark evidence

Targeted external evidence was used only as benchmark evidence, never ontology authority. The review considered systems that distinguish owning party from possessing party and specialist chain-of-custody practices as evidence that these concerns can diverge materially. Provider/legal schemas are not imported into the LifeOS kernel.

## Final verdict

```text
OWNERSHIP / POSSESSION / CUSTODY v0

PASS WITH HARDENING

Ownership
✅ canonical specific contextual relation family
✅ Owner contextual role
❌ Asset identity / Authority / Responsibility / Possession

Possession
✅ canonical specific contextual relation family
✅ Possessor/Holder contextual role
❌ Ownership / Location / Allocation / Actual use

Custody
✅ bounded canonical profile / vocabulary
✅ composition of holding + applicable safeguarding Responsibility + governance basis where relevant
❌ independent universal primitive/root

CORE  PASS WITH HARDENING
MA    PASS WITH HARDENING
XCON  PASS WITH HARDENING
ADS   COMPLETE

STRUCTURAL REOPEN  0
UNCLASSIFIED       0
```

This checkpoint is not `CLOSED` until the exact pre-authorized propagation scope passes remote post-write QA and the closure continuation is written.

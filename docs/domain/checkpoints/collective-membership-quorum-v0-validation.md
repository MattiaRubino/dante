# Collective / Membership / Quorum v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — propagation pending final QA  
**Validated:** 2026-08-16  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Relationships / Reasoning  
**Branch:** `feature/domain-model`

## 1. Scope

Candidate family:

```text
Collective
Membership
Quorum
```

Questions under review:

1. Does LifeOS need a native referent for a plurality whose identity/state/history/agency matters independently from the exact current member set?
2. Is Membership a distinct specific relation family?
3. Does Quorum justify an independent primitive/root, or is it bounded eligibility + Criterion/Evaluation + governance/policy semantics?
4. Can these semantics integrate without creating universal Group/Organization/Party/Member/Quorum roots?

## 2. Candidate hypotheses

```text
H0  no canonical collective semantics; sets/labels only
H1  universal Group / Organization primitive/root
H2  scoped native Collective referent + specific Membership relation
H3  Membership = Participation / Authority / account membership
H4  independent universal Quorum / Vote / Ballot primitive family
H5  Quorum = bounded eligibility + Criterion/Evaluation + applicable governance/policy semantics
```

Result:

```text
Collective  → H2 accepted
Membership  → H2 accepted
Quorum      → H5 accepted
```

H0 fails true collective identity/history scenarios. H1 over-generalizes arbitrary pluralities. H3 collapses independent relations. H4 manufactures an unnecessary universal decision/voting engine.

## 3. Accepted definitions

### Collective

> **A Collective is a scoped persistent native referent representing a materially meaningful plurality as one domain referent where that plurality has identity, state, history or agency that cannot be truthfully reduced to the current set of individual members.**

Classification:

```text
SCOPED NATIVE REFERENT
NOT universal Group/Organization root
```

### Membership

> **Membership is the specific contextual relation through which an eligible native referent belongs to a Collective within a defined scope and material state, independently from Participation, Responsibility, Coordination Stewardship, Authority, Visibility, Agreement, Consent, Account/security membership and actual activity.**

Classification:

```text
SPECIFIC CONTEXTUAL RELATION FAMILY / CAPABILITY
NOT native entity/root
```

### Quorum

> **Quorum is bounded governance/evaluation vocabulary for assessing whether the materially applicable eligible-set and threshold conditions required for a collective process are sufficiently satisfied for the relevant purpose and state. Quorum uses eligibility plus Criterion/Evaluation semantics and does not itself create a Decision, Agreement, Consent, Authority or universal truth.**

Classification:

```text
CANONICAL BOUNDED VOCABULARY / PROFILE
OVER eligibility + Criterion/Evaluation + governance/policy
NO NEW PRIMITIVE
```

## 4. Canonical shape

```text
native referents
      │
      │ Membership
      ↓
  Collective
      │
      ├─ may play Actor / Subject / other contextual roles
      │
      └─ applicable collective process
             +
         eligible set
             +
         threshold Criterion
             ↓
          Evaluation
             ↓
        quorum assessment
             ↓
   applicable governance may establish
        Decision / other effect
```

Required non-collapse:

```text
Collective != current member set
Collective != Actor
Collective != Subject

Membership != Participation
Membership != Responsibility
Membership != Coordination Stewardship
Membership != Authority
Membership != Visibility
Membership != Agreement / Consent
Membership != account/security membership

quorum satisfied != Decision
quorum satisfied != Agreement
quorum satisfied != Consent
quorum satisfied != Authority
quorum satisfied != unanimous assent
```

## 5. CORE Semantic Validation Gate

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

### CORE-01 workflow inversion

Representative workflows survive without one universal Group root:

- persistent household/team/committee-like referent;
- current/historical membership;
- collective subject/agency where truthful;
- member participation independent from membership;
- collective Responsibility or Stewardship where truthful;
- agreement involving a true Collective versus several independent parties;
- threshold-based collective decision formation;
- membership change after prior decision;
- split/merge/replacement history.

### CORE-02 deep chronology

```text
T0  Collective C created/recognized
T1  Anna joins C
T2  Luca joins C
T3  Sara joins C
T4  policy P1 defines eligible members for decision context D
T5  Criterion Q1 = at least 2 of 3 eligible responses
T6  Anna responds yes
T7  Luca responds yes
T8  Evaluation under Q1/P1 = threshold satisfied
T9  applicable governance establishes Collective Decision D1
T10 Sara later leaves C
T11 D1 remains historically tied to eligible/material state at T8/T9
T12 Marco joins C
T13 a later question uses new eligible set/material state
T14 C may remain same Collective if identity invariants remain satisfied
T15 later material split produces C2/C3 if continuity as C would be false
```

Required hardenings:

```text
current Membership change
!= rewrite prior eligible set

quorum evaluation under S1/P1
!= automatically valid under S2/P2

Collective Decision
!= every member's personal stance

split/merge/replacement
!= automatic carry-forward of every prior relation/state
```

### CORE-03 reductio

```text
Collective = current member set              FAIL
Collective = arbitrary set/query/cohort      FAIL
Collective = Actor                           FAIL
Collective = Account/security group          FAIL
Membership = Participation                   FAIL
Membership = Authority                       FAIL
Membership = Agreement                       FAIL
Member as native wrapper entity              FAIL
Quorum as universal primitive/root           FAIL
Quorum = Decision                            FAIL
Quorum = unanimous Agreement                 FAIL
Collective + Membership + scoped Quorum use  SURVIVES
```

### CORE-04 redundancy

The accepted decomposition is minimal:

```text
Collective
owns plurality referent identity

Membership
owns belonging relation

Criterion/Evaluation
owns threshold assessment

Decision / Agreement / Authority
own their existing consequence/governance meanings
```

No accepted concept can absorb all three without semantic loss.

### CORE-06 independence

- Collective can exist with zero current members where the real-world referent truthfully persists.
- a referent can exist without Membership in any Collective.
- Membership can matter even when no current event/Participation exists.
- a quorum evaluation may be absent even though Collective and Membership exist.
- a collective process can remain unresolved despite threshold assessment if additional Decision/Authority semantics are required.

### CORE-08 anti-patterns

Rejected:

```text
one universal groups table as ontology authority
one Member wrapper identity for every relation
security/ACL group == Collective
attendee list == Collective
saved query == Collective
current member set == Collective identity
quorum boolean as permanent universal truth
majority result == Decision automatically
member action == Collective action automatically
```

### CORE-09 epistemic safety

```text
unknown membership != non-member
no response != dissent
threshold not yet provable != failed forever
member majority behavior != collective decision automatically
```

Corrections preserve material historical basis. Conflicting membership/eligibility assertions may remain unresolved pending applicable Authority/Decision/Reconciliation.

## 6. Accepted hardenings — COL-01..32

```text
COL-01  Collective is a scoped native referent for materially meaningful plurality.
COL-02  Collective is not a universal Group/Organization/Party root.
COL-03  Collective identity != exact current member set.
COL-04  ordinary join/leave does not automatically create new Collective identity.
COL-05  material split/merge/replacement may require identity change.
COL-06  no universal Collective continuity rule is accepted.
COL-07  arbitrary sets/queries/cohorts/audiences do not create Collective identity.
COL-08  Collective may play Actor role; Collective != Actor.
COL-09  member action does not automatically establish Collective action.
COL-10  Collective may play Subject role; collective fact != every member fact.
COL-11  Participation/Responsibility/Stewardship do not manufacture Collective identity.
COL-12  Agreement party set does not manufacture Collective identity.
COL-13  Membership grants neither Authority nor Visibility.
COL-14  Collective Decision does not rewrite individual member stance.
COL-15  Quorum evaluation is not part of Collective identity.
COL-16  consequential Collective identity/history remains reconstructible where needed.
COL-17  Membership is a specific contextual relation family, not native entity/root.
COL-18  Member is a contextual role, not wrapper identity.
COL-19  Membership preserves native identities on both ends.
COL-20  Membership != Participation/Responsibility/Stewardship/performer.
COL-21  Membership != Authority/Visibility.
COL-22  Membership != Agreement/Consent/Decision.
COL-23  Membership != Account/security-group membership by default.
COL-24  consequential Membership history remains reconstructible.
COL-25  current member set is not universal quorum eligibility.
COL-26  M:N/cardinality/row ID does not manufacture a primitive.
COL-27  Quorum is bounded eligibility/threshold evaluation vocabulary, not primitive/root.
COL-28  quorum assessment must bind to materially applicable eligible-set/policy/Criterion state where consequential.
COL-29  quorum satisfied != Decision/Agreement/Consent/Authority.
COL-30  material eligibility/policy/Criterion change does not silently inherit prior quorum assessment.
COL-31  no response/unknown eligibility does not fabricate support, opposition or failure.
COL-32  AI may infer/propose eligibility/evaluation but does not fabricate Membership, Collective agency, human assent or Authority.
```

## 7. Multi-Actor Compatibility Gate

```text
MA-01 Identity/account independence       PASS WITH HARDENING
MA-02 Shared fact / actor overlay         PASS WITH HARDENING
MA-03 Responsibility                     PASS WITH HARDENING
MA-04 Stewardship                        PASS WITH HARDENING
MA-05 Common ground                      PASS WITH HARDENING
MA-06 Authority                          PASS WITH HARDENING
MA-07 Selective disclosure               PASS WITH HARDENING
MA-08 Inference privacy                  PASS WITH HARDENING
MA-09 External/accountless member        PASS
MA-10 Representation/on-behalf-of        PASS WITH HARDENING
MA-11 Lifecycle/revocation               PASS WITH HARDENING
MA-12 Conflict                           PASS WITH HARDENING
MA-13 Unequal power                      PASS WITH HARDENING
MA-14 Resource/capacity                  PASS
MA-15 Coordination burden                PASS WITH HARDENING
MA-16 Progressive formality              PASS
MA-17 AI                                 PASS WITH HARDENING
MA-18 Specialist systems                 PASS WITH HARDENING
MA-19 Primitive redundancy               PASS WITH HARDENING
MA-20 Actor-scoped attribution           PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING
```

Key results:

```text
member != Account holder
member != Authority holder
member != participant
member != responsible Actor
member != Steward
```

A Collective may itself bear Actor/Subject/Responsibility/Stewardship semantics where truthful, while several individual holders do not automatically form a Collective.

Privacy:

```text
private Membership detail
→ bounded authorized consequence/result
```

does not require universal disclosure of all membership or eligibility facts.

Collective decision result visibility, member stance visibility and rationale/Evidence visibility remain separately governed.

External/accountless Persons may be members. No synthetic Account is required.

## 8. Cross-Concept Consistency Gate

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

### Identity

Collective adds a native referent category only where plurality identity is independently material. It does not replace Person/Asset/Account or create Subject/Actor wrapper roots.

### Relationships

Membership follows the existing rule:

```text
specific truthful relation
> generic Relationship wrapper
```

Direct relation is preferred when semantically complete; qualified relation when relation state/history/context materially matters.

### Current/history

```text
current members != historical members
current quorum eligibility != historical eligibility
correction != silent overwrite
material change != automatic carry-forward
```

## 9. Adjacent Dependency Sweep

### RESOLVED

```text
true Collective referent vs several Subjects       RESOLVED
Collective vs Actor                                 RESOLVED
Membership vs Participation                         RESOLVED
Membership vs Responsibility                        RESOLVED
Membership vs Coordination Stewardship              RESOLVED
Membership vs Authority / Visibility                RESOLVED
Membership vs Agreement / Consent                   RESOLVED
Collective Agreement party vs party set             RESOLVED
Collective Decision vs member stance                RESOLVED
Collective Decision / quorum threshold core         RESOLVED
Quorum vs Criterion/Evaluation                      RESOLVED
Quorum vs Decision/Authority/Agreement               RESOLVED
```

### SAFE DEFERRED

1. **Organization / legal entity**
   - Why safe: Collective handles generic plurality identity without claiming legal personality.
   - Owner: later identity/specialist domain review.
   - Trigger: ordinary LifeOS workflows require legal/entity lifecycle/registration/capacity semantics independently.
   - Tests: CORE-03/04/06/12, MA-06/13/18/19, XCON-01/02/04.

2. **Collective/joint Responsibility among several distinct Actors**
   - Why safe: true Collective may bear Responsibility, but multiple individual Responsible Actors do not automatically become a Collective.
   - Owner: Responsibility relation review if product needs joint internal allocation semantics.
   - Trigger: recurring workflows require material joint-accountability state not expressible as one Collective bearer or several bounded Responsibility relations.
   - Tests: CORE-03/04/12, MA-03/13/15/19, XCON-04/05.

3. **Collective/joint Coordination Stewardship among several distinct Actors**
   - Same distinction: Collective Stewardship is now representable; joint Stewardship among distinct Actors remains separate.
   - Trigger: coordination burden requires shared-state semantics beyond multiple scoped Stewardship relations.
   - Tests: CORE-03/04/12, MA-04/15/19, XCON-04/05.

4. **Voting / ballot / proxy / delegated-vote mechanics**
   - Why safe: quorum threshold does not require a voting-system ontology.
   - Owner: specialist collective-governance review.
   - Trigger: ordinary LifeOS flows need durable vote/ballot/proxy lifecycle beyond response/Evidence/Evaluation/Decision semantics.
   - Tests: CORE-03/04/07/12/13, MA-05/06/10/13/17/18, XCON-02/04/05.

5. **Membership facets / admission flows**
   - Why safe: Membership relation and Proposal/Request/Decision/Agreement boundaries are sufficient now.
   - Trigger: reusable admission/application lifecycle cannot be represented without a stronger concept.

6. **Physical persistence/security mapping**
   - Owner: logical/physical/security model.
   - No semantic primitive implied.

## 10. Adversarial scenario log

```text
Household persists while one adult moves out
→ Collective may remain same; Membership changes

Ad-hoc dinner attendees
→ no Collective required

Saved query: all coworkers in Rome
→ cohort/query, not Collective

Committee member joins meeting
→ Membership != Participation

Committee member can read one agenda
→ Membership != universal Visibility

Manager is member
→ Membership != Authority

2-of-3 threshold met
→ quorum assessment, not Decision by itself

all members agree personally
→ may support Agreement/Decision but does not bypass owning semantics

one member acts without mandate
→ member action != Collective action automatically

Collective itself assigned Responsibility
→ valid where true bearer is Collective

three individuals jointly responsible
→ does not manufacture Collective; joint Responsibility remains separately reviewable

membership corrected after old vote
→ current assessment may change, historical basis remains reconstructible
```

## 11. External benchmark classification

External standards/products are evidence only.

Useful recurring patterns were classified as:

```text
BORROW  separation of group identity from membership records
BORROW  eligibility/threshold evaluation distinct from final governance effect
ADAPT   membership lifecycle/history where material
ADAPT   collective actor/subject possibility without universal party superclass
REJECT  provider ACL/security-group schema as ontology authority
REJECT  universal Organization/Group/Party root from benchmark convenience
REJECT  generic voting-engine schema as kernel authority
```

## 12. ADS status

```text
Collective ↔ current member set          RESOLVED
Collective ↔ Actor                       RESOLVED
Collective ↔ Subject                     RESOLVED
Collective ↔ Agreement party set         RESOLVED
Collective ↔ Decision                    RESOLVED
Membership ↔ Participation               RESOLVED
Membership ↔ Responsibility              RESOLVED
Membership ↔ Stewardship                 RESOLVED
Membership ↔ Authority / Visibility      RESOLVED
Membership ↔ Agreement / Consent         RESOLVED
Membership ↔ account/security group      RESOLVED
Quorum ↔ Criterion/Evaluation            RESOLVED
Quorum ↔ Decision                        RESOLVED
Quorum ↔ Agreement / Consent             RESOLVED
Quorum ↔ Authority                       RESOLVED

ADS COMPLETE
UNCLASSIFIED 0
REOPEN       0
```

## 13. Verdict

```text
COLLECTIVE / MEMBERSHIP / QUORUM v0

PASS WITH HARDENING

Collective
SCOPED NATIVE REFERENT

Membership
SPECIFIC CONTEXTUAL RELATION FAMILY / CAPABILITY
NO NATIVE ENTITY/ROOT

Quorum
CANONICAL BOUNDED VOCABULARY / PROFILE
OVER ELIGIBILITY + CRITERION/EVALUATION + GOVERNANCE/POLICY
NO NEW PRIMITIVE

CORE  PASS WITH HARDENING
MA    PASS WITH HARDENING
XCON  PASS WITH HARDENING
ADS   COMPLETE

REOPEN       0
UNCLASSIFIED 0
```

Final repository state must not be called CLOSED until the approved propagation set passes remote post-write QA and the pre-authorized closure continuation is written and verified.

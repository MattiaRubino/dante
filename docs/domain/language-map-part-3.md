<!-- LIFEOS-CANONICAL-SPLIT document="language-map.md" part="3" total="5" -->
> **Canonical document split — Part 3 of 5.** Parts 1–5 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](language-map.md) · [Part 2](language-map-part-2.md) · **Part 3** · [Part 4](language-map-part-4.md) · [Part 5](language-map-part-5.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
## Principal

**Status:** DEFERRED TECHNICAL/AUTHORITY CONCEPT

Authenticated/authorized security identity semantics remain open.

```text
Principal != Person
Principal != Actor
Principal != Account by default
```

## Participant / Participation

**Status:** CANONICAL SPECIFIC SEMANTIC RELATION FAMILY  
**Source:** `concepts/participation.md`  
**Validation:** `checkpoints/participation-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who is expected/intended to be involved, or who actually participated, in this bounded shared occurrence/interaction?  
**UI exposure:** CONTEXTUAL; Going / Maybe / Can't go / Attended / participant list where useful

Participant is a contextual role over native identity. Participation contains distinct intended/response and Actual involvement semantics; it is not a Person/Actor/Account subtype or universal membership root.

```text
Participant != Person identity subtype
Participation != Responsibility
Participation != Performer
Participation != Resource
Participation != Organizer/requester
Participation != Authority
Participation != Visibility
Participation != Session
shared Event Actual != identical actor-specific Actual Participation

Invitation != Acceptance
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
```

A response Actor/Account/Principal may differ from the participant whose involvement is at stake. Provider attendance telemetry remains evidence/provenance until applicable reconciliation semantics establish current Participation truth.

## Responsibility

**Status:** CANONICAL SPECIFIC SEMANTIC RELATION FAMILY  
**Source:** `concepts/responsibility.md`  
**Validation:** `checkpoints/responsibility-v0-validation.md` — PASS WITH HARDENING  
**Question:** Who is accountable for ensuring this bounded commitment is appropriately handled?  
**UI exposure:** CONTEXTUAL; often `Responsible`, `Assigned to`, natural person/role label

```text
Responsibility != Actor identity/category
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Resource
Responsibility != Authority
Responsibility != Visibility
Responsibility != ownership/custody
Responsibility != coordination Stewardship
unknown holder != explicitly open/unassigned
```

Simple cases may use a direct specific `responsible_for` relation. Rich/open/transfer/history cases may require a specific qualified Responsibility context. Qualified structure does not automatically imply independent entity identity.

## Assignment

**Status:** CANONICAL OPERATION SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Assignment establishes/changes a **specific named role**. `Assignment` without the role is semantically incomplete.

```text
assign Responsibility
assign expected performer
assign reviewer
```

Whether Assignment immediately makes the role effective depends on policy/Authority/Acceptance semantics.

## Claim

**Status:** CANONICAL OPERATION SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Self-initiated attempt/action to acquire a specific role. Whether the role becomes effective immediately is policy-dependent.

Do not confuse **Responsibility Claim** with a Resource **Capacity Claim / Reservation** merely because the same English word is used.

## Hand-off

**Status:** CANONICAL TRANSFER-WORKFLOW SEMANTICS — NOT STANDALONE UNIVERSAL PRIMITIVE

Hand-off transfers/proposes transfer of a specific named role. A request does not universally establish effective transfer.

```text
hand-off request != effective Responsibility transfer by default
```

## Stewardship / Coordination Responsibility

**Status:** DISTINCT SEMANTIC DIMENSION — STANDALONE PRIMITIVE SAFE DEFERRED

Execution Responsibility can move while anticipation, reminding, monitoring and repair burden remain elsewhere.

```text
Responsibility != coordination Stewardship
Assignment != Stewardship transfer
```

## Performer

**Status:** SPECIFIC ACTOR ROLE — exact logical representation deferred

Who actually performed work; not automatically requester/responsible actor/planned expected performer. Performer is a specific Actor role, not Actor, Participant or Resource identity.

## Subject

**Status:** CANONICAL SEMANTIC ROLE  
**See:** `concepts/subject.md`

Who/what a descriptive record primarily concerns. The native referent retains its identity; Subject is not an entity/root.

## Asset

**Status:** CANONICAL NATIVE ENTITY — CURRENT SCOPED BASELINE  
**See:** `concepts/asset.md`

One individually tracked non-human physical object whose identity/history materially matter. Asset may play Subject or Resource roles, but ownership, holder, stewardship, Authority and Visibility are separate. The exact noun `Asset` is not semantically mandatory.

## Resource

**Status:** CANONICAL SEMANTIC PLANNING / EXECUTION ROLE-CAPABILITY  
**See:** `concepts/resource.md`

Operational eligibility/capacity of an independently meaningful provider to satisfy an execution Requirement.

```text
Resource entity/root = rejected
Person may play Resource role
Asset may play Resource role
Actor != Resource
Subject != Resource
Asset != Resource
Resource != Requirement
Resource != Allocation
Resource != Reservation
Resource != actual use
Resource != Responsibility/Performer/Participation
```

Resource may also apply to supplies/pools without manufacturing identity for them. Resource reservation/candidacy does not establish Participation.

## Owner / Governor / Steward

**Status:** DEFERRED RELATIONSHIP/AUTHORITY SEMANTICS

Do not use as synonyms for creator, Account holder, participant, viewer, responsible actor, performer, Person, Subject, Resource or Asset identity.

## Authority

**Status:** DEFERRED — STRONG CROSS-CUTTING DIMENSION

Who/what may establish, approve, change or override canonical state in context.

```text
Authority != Visibility
Authority != Confirmation
Authority != Provenance/source
Authority != Subject
Authority != Actor
Authority != Resource
Authority != Responsibility
Authority != Participation
Authority != Account
Authority != Asset ownership by default
```

## Visibility / Access

**Status:** DEFERRED

What an Actor/Principal/Account context may inspect/receive/use. Current access and historical Person/Actor/Asset/Responsibility/Participation attribution are distinct. Being Subject, Resource candidate, participant, owner or responsible actor does not automatically grant visibility.

## Acknowledgement

**Status:** PROVISIONAL / DEFERRED

Grounding/receipt/recognition semantics where consequence requires them.

```text
Acknowledgement != Confirmation
Acknowledgement != Acceptance
Acknowledgement != Participation response by default
```

## Acceptance / Agreement

**Status:** PROVISIONAL / DEFERRED

Willingness/proposal/responsibility/participation semantics.

```text
Acceptance != Confirmation
Acceptance != Actual
Assignment != Acceptance by default
Claim != Acceptance by default
hand-off request != Acceptance by default
Participation response may express contextual willingness without defining a universal Acceptance primitive
```

---

# 10. Deferred neighboring semantics

## Verification

**Status:** DEFERRED

Process/basis used to check a claim or record.

```text
Verification != Confirmation
Verification != Provenance
```

## Longitudinal query / aggregation / saved-view implementation

**Status:** PRODUCT + LOGICAL/PHYSICAL MODEL DEFERRED

The required product capability is validated, but exact query DSL, aggregate materialization, cache/history policy and saved-view persistence are implementation/product concerns rather than a kernel `Register` primitive.

## Account / Principal / credential security model

**Status:** DEFERRED LOGICAL / SECURITY MODEL

The conceptual boundary is fixed:

```text
Person != Account
Actor != Account
Account != Principal by default
```

Exact login-provider identities, credentials, account linking, service principals, delegation and authentication/authorization representation remain open.

## Resource Requirement / Allocation / Reservation

**Status:** SAFE DEFERRED — RELATIONSHIPS / PLANNING LOGICAL MODEL

Resource v0 fixes the separation:

```text
Requirement
what is needed
        ↓
Candidate
what could satisfy it
        ↓
Allocation
what is selected
        ↓
Reservation / Capacity Claim
what capacity is held
        ↓
Actual use / consumption
what was really used
```

The exact identity/cardinality/persistence of these structures remains deferred. None implies Responsibility or Participation.

## Asset scope / managed-referent taxonomy

**Status:** RESOLVED AT CURRENT CLUSTER-4 BASELINE — REOPENABLE WITH STRONGER EVIDENCE

The terminology-neutral review was completed across managed/tracked-referent product families.

Current result:

```text
universal ManagedObject root  REJECTED
physical-object identity      RETAINED
exact noun `Asset`            NON-SEMANTIC / reopenable
```

Future Place/Property, living, Document, FinancialAccount, and service workflows remain independently SAFE DEFERRED; they do not become primitives until concrete evidence justifies them.

## Version

**Status:** DEFERRED — RELATIONSHIPS/REASONING REVIEW

Material version identity/history must later integrate with Confirmation, Evidence, Provenance, Responsibility/Participation history and Subject/Person/Asset attribution correction without replacing them.

## Decision

**Status:** DEFERRED — RELATIONSHIPS/REASONING REVIEW

Decision rationale/authority is distinct from Provenance lineage and may be needed for contested/effective Responsibility or Participation reconciliation.

---

# 11. Other high-value relationship terms

## Trigger

**Status:** DEFERRED

```text
Trigger != Recurrence
Trigger != Routine
fallback/conditional Responsibility != current Responsibility
```

## Relationship

**Status:** CANONICAL MODELING CAPABILITY / SEMANTIC RULE — NOT ENTITY/ROOT  
**Validation:** `checkpoints/relationship-v0-validation.md` — PASS WITH HARDENING

LifeOS uses the most specific truthful relation semantics. A semantically complete simple connection may remain direct. A relationship that itself has materially relevant state, lifecycle, history, temporal scope, authority, provenance, privacy, actor-scoped state or domain invariants may become a **specific qualified relation family**.

```text
universal Relationship entity/root = rejected
semantic-free related_to as kernel truth = rejected
specific relation semantics > generic edge
qualified relation != entity automatically
queryability/cardinality/database row id != domain identity
orientation/symmetry/transitivity/inverse rules are relation-family-specific
```

Responsibility and Participation are the first two major successful stresses of this rule: simple relations may remain direct, while material state/history/privacy/actuality can justify specific qualified relation contexts.

A future generic Personal Knowledge link capability is separately SAFE DEFERRED and must not silently become Responsibility, Authority, Evidence, Participation, allocation or Actual semantics.

## Dependency

**Status:** DEFERRED / likely specific relationship family or typed semantic

Represents coordination dependency where justified. Exact directionality, history, waiver, lag and reasoning/transitivity rules require dedicated review rather than inheritance from `Relationship` generally.

---

# 12. Frequently confused terms

## Core

```text
Goal != Plan
Goal != Milestone
Plan != Activity
Plan != Routine
Activity != Event
Activity != Session
Event != Schedule
Event != Participation response
Event != Actual Participation/attendance
Event identity != participant set/state
Routine != Recurrence
Routine != observed habit
Occurrence != Schedule
Occurrence != Session
Schedule != Temporal Constraint
Schedule != Availability
Schedule != Capacity Reservation
Schedule != Session/Actual
Schedule acceptance != Participation response
Session != Actual
Session != Participation/attendance by default
Actual != Outcome
Actual != Observation
Actual != Confirmation
Actual != Evidence
Actual != Provenance
shared Actual != identical actor-specific Actual Participation
reported/asserted reality != established Actual
Outcome != lifecycle/operational state
Outcome != Observation
Outcome != Confirmation
Outcome != Provenance
Outcome != Evidence
Milestone attainment != independent duplicate Actual/Outcome/Observation truth
Observation != Quantity
Observation != universal RegisterEntry
Observation != Confirmation
Observation != Evidence
Observation != Provenance
Quantity != Observation
Quantity != universal RegisterEntry
number != Quantity by default
property/quantity-kind != unit
compatible unit != semantic equivalence by itself
same unit != universal aggregation permission
Quantity != Range/Threshold/comparator/criterion
Subject != Person/Actor/Account/Principal/Asset/Resource
Subject != observer/recorder/source/transformer/authority/viewer
Subject role != Subject entity/root
Subject != generic related_to
Person != Actor
Person != Resource
Person != Participant
Person != Account
Person != Principal
Person != User domain primitive
Person != Asset
Actor != Resource
Actor != Account
Actor != Principal
Actor != Responsibility
Actor != Participation
Actor != Authority
Actor role != Actor entity/root
generic actor relation != specific action role
Account != Person/Actor/Subject/Participant
User != universal domain root
Asset != Subject
Asset != Resource
Asset != Person
Asset identity != owner/holder/steward
Asset instance != product/model definition
physical thing != Asset automatically
managed thing != Asset automatically
universal ManagedObject root = rejected
financial asset semantics != Asset entity
Resource role != Resource entity/root
Resource != Requirement
Resource != candidate set
Resource != Allocation
Resource != Reservation/Capacity Claim
Resource != actual use/consumption
Resource != Responsibility/Performer/Participant/Participation
Resource role != synthetic provider identity
Resource reservation != Participation
Money/Budget != Resource by default
Responsibility != requester
Responsibility != expected performer
Responsibility != actual performer
Responsibility != Participation
Responsibility != Resource
Responsibility != Authority
Responsibility != Visibility
Responsibility != Stewardship
unknown responsibility != explicitly open/unassigned
Assignment != standalone universal primitive
Claim != standalone universal primitive
Hand-off != standalone universal primitive
Assignment/Claim/Hand-off must identify specific role
hand-off request != effective transfer by default
Participation != Responsibility/Performer/Resource/Organizer/Authority/Visibility/Session
Participant != identity/entity
Invitation != Acceptance/Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
Attendance != standalone universal primitive
universal Relationship root = rejected
semantic-free related_to as kernel truth = rejected
specific relation semantics != generic Relationship wrapper
qualified relation structure != independent entity automatically
queryability/cardinality != domain identity
Register/Tracker UI != kernel Register primitive
saved longitudinal view != source of truth
view membership != duplicate native record
Confirmation != Acknowledgement
Confirmation != Acceptance/Agreement
Confirmation != Verification
Confirmation != Authority
Confirmation != Provenance
Evidence != source information
Evidence != Provenance
Evidence != GoalCriterion
Provenance != Source
Provenance != truth
Provenance != Authority
Provenance != Version
Provenance != Audit
missing Observation != observed negative
no Confirmation != false/rejected/incorrect
no Evidence != Evidence against
recorded time != Observation effective time
Temporal Constraint != Availability
Recurrence != Trigger
Availability != empty-gap cache
Capacity != universal busy/free boolean
```

## Multi-actor

```text
Person != Account
Person may exist without Account
Person may play Subject role
Person may play Actor/specific action role
Person may play Resource role
Person may play Participant role
Actor != Account
Actor != Principal
Actor != Subject
Actor != Resource
Actor != Responsibility/Participation/Authority
Account != Participant
Subject != Resource
Asset != owner
Asset owner != holder/custodian/steward
Asset ownership != Authority/Visibility
Asset may play Subject role
Asset may play Resource role
Resource candidacy != Responsibility/Participation/consent/allocation Authority
Participant != Responsible actor
Participant != Performer by default
Organizer != Participant by default
Responsible actor != expected performer
Responsible actor != actual performer
expected performer != actual performer
Creator != Owner/Governor
Visibility != Authority
Sharing != ownership
Assignment != Activity identity
Assignment != Acceptance by default
Claim != effective Responsibility by default
hand-off request != effective role transfer by default
Responsibility transfer != Activity replacement
Responsibility != coordination Stewardship
Participation response != Actual Participation
accepted != attended
declined != proved absent
no response != declined
no attendance evidence != proved absence
shared Actual != identical actor Participation
shared Outcome != identical actor consequence
shared Asset != identical actor visibility/private overlays
Observation Subject != observer/recorder/source/authority/viewer
current Account != universal Subject
current Account != semantic Actor automatically
non-LifeOS Person may be Subject/Participant/Actor/Resource candidate/Responsibility holder where context allows
response Actor != participant identity by default
Confirmation by A != Confirmation by B
conflicting Observation != automatic overwrite/average
conflicting Confirmation != automatic canonical truth
provider attendance telemetry != canonical Participation automatically
source actor != recorder != Subject by default
Schedule acceptance != Participation acceptance/response
Delivery != acknowledgement
Acknowledgement != agreement
Agreement != authority
Authority != Actual
Authority != Confirmation
Authority != Responsibility
Authority != Participation
Actor action != Authority
relation existence/type != Authority
relation existence/type != Visibility
AI knowledge != disclosure permission
AI inference != Confirmation
AI inference != established Actual
AI inferred relation != established relationship
AI Responsibility suggestion != effective assignment/transfer
AI Participation inference != established response/attendance
AI Subject/Person/Asset guess != established identity
AI Resource match != authoritative allocation
AI Actor != human author/authority automatically
AI provenance != disclosure permission
future Account access revocation != deletion of historical Person/Actor/Responsibility/Participation attribution
Quantity display preference != canonical value mutation
actor tracker preferences != shared fact mutation
```


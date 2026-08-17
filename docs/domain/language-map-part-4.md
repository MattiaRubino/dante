<!-- LIFEOS-CANONICAL-SPLIT document="language-map.md" part="4" total="5" -->
> **Canonical document split — Part 4 of 5.** Parts 1–5 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: [Part 1](language-map.md) · [Part 2](language-map-part-2.md) · [Part 3](language-map-part-3.md) · **Part 4** · [Part 5](language-map-part-5.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
## Product vs kernel

```text
Task != separate Activity primitive
Project != currently separate Plan primitive
Program != currently separate Plan primitive
Calendar Block != mandatory time primitive
Planning Item != current universal kernel root
Shared Item != universal collaboration primitive
Module != domain entity
Register/Tracker view != kernel Register entity
RegisterEntry != universal semantic record
Subject UI/context != Subject entity
Actor UI label != Actor entity
Resource UI label != Resource entity
Relationship UI/link != universal Relationship entity
Participant UI label != Participant entity/root
Invitation UI/workflow != universal Invitation entity
Attendance UI != universal Attendance entity
Assigned-to UI != universal Assignment entity
Claim UI action != universal Claim entity
Hand-off UI action != universal HandOff entity
User UI/implementation term != universal domain entity
Account settings object != Person identity
Asset UI profile != new Asset subtype primitive automatically
Inventory UI != every unit is Asset
Gear/Device UI label != broader Asset kernel semantics
Needs confirmation != Confirmation object by itself
Source label != complete Provenance model
Quantity UI value != standalone Quantity entity
```

---

# 13. Domain -> Product -> UI examples

## Buy milk

```text
Domain: Activity
Product/UI: Task / Buy milk
```

Simple personal policy may hide Responsibility entirely or show `Assigned to me`; the underlying Activity identity does not depend on Account coincidence.

## Open household chore

```text
Activity
Take recycling out

Responsibility
explicitly open / claimable
```

This is not the same as unknown Responsibility data.

## Responsibility hand-off

```text
Activity
Pick up prescription

current responsible
Luca

hand-off request
Luca -> Anna

pending
Luca remains current holder unless policy/Authority makes transfer effective
```

## Shared dinner participation

```text
Event
Dinner · Saturday 21:00

Anna
invited → accepted
Actual Participation: attended

Luca
invited → declined
Actual Participation: unknown / established absent only if evidence supports it

Marco
not invited
Actual Participation: attended
```

Earlier response history is not rewritten to match later reality.

## Partial meeting attendance

```text
Event Actual
meeting occurred 10:00–12:00

Anna Actual Participation
10:00–12:00

Luca Actual Participation
10:35–11:10
```

No one-Session-per-attendee model is implied.

## Gym 3x/week

```text
Routine + Recurrence + Occurrences + optional Schedules
UI: Gym — 3 times per week
```

## Website redesign

```text
Goal optional + Plan + Activities + Events + Milestones
Product: Project
```

## Exam result

```text
Person student
+ Subject role on Observation
+ Event
+ Actual
+ Observation: score = 78/100
+ Outcome: passed
+ optional Confirmation
+ Evidence use toward Goal/Milestone
+ Provenance of imported/recorded result
```

UI may show simply `78/100 · Passed`, with source/evidence/history on demand.

## Weight history

```text
Person P17
        ↑ Subject role
Observation O1: body weight = Quantity(66.8 kg)
Observation O2: body weight = Quantity(66.5 kg)
Observation O3: body weight = Quantity(66.4 kg)
        ↓
query / trend projection
        ↓
UI: Weight / History / Tracker / Progress
```

No universal Subject wrapper or RegisterEntry copy is created.

## Camera history

```text
Asset A17 = specific Sony A7 IV body
        ↑ Subject role
Observation: shutter count = 32,411
Observation: battery health = 87%
        ↓
query / history projection
UI: Sony A7 IV / History
```

The camera is one Asset identity; the Observations do not become Asset fields merely because the UI groups them.

## Camera required for a shoot

```text
Activity: photo shoot

Resource Requirement
camera suitable for wildlife photography

Candidates
Asset A17
Asset A18

Allocation
A17 selected

Reservation
A17 17:00–20:00
```

Asset identity, Resource role, Requirement, Allocation, Reservation and Responsibility remain distinct.

## Consumable requirement

```text
Maintenance
Requirement: 500 ml oil
```

The supply may satisfy Resource semantics without becoming an identity-bearing Resource entity.

## Person required by capability

```text
Requirement
Japanese B2+

Candidates
Person Anna
Person Luca
```

The people retain Person identity. Resource candidacy does not establish Responsibility, Participation or Performer status.

## Company laptop

```text
Asset L1
owner = Company
holder = Person Mattia
maintenance responsibility = IT
coordination Stewardship = possibly Anna
actual repair performer = Technician
```

One Asset identity; ownership, possession, Responsibility, Stewardship and performer are separate semantics.

## Caregiver measurement

```text
Person Maria
        ↑ Subject role
Observation: temperature = 38.2 °C

Person Anna
        ↓ observer/recorder Actor roles

Account Anna-A1
        ↓ authenticates LifeOS access
```

Person, Subject, Actor role and Account remain distinct.

## External participant/responsible Person with no Account

```text
Person Dr. Rossi
Event Participant / possible Responsibility holder in relevant context
no LifeOS Account required
```

If Dr. Rossi later creates an Account, the human Person identity and historical roles do not need to be recreated.

## AI proposal

```text
AI Agent X
specific role: proposer
Actor semantics

Resource matching
proposes A17 for requirement

Responsibility planning
proposes Anna as responsible

Participation planning
suggests inviting Luca

service/security identity
future Principal semantics
```

AI proposal does not become allocation Authority, Responsibility, Participation response, Acceptance or human Confirmation automatically.

## Quantity display conversion

```text
shared Observation
value: 66.4 kg

Actor A display
66.4 kg

Actor B display
146.4 lb
```

One underlying fact; no per-actor Quantity/Observation duplication.

## Correction lineage

```text
Observation v1
subject = Asset A1
value = 32,411

Observation correction
subject = Asset A2
value remains 32,411
```

Material Provenance/Version history must preserve that Asset attribution changed rather than pretending A2 was always known.

## Private availability

```text
private source context / Observation / Provenance
        ↓
authorized projection
Unavailable 18:00–20:00
```

Shared Actors do not automatically receive the private source reason, Person/Asset linkage, Actor/delegation lineage, Resource-match basis, Responsibility context, Participation state or Subject association.

---

# 14. Frontend rule

Prefer plain language, progressive disclosure and contextual actions over internal nouns when clearer.

```text
Occurrence          → This time
Temporal Constraint → Deadline / Preferred time / Not before
Actual              → What happened? / Actual time / Performed
Outcome             → Passed / Partial / Approved / Result details
Observation         → Weight / Mood / Score / Odometer / Shutter count
Quantity            → 66.4 kg / 5 km / 45 min
Subject             → usually hidden; natural referent label such as Maria / Sony A7 IV
Person              → natural human name/contact representation
Actor               → hidden; expose role: Done by / Recorded by / Suggested by
Account             → Account / Profile / Login in settings/security context
Asset               → Car / Camera / Laptop / Bike / Gear / Equipment according to context
Resource            → usually hidden; Camera / Room / Person / Service / Who's available? / Required equipment
Relationship        → usually hidden; expose the specific verb/role instead
Responsibility      → Responsible / Assigned to / Who's handling this? depending on context
Participation       → Going / Maybe / Can't go / Attended / participant list according to context
Invitation          → Invite / invited
Attendance          → Attended / Partially attended / Did not attend where established
Assignment          → Assign / Reassign action
Claim               → I'll take it / Claim action
Hand-off            → Hand off / Transfer / Ask someone else
User                → ordinary product language only where unambiguous
Register capability → History / Tracker / Progress / Register when useful
Confirmation        → Confirm / Looks correct / Needs confirmation
Evidence            → Why? / Based on… / Supporting or conflicting data
Provenance          → Source / Imported from / Corrected by / View history
```

Reverse rule:

> **A UX label does not automatically create or broaden a backend/domain type.**

---

# 15. Implementation-language rule

Physical/API terminology remains intentionally incomplete until logical/physical modeling.

Do not infer table/class names from this map.

In particular Person, Actor, Account, Asset, Principal, Participant, Responsibility, Participation, Resource, Authority, Visibility, Actual, Outcome, Observation, Confirmation, Evidence, Provenance, Quantity and Subject-role references must not be translated prematurely into final SQL/cardinality choices.

Specific guardrails:

- Observation does not imply one generic fact table or row per sensor tick;
- Confirmation does not imply one universal polymorphic confirmation table;
- Evidence does not imply one persisted edge/entity per evaluative use;
- Provenance does not imply one universal provenance/actor graph/table or event row for every technical operation;
- Quantity does not imply a standalone table/entity for each scalar amount;
- Subject does not imply a universal `subjects` table/root or every referent inheriting from Subject;
- Actor does not imply a universal `actors` table/root, generic `actor_id`, or replacement of specific action roles;
- Resource does not imply a universal `resources` table/root, generic `resource_id`, or synthetic identity for supplies/pools;
- Relationship modeling discipline does not imply a universal `relationships` table, graph edge root, Node supertype, or one polymorphic `related_to` mechanism;
- Responsibility does not imply a universal `responsibilities` table, `assigned_to` field, or independent relation identity in every simple case;
- Participation does not imply a universal `participants`/`participations` table/root, one participant-status enum, one Session per attendee, or independent relation identity in every simple case;
- Invitation/Attendance do not imply standalone universal tables/entities;
- planned/response Participation and Actual Participation must remain independently representable even if one future aggregate stores both facets;
- provider attendee/attendance records do not define canonical LifeOS Participation automatically;
- Assignment/Claim/Hand-off do not imply standalone tables/entities;
- explicitly open/unassigned Responsibility must remain distinguishable from unknown, even if SQL later uses nullable references internally;
- structured/qualified relation persistence does not by itself establish independent domain identity;
- queryability, cardinality and database row IDs do not create domain concepts;
- Resource Requirement/Allocation/Reservation remain distinct logical-model questions;
- Person does not imply `persons.id = accounts.id`;
- Account does not imply final auth/provider/credential/Principal schema;
- User must not become the universal implementation FK just because the UI uses the word;
- Asset does not imply one universal managed-things table, one table per subtype, one row per physical unit, or inheritance into Resource;
- Asset serial/provider identifiers do not define canonical Asset identity by default;
- Asset model/type/profile semantics are not fixed yet;
- heterogeneous Subject/Actor/Resource/relation references must preserve native semantics and attribution/history;
- longitudinal UI does not imply a universal `registers` + `register_entries` source-of-truth schema;
- saved tracker/view configuration may be persisted without becoming domain truth;
- unit normalization does not erase source representation/provenance;
- provider/source/auth identifiers do not define Person/Asset/domain identity by default;
- product aliases do not create duplicate persistence models.

When implementation names later differ for good technical reasons, document the mapping here.

---

# 16. Terminology change policy

A term may enter when at least one holds:

1. it is an accepted Domain Atlas concept/capability/value/role/relation semantics;
2. it is recurring product/UI language with clear mapping;
3. omitting it creates material ambiguity;
4. a demonstrated semantic need must be tracked as PROVISIONAL/DEFERRED.

A term does not become canonical because a competitor uses it, a table would be convenient, a mockup contains it, an AI suggested it, or it makes the ontology look complete.

A historical candidate may be rejected when validation shows that its useful behavior is better expressed through existing concepts plus product/query/application capability or a semantic role rather than a new entity.

An implementation/security concept may have an accepted boundary without being promoted prematurely into a fully modeled domain concept. `Account` currently follows this rule.

A terminology-neutral revisit can resolve a naming-bias concern without freezing the noun forever. Asset v0 currently follows this rule: its cross-domain semantic test is complete, while the exact word `Asset` remains renameable.

Change procedure:

1. review/change source concept or candidate first;
2. preserve historical reasoning and rejection rationale;
3. update this map;
4. update checkpoints/handoffs;
5. update implementation names only after persistence/API exists.

Do not silently recycle one term with a new meaning.

---

# 17. Cluster-status reference

Current integrated checkpoint set:

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING
Relationship v0 review          PASS WITH HARDENING
Responsibility v0 review        PASS WITH HARDENING
Participation v0 review         PASS WITH HARDENING
```

Current cross-cluster structural reopenings: **0**.

Normative transition/current references:

- `checkpoints/data-subjects-v0.md`;
- `checkpoints/deferred-dependency-closure-clusters-1-4-v0.md`;
- `checkpoints/cross-cluster-validation-v4.md`;
- `checkpoints/relationship-v0-validation.md`;
- `concepts/responsibility.md`;
- `checkpoints/responsibility-v0-validation.md`;
- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`.

Relationships / Reasoning is **IN PROGRESS**. The next candidate must be reselected by dependency leverage rather than roadmap order. Responsibility and Participation now both place strong pressure on the common-ground/governance boundary — especially Authority, Visibility, Acceptance/Acknowledgement and delegation — but none of those terms is pre-accepted by this map.

---

# 18. Maintenance rule

This file is the semantic navigation layer, not a duplicate of every concept spec.

It should answer quickly:

> **What does this LifeOS term mean, what does it not mean, what status does it have, and what might a user actually see?**

Detailed lifecycle, tests, history, rejected alternatives and persistence implications remain in the authoritative concept/checkpoint documents.

---

# 2026-08-13/14 — Downstream current-state consolidation amendment

This amendment is part of the same canonical document. It preserves downstream current-state sections without deleting the full pre-compaction baseline above. A current section is retained in full whenever it contains material text not already present verbatim in the baseline, so heading/list/example context is preserved. Where a later status, closure, or repository-state statement conflicts with an earlier one, the later amendment is authoritative; earlier rationale, examples, rejected alternatives, tests, and boundary detail remain preserved unless explicitly superseded.


**Status:** Canonical terminology reference for the active Domain Atlas  
**Established:** 2026-08-11  
**Current revision:** 2026-08-14 — Reconciliation / Source Precedence v0 semantic propagation complete; probe cleanup and historical-preservation audit complete; final branch QA pending current-document reconstruction and separately gated upstream `main` sync  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## Purpose

LifeOS uses the same ordinary words at several semantic layers. Without explicit separation, product language, UI labels, external provider vocabulary, code names, persistence artifacts, and domain concepts can silently redefine each other.

This map is the current terminology authority for the Domain Atlas.

It governs the distinction between:

```text
DOMAIN
PRODUCT
UI
IMPLEMENTATION
```

A word may legitimately appear at more than one layer while meaning different things. The layer must be explicit whenever ambiguity matters.

---


## 1. Language hierarchy
### DOMAIN
The semantic meaning required for LifeOS to preserve reality, intention, history, identity, responsibility, relationships, evidence, authority, and time correctly.

Examples:

```text
Goal
Plan
Activity
Event
Routine
Milestone
Occurrence
Schedule
Session
Observation
Actual
Outcome
Evidence
Provenance
Relationship
Responsibility
Participation
Authority
Visibility
Acknowledgement
Decision
Agreement
Consent
Representation
Version / Material-State
Reconciliation
```

Domain terminology is selected only through explicit semantic validation.

### PRODUCT
A product capability, configuration, projection, mode, helper, workflow, or feature that may combine several domain concepts.

Examples:

```text
Tracker
Register
Calendar Block
Temporary Mode
Life Area
Inbox
Weekly Review
Focus Mode
Progress View
Shared Plan
```

Product terms may be useful and persistent without becoming kernel primitives.

### UI
Words shown to users because they are understandable and actionable.

Examples:

```text
Done
Skip
Accept
Decline
Confirm
Apply
Use this
Moved
Busy
Free
Share
Owner
Assigned to
```

UI vocabulary optimizes comprehension. It does not define ontology by itself.

### IMPLEMENTATION
Technical concepts required for storage, APIs, security, providers, synchronization, framework code, or deployment.

Examples:

```text
Account
Principal
JWT subject
OAuth token
provider event ID
sync token
row version
ETag
foreign key
join table
polymorphic reference
materialized view
```

Implementation language must not silently become domain meaning.

---



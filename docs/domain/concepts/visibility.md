# Visibility v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Visibility is the contextual information-exposure capability through which a bounded representation of a domain object, fact, relationship, state, or projection may be made available for inspection or receipt by a specific recipient/access context under an applicable basis. Visibility does not create recipient identity and does not by itself grant Authority to change the underlying domain, permission to use or re-disclose the information for another purpose, access to hidden source causes or related records, Acknowledgement that the information was explicitly taken notice of, or technical authorization identity.**

Visibility answers:

> **What information may this recipient context be exposed to?**

Visibility is a **canonical cross-cutting information-exposure capability**, not a universal Access mega-concept and not an ACL entity/root.

---

# 1. Why Visibility exists

LifeOS needs selective disclosure across one shared reality without duplicating objects per user.

Examples:

- expose `Unavailable 18:00–20:00` without exposing the private Event causing it;
- show a shared Asset without exposing serial number, price, exact location or private notes;
- let two endpoints be visible while a sensitive relationship between them remains hidden;
- let an external Person receive a bounded projection without a LifeOS Account;
- let AI use authorized private context for a safe derived answer without disclosing the private source.

Without Visibility semantics LifeOS is pushed toward `shared=true`, object-wide ACL assumptions, per-user duplicated reality, or read access confused with Authority.

---

# 2. Representation / projection scope

Visibility does not necessarily expose an entire object.

```text
visible:
Asset Sony A7 IV
current availability

not automatically visible:
serial number
purchase price
private location
private notes
ownership history
```

> **Visibility may apply to a bounded representation/projection rather than every facet/source of the underlying object.**

Exact field/facet policy belongs to later logical/security design.

---

# 3. Projection visibility != source visibility

```text
PRIVATE SOURCE
Therapy Event 18:30–19:30
        ↓ authorized computation
DERIVED PROJECTION
Unavailable 18:30–19:30
        ↓
recipient-visible
```

```text
Visibility(projection) != Visibility(source)
```

A safe projection does not create a duplicate public source object.

---

# 4. Endpoint visibility != relationship visibility

```text
Person Anna visible
Event E visible
Participation(Anna, E) private
```

```text
Visibility(endpoint A) + Visibility(endpoint B)
!= Visibility(relationship A↔B)
```

This applies to Participation, Responsibility, Authority, Acknowledgement, ownership, Subject associations, Resource allocation, Provenance and future relationship families.

---

# 5. Visibility versus Authority

```text
Visibility != Authority
can see != can change/govern
```

Authority also grants no automatic Visibility. An Actor may approve an aggregate/consequence without seeing every private source.

---

# 6. Visibility versus Account / Principal / technical read permission

```text
Account != Visibility
Principal != Visibility
technical read permission != Visibility
```

Account/Principal are platform/security contexts; technical read permission is enforcement; Visibility is domain/product exposure semantics.

An external Person may receive an authorized projection without a native LifeOS Account.

---

# 7. Visibility versus actual view / read / Acknowledgement

Visibility means information **may be exposed**.

```text
may view
!= actually viewed/read
!= explicitly acknowledged
```

Provider/client read/display telemetry and explicit Acknowledgement are separate from standing Visibility.

Acknowledgement v0 now closes the semantic boundary:

```text
Visibility != Acknowledgement
read/display telemetry != Acknowledgement
```

A recipient can have Visibility without reading; can read without explicit Acknowledgement; can explicitly Acknowledge a specific version/change where the workflow supports it.

---

# 8. Visibility versus knowledge and historical disclosure

Revoking Visibility controls future LifeOS-mediated exposure. It does not erase human knowledge or external copies.

```text
T0 hidden
T1 shared
T2 viewed
T3 Visibility revoked
```

At T3:

```text
current Visibility = no
```

but not:

```text
recipient no longer knows
past disclosure never happened
external copies disappear
```

> **Visibility revocation does not rewrite historical disclosure or human knowledge.**

Current Visibility and historical Visibility are different questions.

---

# 9. Not visible != nonexistent

```text
not visible != nonexistent
```

This matters for search, counts, relationships, notifications, AI answers, calendar projections and errors.

Even revealing `1 hidden participant` is itself a disclosure choice.

---

# 10. Unknown/no grant != explicit prohibition

```text
Visibility unknown / no applicable grant found
!= explicit prohibition
```

An enforcement engine may default-deny without turning that default into a domain fact of explicit prohibition.

---

# 11. Visibility versus Sharing / Disclosure

```text
Visibility != Share
Visibility != Disclosure event
```

Visibility is current exposure capability. Sharing may alter it. Disclosure is an act/event of making information available.

No universal Share/Disclosure root is accepted by this concept.

---

# 12. Visibility != Authority to re-disclose

```text
can see X != may disclose X to Y
```

Re-disclosure belongs to separate Authority/privacy/policy semantics.

---

# 13. Visibility != downstream Use / purpose

```text
Visibility != arbitrary data-use permission
```

A visible record may still be restricted from unrelated analytics, training, export or secondary use.

Consent, purpose limitation and processing policy remain separate candidate/deferred areas.

---

# 14. Subject / Responsibility / Participation / Resource / ownership boundaries

None of the following automatically grants Visibility:

```text
being Subject
being Participant
holding Responsibility
being Resource candidate/allocated Resource
owning an Asset
creating an object
organizing an Event
acknowledging a change
```

A relationship itself may be more sensitive than either endpoint.

---

# 15. Provenance / Actual / Evidence boundary

```text
Visibility(target) != Visibility(full Provenance)
Visibility != truth
Visibility != Actual
Visibility != Confirmation
Visibility != Evidence
```

A private/hidden fact may still be true; a visible assertion may still be wrong or contested.

---

# 16. Multi-actor implications

Visibility supports one shared reality plus actor-scoped exposure.

Key rules:

- Accountless Person may receive bounded projection;
- Participation does not grant all Event-related information;
- Responsibility does not grant all related private context;
- Authority does not automatically grant Visibility;
- Acknowledgement does not grant broader Visibility or re-disclosure;
- ownership does not mean universal visibility;
- historical Participation/Responsibility does not imply future Visibility;
- revocation does not erase historical attribution;
- visible object does not expose every relationship/facet;
- group/role membership may be one basis, never universal exposure;
- no per-user copies of shared facts are required merely for privacy.

---

# 17. Unequal-power contexts

Guardian, caregiver, manager, teacher or specialist relationships may justify bounded Visibility in specific contexts.

They do not imply:

```text
role = manager/guardian/etc.
→ see everything
```

Visibility remains contextual, bounded, explainable and separable from Authority, Consent and Acknowledgement.

---

# 18. AI / Context Builder boundary

```text
private source
Therapy 18:30–19:30

AI Context Builder
may use authorized source

shared answer
18:30–19:30 doesn't work
```

AI must not infer:

```text
may process source → may reveal source
```

> **AI source access/processing is not disclosure permission. Output Visibility must be evaluated independently.**

Inference privacy matters: a derived answer can leak source meaning even if the source record is hidden.

Likewise AI read/access telemetry does not fabricate another actor's Acknowledgement.

---

# 19. Scale and persistence

Visibility semantics do not require materializing every recipient×object×field ACL edge.

Future implementations may derive exposure from bounded policy, relationship, group, scope, projection or explicit grant.

Canonical rules:

- query frequency does not create domain identity;
- visibility-check scale does not justify universal ACL ontology;
- field/facet/projection persistence is logical/security design;
- no universal `visibility` root or polymorphic `can_access` kernel edge is pre-approved.

---

# 20. Product / UI language

Typical UI:

```text
Private
Shared with Anna
Only me
Available to household
Show free/busy only
```

The UI need not expose `Visibility` as ontology vocabulary.

Actual read/acknowledgement flows may use different UI such as `Seen`, `Got it`, `Acknowledge`; those do not redefine Visibility.

---

# 21. Relationship-modeling implication

Simple cases may be direct/derived from bounded policy/context. Rich cases may require a specific qualified visibility/exposure context with target/projection, recipient, scope, purpose/basis, effective period or history.

```text
qualified Visibility != independent entity automatically
```

No universal Relationship/ACL root is required.

---

# 22. Core invariants

1. **Visibility is contextual information-exposure capability, not identity.**
2. **Visibility != Authority.**
3. **Visibility != Account/Principal/technical read permission.**
4. **Visibility != actual view/read/Acknowledgement.**
5. **Read/display telemetry != Acknowledgement.**
6. **Visibility != knowledge.**
7. **Visibility revocation != historical disclosure erasure.**
8. **Current Visibility != historical Visibility.**
9. **Not visible != nonexistent.**
10. **No applicable grant != explicit prohibition semantically.**
11. **Projection visibility != source visibility.**
12. **Endpoint visibility != relationship visibility.**
13. **Object visibility != every facet visibility.**
14. **Visibility != permission to re-disclose.**
15. **Visibility != arbitrary downstream Use/purpose.**
16. **Participation/Responsibility/Subject/Resource/ownership/Acknowledgement do not automatically grant Visibility.**
17. **Target visibility != full Provenance visibility.**
18. **Visibility != truth/Actual/Confirmation/Evidence.**
19. **AI may process authorized source != AI may disclose source.**
20. **No universal Access mega-concept / ACL entity/root is accepted.**
21. **Exact enforcement/persistence belongs to later logical/security design.**

---

# 23. Adjacent Dependency Sweep

## RESOLVED

- Visibility ↔ Authority: information exposure != governance.
- Visibility ↔ Account/Principal: identity/enforcement != Visibility.
- Visibility ↔ technical Read Permission: security enforcement != domain exposure.
- Visibility ↔ Participation: involvement != access.
- Visibility ↔ Responsibility: accountability != access.
- Visibility ↔ Subject: aboutness != access.
- Visibility ↔ Asset/ownership: identity/ownership != access.
- Visibility ↔ Resource: eligibility/allocation != access.
- Visibility ↔ source/projection: projection visibility != source visibility.
- Visibility ↔ Disclosure/Share: operation/event != standing capability.
- Visibility ↔ actual View/read: may see != did see/read.
- Visibility ↔ Acknowledgement: exposure/read evidence != explicit taking-notice.
- Visibility ↔ Provenance: target visibility != full lineage visibility.

## SAFE DEFERRED

### Consent

**Owner:** privacy/common-ground review.  
**Why safe:** Consent may be one basis/constraint for exposure/use but is not Visibility.  
**Reopening trigger:** privacy cannot be represented without collapsing Consent into Visibility.  
**Tests to rerun:** CORE-04, MA-05, MA-07, MA-13, XCON-02, XCON-05.

### Data Use / purpose limitation

**Owner:** Consent/privacy/policy review.  
**Why safe:** inspection/receipt remains separate from downstream processing/reuse.  
**Reopening trigger:** ordinary privacy workflows require Visibility to encode arbitrary purpose/use semantics.  
**Tests to rerun:** CORE-03, CORE-04, MA-07, MA-08, MA-17.

### Inference privacy / derived disclosure

**Owner:** AI Context Builder + privacy review.  
**Why safe:** projection/source distinction is fixed.  
**Reopening trigger:** safe AI output cannot be governed without changing Visibility semantics.  
**Tests to rerun:** MA-07, MA-08, MA-17, CORE-09, CORE-13.

### Principal / technical enforcement

**Owner:** security logical model.  
**Why safe:** domain Visibility and technical authorization remain separate.  
**Reopening trigger:** enforcement cannot preserve recipient/Actor/Account/Principal separation.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, MA-01, XCON-01.

### Group / public / link recipient scope

**Owner:** multi-actor/security review.  
**Why safe:** recipient/access context does not require final Group/public-link ontology.  
**Reopening trigger:** ordinary sharing cannot represent recipient scope without new native identity semantics.  
**Tests to rerun:** CORE-04, CORE-10, MA-02, MA-09, XCON-01.

### Sensitivity / field/facet/projection policy

**Owner:** privacy/logical/security model.  
**Why safe:** bounded representation exposure is fixed without selecting storage granularity/taxonomy.  
**Reopening trigger:** selective disclosure cannot be represented without semantic redesign.  
**Tests to rerun:** CORE-04, CORE-10, CORE-13, MA-07, XCON-04.

### Authority to disclose/re-share

**Owner:** Authority + privacy policy.  
**Why safe:** recipient Visibility grants no re-disclosure Authority.  
**Reopening trigger:** re-sharing workflows require Visibility itself to carry governance power.  
**Tests to rerun:** CORE-04, MA-06, MA-07, XCON-02.

### Access/view audit / read receipt persistence

**Owner:** Audit/integration/logical model.  
**Why safe:** Acknowledgement v0 has now closed the semantic boundary; read/view telemetry remains distinct.  
**Reopening trigger:** durable read/view evidence cannot coexist with the current Visibility/Acknowledgement separation.  
**Tests to rerun:** CORE-02, CORE-04, CORE-10, CORE-13, MA-05, MA-07, MA-11, XCON-03.

### Retention / deletion / external copies

**Owner:** privacy/retention review.  
**Why safe:** revocation is future LifeOS-mediated exposure, not retroactive knowledge erasure.  
**Reopening trigger:** retention/deletion requirements force Visibility to represent copy lifecycle.  
**Tests to rerun:** CORE-02, CORE-09, MA-11, XCON-03.

### Qualified Visibility identity / persistence

**Owner:** logical data model.  
**Why safe:** rich grants/policies may need structure/history without proving universal identity.  
**Reopening trigger:** direct/derived/qualified representation cannot preserve scoped exposure/history.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 24. Rejected alternatives

Rejected:

- Visibility = Authority;
- Visibility = Account/Principal/technical read permission;
- Visibility = Participation/Responsibility/ownership/Subject/Resource;
- Visibility = actual View/read/Acknowledgement;
- Visibility = arbitrary downstream Use;
- universal Access mega-concept;
- universal ACL/Visibility entity/root;
- `shared=true` as complete privacy model;
- visible endpoints imply visible relationship;
- visible projection implies visible source;
- revocation implies erased historical knowledge;
- AI source processing implies disclosure permission.

---

# 25. Reopening triggers

Reopen Visibility v0 if later evidence shows that:

1. exposure and Authority cannot remain distinct;
2. Consent/use semantics require Visibility to absorb a separate purpose/permission question;
3. field/projection/inference privacy cannot be represented without changing the core capability;
4. read/view/Acknowledgement persistence cannot preserve current semantic separation;
5. Principal/enforcement requires identity collapse;
6. logical persistence cannot preserve direct/derived/qualified Visibility/history.

Until then, Visibility remains the current accepted **cross-cutting information-exposure capability**, not an ACL/root.

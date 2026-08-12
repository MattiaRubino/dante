# Visibility v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Visibility is the contextual information-exposure capability through which a bounded representation of a domain object, fact, relationship, state, or projection may be made available for inspection or receipt by a specific recipient/access context under an applicable basis. Visibility does not create recipient identity and does not by itself grant Authority to change the underlying domain, permission to use or re-disclose the information for another purpose, access to hidden source causes or related records, acknowledgement that the information was actually seen, or technical authorization identity.**

Visibility answers:

> **What information may this recipient context be exposed to?**

Visibility is therefore a **canonical cross-cutting information-exposure capability**, not a universal Access mega-concept and not an ACL entity/root.

---

# 1. Why Visibility exists

LifeOS needs selective disclosure across one shared reality without duplicating domain objects per user.

Examples:

- expose `Unavailable 18:00–20:00` without exposing the private Event causing it;
- show a shared Asset without exposing serial number, purchase price, exact location, or private notes;
- let two endpoints be individually visible while their sensitive relationship remains hidden;
- allow an external Person to receive a bounded projection without having a LifeOS Account;
- allow AI to use authorized private context for a safe derived answer without disclosing the private source.

Without Visibility semantics, LifeOS would be pushed toward weak alternatives such as `shared=true`, object-wide ACL assumptions, per-user duplicated reality, or conflating read access with Authority.

---

# 2. Visibility is representation/projection scoped

Visibility does not necessarily expose an entire domain object.

A recipient may see:

```text
Asset: Sony A7 IV
current availability
```

without seeing:

```text
serial number
purchase price
private location
private notes
ownership history
```

Canonical rule:

> **Visibility may apply to a bounded representation/projection rather than every facet/source of the underlying domain object.**

Exact field/facet policy belongs to later logical/security design.

---

# 3. Projection visibility != source visibility

A private source may legitimately produce a shareable consequence.

Example:

```text
PRIVATE SOURCE
Therapy Event 18:30–19:30
        ↓ authorized computation
DERIVED PROJECTION
Unavailable 18:30–19:30
        ↓
recipient-visible
```

Therefore:

```text
Visibility(projection)
!= Visibility(source)
```

A safe projection does not create a duplicate public copy of the private source.

---

# 4. Endpoint visibility != relationship visibility

Two referents can each be visible while the relationship between them remains private.

```text
Person Anna visible
Event E visible
Participation(Anna, E) private
```

Therefore:

```text
Visibility(endpoint A)
+
Visibility(endpoint B)
!=
Visibility(relationship A↔B)
```

This applies to Participation, Responsibility, Authority, ownership, Subject associations, Resource allocation, Provenance, and future relationship families.

---

# 5. Visibility versus Authority

Authority governs domain effects.

Visibility governs information exposure.

```text
Visibility != Authority
can see != can change/govern
```

The reverse is also not universal: an Actor may be empowered to approve an aggregate/consequence without seeing every private source behind it.

See `authority.md`.

---

# 6. Visibility versus Account / Principal / technical read permission

Account/Principal identify platform/security contexts.

Technical read permission is enforcement.

Visibility is domain/product information exposure semantics.

```text
Account != Visibility
Principal != Visibility
technical read permission != Visibility
```

A backend/system administrator may be technically capable of reading storage without having ordinary domain Visibility in the product context.

An external Person may receive an authorized projection without a native LifeOS Account.

---

# 7. Visibility versus actual view / acknowledgement

Visibility means information **may be exposed**.

It does not prove that the recipient actually saw or understood it.

```text
may view
!= actually viewed

response delivered
!= read
!= understood
!= acknowledged
```

Actual access/view logs and Acknowledgement remain separate concerns.

---

# 8. Visibility versus knowledge

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
recipient no longer knows the information
past disclosure never occurred
external screenshots/copies disappear
```

Canonical rule:

> **Visibility revocation does not rewrite historical disclosure or human knowledge.**

---

# 9. Current Visibility != historical Visibility

A later grant does not imply the recipient could always see the information.

A later revocation does not imply the recipient never could.

```text
current Visibility
!= Visibility applicable at historical time T
```

Historical access/disclosure may require audit/provenance depending on consequence, but no universal view-event root is pre-approved.

---

# 10. Not visible != nonexistent

A recipient's inability to inspect information must not be interpreted as proof that the underlying information does not exist.

```text
not visible
!= nonexistent
```

This matters for search, counts, relationship existence, notifications, AI answers, calendar projections, and error messages.

Even disclosing `1 hidden participant` reveals information and must itself be treated as a projection/disclosure choice.

---

# 11. Unknown/no grant != explicit prohibition

Semantic states remain distinguishable:

```text
Visibility unknown / no applicable grant found
!= explicit prohibition
```

A security engine may default-deny without turning that enforcement default into a domain fact that a specific recipient is explicitly prohibited.

---

# 12. Visibility versus Sharing / Disclosure

Visibility is standing/current exposure capability.

Sharing is a product/workflow action that may alter exposure.

Disclosure is an act of making information available/sending it.

```text
Visibility != Share
Visibility != Disclosure event
```

High-consequence disclosure may later require audit/history, but this review does not justify universal `Share` or `Disclosure` entities.

---

# 13. Visibility != Authority to re-disclose

Being allowed to inspect information does not automatically allow re-sharing it.

```text
can see X
!= may disclose X to Y
```

Re-disclosure is governed by separate Authority/privacy/policy semantics.

---

# 14. Visibility != downstream Use / purpose

Inspection or receipt is not universal permission for arbitrary reuse.

A source may be usable for one authorized computation but not directly visible to another Actor.

A visible record may still be restricted from unrelated analytics, training, export, or secondary use.

```text
Visibility != arbitrary data-use permission
```

Consent / purpose limitation / processing policy remain separate SAFE DEFERRED dimensions.

---

# 15. Subject, Responsibility, Participation, Resource and ownership boundaries

None of the following automatically grants Visibility:

```text
being Subject
being Participant
holding Responsibility
being Resource candidate / allocated Resource
owning an Asset
creating an object
organizing an Event
```

A relationship itself may be more sensitive than either endpoint.

Visibility must therefore remain a separate contextual capability.

---

# 16. Provenance boundary

Visibility of a target does not imply visibility of its full Provenance.

A recipient may see:

```text
Result: passed
```

without receiving every private upstream Observation, identity linkage, source payload, correction actor, or provider record.

Likewise access to some Provenance does not imply access to every upstream source.

```text
Visibility(target)
!= Visibility(full lineage)
```

---

# 17. Actual / Evidence boundary

Visibility does not establish truth, Actual, Confirmation, or Evidence strength.

A private or hidden fact may still be true.

A visible assertion may still be wrong or contested.

```text
Visibility != truth
Visibility != Actual
Visibility != Confirmation
Visibility != Evidence
```

---

# 18. Multi-actor implications

Visibility supports one shared canonical reality plus actor-scoped exposure.

Key rules:

- Accountless Person may receive a bounded projection;
- Participation does not grant all Event-related information;
- Responsibility does not grant all related private context;
- Authority does not automatically grant Visibility;
- ownership does not mean universal visibility;
- historical Participation/Responsibility does not imply future Visibility;
- revocation does not erase historical attribution;
- a visible object does not expose every relationship/facet;
- group/role membership may become one basis but never automatic universal visibility;
- no per-user copies of shared facts are required merely to implement privacy.

---

# 19. Unequal-power contexts

Guardian, caregiver, manager, teacher, or specialist relationships may justify bounded Visibility in specific contexts.

They do not imply:

```text
role = manager/guardian/etc.
→ see everything
```

Visibility remains contextual, bounded, explainable, and separable from Authority.

---

# 20. AI / Context Builder boundary

This is a critical LifeOS rule.

An AI may be allowed to use private source context to compute a safe consequence while being forbidden to disclose the source.

Example:

```text
private source
Therapy 18:30–19:30

AI Context Builder
may use authorized source

shared answer
18:30–19:30 doesn't work
```

The AI must not infer:

```text
may process source
→ may reveal source
```

Canonical rule:

> **AI source access/processing is not disclosure permission. Output Visibility must be evaluated independently.**

Inference privacy also matters: a derived answer can disclose sensitive source information even if the source record itself is hidden.

Exact Context Builder enforcement remains later implementation/security work.

---

# 21. Scale and persistence

Visibility semantics do not require materializing every possible recipient×object×field ACL edge.

Future implementations may derive exposure from bounded policy, relationship, group, scope, projection, or explicit grant where appropriate.

Canonical rules:

- query frequency does not create a domain entity;
- large-scale visibility checks do not justify universal ACL ontology;
- field/facet/projection persistence is a logical/security decision;
- no universal `visibility` table/root or one polymorphic `can_access` edge is pre-approved.

---

# 22. Simple UI versus kernel semantics

Ordinary product surfaces may use natural labels:

```text
Private
Shared with Anna
Only me
Available to household
Show free/busy only
```

The UI should not require users to understand `Visibility` as an ontology noun.

A product-level `Share` action may modify underlying visibility/policy without becoming a kernel entity.

---

# 23. Relationship-modeling implication

Visibility confirms Relationship v0.

Simple cases may be derived/direct from bounded policy/context.

Rich cases may require specific qualified visibility/exposure policy with target/projection, recipient context, scope, purpose/basis, effective period, or history.

```text
qualified Visibility
!= independent entity automatically
```

No universal Relationship/ACL root is required.

---

# 24. Core invariants

1. **Visibility is contextual information-exposure capability, not identity.**
2. **Visibility != Authority.**
3. **Visibility != Account/Principal/technical read permission.**
4. **Visibility != actual view/read/Acknowledgement.**
5. **Visibility != knowledge.**
6. **Visibility revocation != historical disclosure erasure.**
7. **Current Visibility != historical Visibility.**
8. **Not visible != nonexistent.**
9. **No applicable grant != explicit prohibition semantically.**
10. **Projection visibility != source visibility.**
11. **Endpoint visibility != relationship visibility.**
12. **Object visibility != every facet visibility.**
13. **Visibility != permission to re-disclose.**
14. **Visibility != arbitrary downstream Use/purpose.**
15. **Participation/Responsibility/Subject/Resource/ownership do not automatically grant Visibility.**
16. **Target visibility != full Provenance visibility.**
17. **Visibility != truth/Actual/Confirmation/Evidence.**
18. **AI may process authorized source != AI may disclose source.**
19. **No universal Access mega-concept / ACL entity/root is accepted.**
20. **Exact enforcement/persistence belongs to later logical/security design.**

---

# 25. Adjacent Dependency Sweep

## RESOLVED

- Visibility ↔ Authority: information exposure != governance.
- Visibility ↔ Account/Principal boundary: identity/enforcement != Visibility.
- Visibility ↔ technical Read Permission: enforcement != domain exposure semantics.
- Visibility ↔ Participation: involvement != access.
- Visibility ↔ Responsibility: accountability != access.
- Visibility ↔ Subject: aboutness != access.
- Visibility ↔ Asset/ownership: identity/ownership != access.
- Visibility ↔ Resource: eligibility/allocation != access.
- Visibility ↔ source/projection: projection visibility != source visibility.
- Visibility ↔ Disclosure/Share: operation/exposure event != standing visibility capability.
- Visibility ↔ actual View: may see != did see.
- Visibility ↔ Acknowledgement boundary: exposure != recognition.
- Visibility ↔ Provenance: target visibility != full lineage visibility.

## SAFE DEFERRED

### Consent

**Owner:** privacy/common-ground review.  
**Why safe:** Consent may be one basis/constraint for exposure/use but is not Visibility itself.  
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
**Why safe:** domain Visibility and technical request authorization remain distinct.  
**Reopening trigger:** enforcement cannot preserve recipient/Actor/Account/Principal separation.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, MA-01, XCON-01.

### Group / public / link recipient scope

**Owner:** multi-actor/security review.  
**Why safe:** Visibility only requires a recipient/access context, not a final Group/public-link ontology.  
**Reopening trigger:** ordinary sharing cannot represent recipient scope without a new native identity concept.  
**Tests to rerun:** CORE-04, CORE-10, MA-02, MA-09, XCON-01.

### Sensitivity / information classification

**Owner:** privacy/logical model.  
**Why safe:** current capability can expose bounded representations without one universal classification taxonomy.  
**Reopening trigger:** selective disclosure cannot be derived without canonical classification semantics.  
**Tests to rerun:** CORE-04, CORE-10, CORE-13, MA-07.

### Field/facet/projection policy

**Owner:** logical/security model.  
**Why safe:** representation-scoped Visibility is fixed without choosing storage granularity.  
**Reopening trigger:** persistence cannot represent source/projection/facet separation.  
**Tests to rerun:** CORE-10, CORE-13, XCON-04.

### Authority to disclose/re-share

**Owner:** Authority + privacy policy.  
**Why safe:** recipient Visibility explicitly grants no re-disclosure Authority.  
**Reopening trigger:** re-sharing workflows require Visibility itself to carry governance power.  
**Tests to rerun:** CORE-04, MA-06, MA-07, XCON-02.

### Access/view audit / read receipt

**Owner:** Audit/Acknowledgement review.  
**Why safe:** may-see and did-see are explicitly distinct.  
**Reopening trigger:** product requires acknowledged/read history that cannot coexist with Visibility.  
**Tests to rerun:** CORE-02, CORE-04, MA-05, XCON-03.

### Retention / deletion / cache / external copies

**Owner:** privacy/retention review.  
**Why safe:** revocation semantics are bounded to future LifeOS-mediated exposure.  
**Reopening trigger:** retention/deletion requirements force Visibility to represent copy lifecycle.  
**Tests to rerun:** CORE-02, CORE-09, MA-11, XCON-03.

### Qualified Visibility identity/persistence

**Owner:** logical data model.  
**Why safe:** rich grants/policies may need structure/history without proving universal identity.  
**Reopening trigger:** direct/derived/qualified representation cannot preserve scoped exposure/history.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

No current dependency is a structural blocker.

---

# 26. Rejected alternatives

Rejected:

- generic `Access` mega-concept combining read/write/use/share/execute;
- Visibility = Authority;
- Visibility = Account/Principal;
- Visibility = technical read permission;
- Visibility = Participation;
- Visibility = Responsibility;
- Visibility = ownership;
- Visibility = Subject;
- Visibility = Sharing;
- Visibility = actual View;
- Visibility = Acknowledgement;
- Visibility = Consent;
- Visibility = arbitrary downstream Use;
- object-wide `shared=true` as canonical semantic model;
- endpoint visibility automatically implying relationship visibility;
- safe projection automatically exposing source;
- universal ACL/Visibility entity/root.

---

# 27. Reopening triggers

Reopen Visibility v0 if later evidence shows that:

1. information exposure cannot remain separate from Authority or technical authorization;
2. source/projection/relationship visibility cannot be represented without duplicate domain reality;
3. Consent/use-purpose semantics prove inseparable from exposure capability;
4. AI inference/privacy cannot preserve safe derived disclosure under this boundary;
5. a universal Visibility identity/lifecycle is required across contexts;
6. logical persistence cannot preserve scoped/current/historical visibility without a stronger concept.

Until then, Visibility remains canonical **cross-cutting contextual information-exposure capability**, not entity/root or universal Access/ACL object.

---

# 2026-08-12 — Acknowledgement closure amendment

Acknowledgement v0 resolves the common-ground side of the previously open read/acknowledgement boundary without changing Visibility semantics.

```text
Visibility
= may this bounded representation be exposed?

Acknowledgement
= did this Actor explicitly take notice of this specific target/material version/change/request?
```

Therefore:

```text
Visibility != actual View/read
Visibility != Acknowledgement
read/display telemetry != Acknowledgement
```

The existing `Access/view audit / read receipt` SAFE DEFERRED item remains open only for audit/integration/persistence mechanics:

**Current owner:** Audit / Integration / logical model.  
**Why still safe:** Acknowledgement semantics are now canonical; provider/client read/view evidence remains a separate evidence/audit concern.  
**Reopening trigger:** durable read/view evidence cannot coexist with the current Visibility/Acknowledgement separation.  
**Tests to rerun:** CORE-02, CORE-04, CORE-10, CORE-13, MA-05, MA-07, MA-11, XCON-03.

Generic cross-domain `Acceptance` was rejected downstream as a standalone kernel primitive and is not part of Visibility. No Visibility reopening is required.

# Visibility v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

- **Primary candidate:** Visibility / Access.
- **Candidate pressure:** distinguish `can inspect`, `can receive`, `can use`, `can modify`, `can execute`, `can disclose`, and technical read capability.
- **Selected semantic:** Visibility as bounded information-exposure capability.
- **Rejected framing:** one universal `Access` mega-concept combining read/write/use/share/execute semantics.
- **Not pre-accepted:** Consent, data-use/purpose limitation, Share, Disclosure, access-log/View/Acknowledgement, sensitivity taxonomy, Group/public-link recipient ontology, technical Permission/Principal model.

This checkpoint validates Visibility as a **cross-cutting contextual information-exposure capability**. It does not design ACL/RBAC/ABAC/ReBAC persistence, field-level security storage, final Principal/AuthN/AuthZ, Consent, legal retention, SQL/API shapes, or universal sharing objects.

---

# 2. Candidate conclusion

> **Visibility is the contextual information-exposure capability through which a bounded representation of a domain object, fact, relationship, state, or projection may be made available for inspection or receipt by a specific recipient/access context under an applicable basis. Visibility does not create recipient identity and does not by itself grant Authority to change the underlying domain, permission to use or re-disclose the information for another purpose, access to hidden source causes or related records, acknowledgement that the information was actually seen, or technical authorization identity.**

Current classification:

```text
VISIBILITY
CANONICAL CROSS-CUTTING INFORMATION-EXPOSURE CAPABILITY
contextual + recipient/representation scoped
may be direct / derived / specifically qualified where justified
NOT native entity/root
NOT universal Access/ACL object

ACCESS
TOO BROAD AS ONE DOMAIN NOUN
read/write/use/share/execute remain separate questions

SHARE / DISCLOSURE
operations/exposure events
NOT Visibility itself
NOT standalone universal primitives by this review
```

---

# 3. Core Semantic Validation Gate

| Test ID | Result | Finding |
|---|---|---|
| CORE-01 Workflow inversion | PASS | selective exposure/projection is a real need distinct from governance and technical access |
| CORE-02 Deep chronology | PASS WITH HARDENING | grants, disclosure, view, revocation and historical visibility must not be conflated |
| CORE-03 Reductio | PASS | Authority/Account/Permission/Participation/Responsibility/ownership cannot replace Visibility |
| CORE-04 Redundancy / merge-split | PASS WITH HARDENING | Visibility survives; Share/Disclosure/View/Consent/Access mega-root do not |
| CORE-05 Traceability | PASS | private source → authorized projection → recipient exposure remains explainable |
| CORE-06 Orphan / independence | PASS | contextual capability, not native recipient/target identity |
| CORE-07 External benchmark | PASS | mature systems separate scopes/permissions/projections rather than treating object existence as universal disclosure |
| CORE-08 Anti-pattern | PASS | `shared=true`, endpoint visibility implies relation visibility, source visibility follows projection rejected |
| CORE-09 Correction / epistemic integrity | PASS WITH HARDENING | not visible != nonexistent; revoked != never disclosed; no grant != explicit prohibition semantically |
| CORE-10 Scale/history | PASS WITH HARDENING | do not materialize recipient×object×field edges as ontology by default |
| CORE-11 Simple vs power user | PASS | ordinary UX can use Private/Shared/free-busy labels |
| CORE-12 Product value/complexity | PASS | exposure sophistication appears only where useful |
| CORE-13 Implementation pressure | PASS WITH HARDENING | domain Visibility remains distinct from security enforcement/storage |

**Core Gate:** PASS WITH HARDENING.

---

# 4. Representative real-world inversions

## 4.1 Private source, shared consequence

```text
Private Event
Therapy 18:30–19:30
        ↓ authorized computation
Projection
Unavailable 18:30–19:30
        ↓
shared recipient
```

The recipient may see the consequence without receiving the Event reason, location, notes, participants, or other source details.

## 4.2 Visible endpoints, hidden relationship

```text
Person Anna visible
Event E visible
Participation(Anna,E) private
```

Endpoint visibility does not imply relationship visibility.

## 4.3 Visible object, hidden facets

```text
Asset Sony A7 IV visible
serial/location/private notes hidden
```

Object exposure need not be all-or-nothing.

## 4.4 AI Context Builder

AI may use authorized source context to derive a safe result without gaining permission to disclose the source.

```text
may process source
!= may disclose source
```

---

# 5. Deep chronology stress

Representative chronology:

```text
T0  note hidden from Anna
T1  note/projection shared with Anna
T2  Anna views it
T3  Visibility revoked
T4  historical query asks what Anna could see at T1/T2
```

Required truths:

- T3 stops/narrows future LifeOS-mediated exposure;
- T3 does not rewrite T1/T2;
- revocation does not erase human memory/screenshots/external copies;
- current Visibility != historical Visibility;
- actual view != mere visibility grant;
- later sharing does not imply earlier visibility.

**Result:** PASS WITH HARDENING.

---

# 6. Reductio / candidate elimination

```text
REMOVE Visibility
→ FAIL

Visibility = Authority
→ FAIL

Visibility = Account / Principal
→ FAIL

Visibility = technical read Permission
→ FAIL

Visibility = Participation
→ FAIL

Visibility = Responsibility
→ FAIL

Visibility = ownership
→ FAIL

Visibility = Subject
→ FAIL

Visibility = Sharing / Disclosure
→ FAIL

Visibility = actual View
→ FAIL

Visibility = Acknowledgement
→ FAIL

Visibility = Consent
→ FAIL

Visibility = arbitrary downstream Use
→ FAIL

universal Access mega-concept
→ FAIL

contextual bounded Visibility capability
→ PASS WITH HARDENING
```

---

# 7. Primary hardenings

1. **Can see != can change/govern.**
2. **Can see != can re-disclose.**
3. **Can see != can use for any purpose.**
4. **May see != actually saw.**
5. **Visible target != visible related records.**
6. **Visible endpoints != visible relationship.**
7. **Visible projection != visible source.**
8. **Current Visibility != historical Visibility.**
9. **Revoked Visibility != erased past disclosure/knowledge.**
10. **Not visible != nonexistent.**
11. **No applicable grant != explicit prohibition semantically.**
12. **AI may process source != AI may disclose source.**

---

# 8. Multi-Actor Compatibility Gate

| Test ID | Result | Finding |
|---|---|---|
| MA-01 | PASS | Accountless Person may receive a bounded shared projection |
| MA-02 | PASS | one shared reality supports actor-scoped exposure without per-user copies |
| MA-03 | PASS | Responsibility does not grant all related information |
| MA-04 | PASS | Stewardship/coordination burden does not grant universal Visibility |
| MA-05 | PASS WITH HARDENING | exposure != read/acknowledgement/agreement |
| MA-06 | PASS WITH HARDENING | Authority remains separate; re-disclosure may require Authority |
| MA-07 | PASS WITH HARDENING | selective disclosure is explicit core pressure |
| MA-08 | PASS WITH HARDENING | inference/output privacy distinct from source access |
| MA-09 | PASS | non-LifeOS recipient can receive bounded projection |
| MA-10 | PASS | acting/sharing Actor may differ from information Subject/recipient |
| MA-11 | PASS WITH HARDENING | revocation affects future exposure, not historical disclosure/attribution |
| MA-12 | PASS | disputed/unknown visibility bases can remain unresolved |
| MA-13 | PASS WITH HARDENING | guardian/manager/caregiver access may be bounded/asymmetric, never god-mode by relation alone |
| MA-14 | PASS | Resource allocation/availability does not imply source visibility |
| MA-15 | PASS | coordination responsibility does not imply private-source access |
| MA-16 | PASS | simple UI can hide ontology and use Private/Shared/free-busy labels |
| MA-17 | PASS WITH HARDENING | AI source processing does not imply output disclosure |
| MA-18 | PASS | specialist access controls can remain external/adapted |
| MA-19 | PASS | generic Access/ACL/Share roots not required |
| MA-20 | PASS | private/visible state does not change underlying domain truth attribution |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 9. Cross-Concept Consistency Gate

```text
XCON-01 Identity                           PASS
XCON-02 Ownership / Authority              PASS WITH HARDENING
XCON-03 Planned / current / actual/history PASS WITH HARDENING
XCON-04 Relationships                      PASS WITH HARDENING
XCON-05 Multi-actor                        PASS WITH HARDENING
XCON-06 Language                           PASS
```

No accepted prior concept requires structural reopening.

---

# 10. Adjacent Dependency Sweep

## RESOLVED

| Boundary | Resolution |
|---|---|
| Visibility ↔ Authority | information exposure != governance |
| Visibility ↔ Account/Principal boundary | identity/enforcement != Visibility |
| Visibility ↔ technical Read Permission | security enforcement != domain exposure semantics |
| Visibility ↔ Participation | involvement != access |
| Visibility ↔ Responsibility | accountability != access |
| Visibility ↔ Subject | aboutness != access |
| Visibility ↔ Asset/ownership | identity/ownership != access |
| Visibility ↔ Resource | eligibility/allocation != access |
| Visibility ↔ source/projection | projection visibility != source visibility |
| Visibility ↔ Disclosure/Share | operation/exposure event != standing visibility capability |
| Visibility ↔ actual View | may see != did see |
| Visibility ↔ Acknowledgement boundary | exposure != recognition |
| Visibility ↔ Provenance | target visibility != full lineage visibility |

## SAFE DEFERRED

### Consent

**Owner:** privacy/common-ground review.  
**Safe because:** Consent may be one basis/constraint for exposure/use but is not Visibility itself.  
**Reopening trigger:** privacy cannot be represented without collapsing Consent into Visibility.  
**Rerun:** CORE-04, MA-05, MA-07, MA-13, XCON-02, XCON-05.

### Data Use / purpose limitation

**Owner:** Consent/privacy/policy review.  
**Safe because:** inspection/receipt remains separate from downstream processing/reuse.  
**Reopening trigger:** ordinary privacy workflows require Visibility to encode arbitrary purpose/use semantics.  
**Rerun:** CORE-03, CORE-04, MA-07, MA-08, MA-17.

### Inference privacy / derived disclosure

**Owner:** AI Context Builder + privacy review.  
**Safe because:** projection/source distinction is fixed.  
**Reopening trigger:** safe AI output cannot be governed without changing Visibility semantics.  
**Rerun:** MA-07, MA-08, MA-17, CORE-09, CORE-13.

### Principal / technical enforcement

**Owner:** security logical model.  
**Safe because:** domain Visibility and technical request authorization remain distinct.  
**Reopening trigger:** enforcement cannot preserve recipient/Actor/Account/Principal separation.  
**Rerun:** CORE-06, CORE-10, CORE-13, MA-01, XCON-01.

### Group / public / link recipient scope

**Owner:** multi-actor/security review.  
**Safe because:** Visibility only requires a recipient/access context, not final Group/public-link ontology.  
**Reopening trigger:** ordinary sharing cannot represent recipient scope without a new native identity concept.  
**Rerun:** CORE-04, CORE-10, MA-02, MA-09, XCON-01.

### Sensitivity / information classification

**Owner:** privacy/logical model.  
**Safe because:** bounded representation exposure does not require one universal sensitivity taxonomy now.  
**Reopening trigger:** selective disclosure cannot be derived without canonical classification semantics.  
**Rerun:** CORE-04, CORE-10, CORE-13, MA-07.

### Field/facet/projection policy

**Owner:** logical/security model.  
**Safe because:** representation-scoped Visibility is fixed without choosing storage granularity.  
**Reopening trigger:** persistence cannot represent source/projection/facet separation.  
**Rerun:** CORE-10, CORE-13, XCON-04.

### Authority to disclose/re-share

**Owner:** Authority + privacy policy.  
**Safe because:** recipient Visibility explicitly grants no re-disclosure Authority.  
**Reopening trigger:** re-sharing workflows require Visibility itself to carry governance power.  
**Rerun:** CORE-04, MA-06, MA-07, XCON-02.

### Access/view audit / read receipt

**Owner:** Audit/Acknowledgement review.  
**Safe because:** may-see and did-see are explicitly distinct.  
**Reopening trigger:** product requires acknowledged/read history that cannot coexist with Visibility.  
**Rerun:** CORE-02, CORE-04, MA-05, XCON-03.

### Retention / deletion / cache / external copies

**Owner:** privacy/retention review.  
**Safe because:** revocation is bounded to future LifeOS-mediated exposure.  
**Reopening trigger:** retention/deletion requirements force Visibility to represent copy lifecycle.  
**Rerun:** CORE-02, CORE-09, MA-11, XCON-03.

### Qualified Visibility identity / persistence

**Owner:** logical data model.  
**Safe because:** rich grants/policies may need structure/history without proving universal identity.  
**Reopening trigger:** direct/derived/qualified representation cannot preserve scoped exposure/history.  
**Rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 11. Final verdict

```text
VISIBILITY
PASS WITH HARDENING

classification:
CANONICAL CROSS-CUTTING INFORMATION-EXPOSURE CAPABILITY

✅ contextual
✅ recipient-context scoped
✅ target / representation scoped
✅ may expose projection without source
✅ may change/revoke over time
✅ relationship itself may have independent visibility
✅ compatible with direct/derived/qualified policy

❌ entity/root
❌ Account / Principal
❌ technical read permission
❌ Authority
❌ Participation
❌ Responsibility
❌ ownership
❌ Sharing operation
❌ actual View
❌ Acknowledgement
❌ Consent
❌ arbitrary downstream Use
❌ universal ACL object
```

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 12. Documentation propagation

Required propagation for this accepted scope:

- [x] `concepts/visibility.md`
- [x] this checkpoint
- [x] `concepts/authority.md`
- [x] `concepts/participation.md`
- [x] `concepts/responsibility.md`
- [x] `concepts/subject.md`
- [x] `concepts/asset.md`
- [x] `concepts/resource.md`
- [x] `concepts/provenance.md`
- [x] `concepts/actual.md`
- [x] `language-map.md`
- [x] `README.md`
- [x] `workstreams/domain-model.md`

No `access.md`, `permission.md`, `sharing.md`, `disclosure.md`, `consent.md`, or `use-permission.md` is justified by this review.

---

# 13. Next-stage implication

With Authority and Visibility separated, the next high-leverage common-ground question is now clearer:

```text
who can govern        Authority
who can see           Visibility
who received/knows?   Acknowledgement/common-ground still open
who agrees/wants?     Acceptance/Agreement still open
```

Acceptance / Acknowledgement should therefore be re-scored next, without presuming they are one concept or standalone primitives.

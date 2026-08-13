# Visibility v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING  
**Validated:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Cluster:** Relationships / Reasoning v0  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

> **Historical checkpoint note:** the Visibility v0 validation result is preserved at the state known when it was accepted. Later Acknowledgement and Agreement/Consent work is recorded only as explicit downstream closure; it does not retroactively change the original validation result.

## 1. Scope

- **Primary candidate:** Visibility / Access boundary.
- **Family reviewed:** information exposure / technical read permission / Share-Disclosure / actual View / downstream Use / Authority boundary.
- **Purpose:** determine whether LifeOS needs cross-cutting bounded information-exposure semantics without creating a universal Access/ACL domain root.
- **Not pre-accepted:** Consent, purpose limitation, Principal/security enforcement, group/public-link recipient ontology, sensitivity taxonomy, read-receipt/Acknowledgement model.

Visibility was validated as a **contextual information-exposure capability**, not identity, technical authorization or universal ACL object.

---

# 2. Candidate conclusion

> **Visibility is the contextual information-exposure capability through which a bounded representation of a domain object, fact, relationship, state, or projection may be made available for inspection or receipt by a specific recipient/access context under an applicable basis.**

```text
VISIBILITY
CANONICAL CROSS-CUTTING INFORMATION-EXPOSURE CAPABILITY
contextual + recipient/representation scoped
may be direct/derived/specific qualified
NOT native entity/root
NOT universal Access/ACL object
```

---

# 3. Evidence reviewed

Internal evidence included shared-fact/private-overlay requirements, Availability/Capacity projection, Person/Actor/Subject/Asset/Resource boundaries, Participation/Responsibility, Authority, Provenance, Actual and AI Context Builder/privacy requirements.

External evidence was behavioral only: mature products and authorization/privacy systems demonstrate scoped exposure, derived projections, field/relationship sensitivity and revocation, but provider ACL vocabulary or infrastructure models do not define LifeOS ontology.

---

# 4. Core Semantic Validation Gate

| Test ID | Result | Finding |
|---|---|---|
| CORE-01 Workflow inversion | PASS | real coordination needs bounded exposure distinct from governance |
| CORE-02 Deep chronology | PASS WITH HARDENING | grants/revocation/history and past disclosure remain distinct |
| CORE-03 Reductio | PASS | Authority, Account, ACL, Sharing, actual View and downstream Use fail as replacements |
| CORE-04 Redundancy | PASS WITH HARDENING | Visibility survives; universal Access/ACL root does not |
| CORE-05 Traceability | PASS | private source → safe projection → recipient exposure remains explainable |
| CORE-06 Orphan/independence | PASS | contextual capability, not identity |
| CORE-07 External benchmark | PASS | mature systems reinforce scoped exposure/projection patterns |
| CORE-08 Anti-pattern | PASS | `shared=true`, endpoint leakage and universal ACL ontology rejected |
| CORE-09 Correction/privacy integrity | PASS WITH HARDENING | not visible != nonexistent; revocation != erased knowledge/history |
| CORE-10 Scale/history | PASS WITH HARDENING | no need to materialize every recipient×field edge |
| CORE-11 Simple/power user | PASS | Private/Shared/free-busy UI can remain simple |
| CORE-12 Product value/cost | PASS | selective exposure reduces coordination/privacy cost |
| CORE-13 Implementation pressure | PASS WITH HARDENING | domain exposure remains separate from security enforcement/schema |

**Core Gate:** PASS WITH HARDENING.

---

# 5. Primary hardenings

```text
can see != can change/govern
can see != can re-disclose
can see != can use for every purpose
may see != actually saw
visible target != every related record
visible endpoints != visible relationship
visible projection != visible source
current Visibility != historical Visibility
revoked Visibility != erased past disclosure/knowledge
not visible != nonexistent
no applicable grant != explicit prohibition semantically
AI may process source != AI may disclose source
```

---

# 6. Multi-Actor Compatibility Gate

| Test ID | Result | Finding |
|---|---|---|
| MA-01 | PASS | Accountless Person may receive bounded projection |
| MA-02 | PASS | one shared reality supports actor-scoped exposure |
| MA-03 | PASS | Responsibility does not grant all related information |
| MA-04 | PASS | Stewardship does not grant universal Visibility |
| MA-05 | PASS WITH HARDENING | exposure != read/Acknowledgement/agreement |
| MA-06 | PASS WITH HARDENING | Authority separate; re-disclosure may require Authority |
| MA-07 | PASS WITH HARDENING | selective disclosure is core pressure |
| MA-08 | PASS WITH HARDENING | inference/output privacy distinct from source access |
| MA-09 | PASS | non-LifeOS recipient may receive bounded projection |
| MA-10 | PASS | sharing Actor may differ from Subject/recipient |
| MA-11 | PASS WITH HARDENING | revocation affects future exposure, not past attribution |
| MA-12 | PASS | disputed/unknown visibility bases can remain unresolved |
| MA-13 | PASS WITH HARDENING | guardian/manager/caregiver relation is not god-mode |
| MA-14 | PASS | Resource allocation/availability does not imply source visibility |
| MA-15 | PASS | coordination responsibility does not imply private-source access |
| MA-16 | PASS | simple UI can hide ontology |
| MA-17 | PASS WITH HARDENING | AI source processing != output disclosure |
| MA-18 | PASS | specialist controls may remain external/adapted |
| MA-19 | PASS | generic Access/ACL/Share roots not required |
| MA-20 | PASS | exposure does not change underlying truth attribution |

**Multi-Actor Gate:** PASS WITH HARDENING.

---

# 7. Cross-Concept Consistency Gate

```text
XCON-01 Identity                           PASS
XCON-02 Ownership / Authority              PASS WITH HARDENING
XCON-03 Planned / current / actual/history PASS WITH HARDENING
XCON-04 Relationships                      PASS WITH HARDENING
XCON-05 Multi-actor                        PASS WITH HARDENING
XCON-06 Language                           PASS
```

No accepted prior concept required structural reopening.

---

# 8. Adjacent Dependency Sweep at validation time

## RESOLVED

| Boundary | Resolution |
|---|---|
| Visibility ↔ Authority | information exposure != governance |
| Visibility ↔ Account/Principal | identity/enforcement != Visibility |
| Visibility ↔ technical Read Permission | security enforcement != domain exposure |
| Visibility ↔ Participation | involvement != access |
| Visibility ↔ Responsibility | accountability != access |
| Visibility ↔ Subject | aboutness != access |
| Visibility ↔ Asset/ownership | identity/ownership != access |
| Visibility ↔ Resource | eligibility/allocation != access |
| Visibility ↔ source/projection | projection visibility != source visibility |
| Visibility ↔ Disclosure/Share | action/event != standing capability |
| Visibility ↔ actual View | may see != did see |
| Visibility ↔ Acknowledgement boundary | exposure != recognition |
| Visibility ↔ Provenance | target visibility != full lineage visibility |

## SAFE DEFERRED at validation time

### Consent

**Owner:** privacy/common-ground review.  
**Why safe:** Consent may be a basis/constraint for exposure/use but is not Visibility.  
**Trigger:** privacy cannot be represented without collapsing Consent into Visibility.  
**Rerun:** CORE-04, MA-05, MA-07, MA-13, XCON-02, XCON-05.

### Data Use / purpose limitation

**Owner:** Consent/privacy/policy.  
**Why safe:** inspection/receipt separate from downstream processing/reuse.  
**Trigger:** Visibility must encode arbitrary purpose/use semantics.  
**Rerun:** CORE-03, CORE-04, MA-07, MA-08, MA-17.

### Inference privacy / derived disclosure

**Owner:** AI Context Builder + privacy.  
**Why safe:** projection/source distinction fixed.  
**Trigger:** safe output cannot be governed without changing Visibility.  
**Rerun:** MA-07, MA-08, MA-17, CORE-09, CORE-13.

### Principal / technical enforcement

**Owner:** security logical model.  
**Why safe:** domain Visibility and technical authorization separate.  
**Trigger:** enforcement cannot preserve recipient/Actor/Account/Principal separation.  
**Rerun:** CORE-06, CORE-10, CORE-13, MA-01, XCON-01.

### Group / public / link recipient scope

**Owner:** multi-actor/security.  
**Why safe:** recipient/access context does not require final Group/public-link ontology.  
**Trigger:** ordinary sharing cannot represent recipient scope without new native identity semantics.  
**Rerun:** CORE-04, CORE-10, MA-02, MA-09, XCON-01.

### Sensitivity / field/facet/projection policy

**Owner:** privacy/logical/security.  
**Why safe:** bounded exposure does not select storage/taxonomy.  
**Trigger:** selective disclosure cannot be represented without semantic redesign.  
**Rerun:** CORE-04, CORE-10, CORE-13, MA-07, XCON-04.

### Authority to disclose/re-share

**Owner:** Authority + privacy policy.  
**Why safe:** recipient Visibility grants no re-disclosure Authority.  
**Trigger:** re-sharing requires Visibility itself to carry governance power.  
**Rerun:** CORE-04, MA-06, MA-07, XCON-02.

### Access/view audit / read receipt

**Owner at validation time:** Audit/Acknowledgement review.  
**Why safe:** may-see and did-see explicitly distinct.  
**Trigger:** acknowledged/read history cannot coexist with Visibility semantics.  
**Rerun:** CORE-02, CORE-04, MA-05, XCON-03.

### Retention / deletion / external copies

**Owner:** privacy/retention.  
**Why safe:** revocation concerns future LifeOS-mediated exposure.  
**Trigger:** retention/deletion forces Visibility to represent copy lifecycle.  
**Rerun:** CORE-02, CORE-09, MA-11, XCON-03.

### Qualified Visibility identity / persistence

**Owner:** logical data model.  
**Why safe:** rich policies/history do not prove universal identity.  
**Trigger:** direct/derived/qualified representation cannot preserve scope/history.  
**Rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 9. Final verdict

```text
VISIBILITY
PASS WITH HARDENING

classification:
CANONICAL CROSS-CUTTING INFORMATION-EXPOSURE CAPABILITY

✅ contextual
✅ recipient/representation scoped
✅ may be direct/derived/qualified
✅ supports safe projections

❌ native entity/root
❌ Authority
❌ Account/Principal/technical read permission
❌ Share/Disclosure operation
❌ actual View/Acknowledgement
❌ arbitrary downstream Use
❌ universal Access/ACL object
```

**Structural reopenings:** 0.  
**Unclassified material dependencies:** 0.

---

# 10. Documentation propagation at acceptance time

Visibility acceptance propagated to the concept/checkpoint and affected Authority/Participation/Responsibility/identity/reality/Provenance/Language Map/Domain README/workstream documents. No universal Access/ACL root was introduced.

---

# 11. Product / implementation implication

Simple UI can use `Private`, `Shared with…`, `free/busy only` while the kernel preserves projection/source/relationship distinctions. Technical authorization, field/facet persistence and read-audit mechanics remain later design work.

---

# 12. Historical next-stage implication

At Visibility acceptance time, Consent/use-purpose, Principal/enforcement, read/audit/Acknowledgement, inference privacy, group recipient scope and retention remained separately owned dependencies.

---

# 13. Historical preservation rule

The checkpoint's original statement `Visibility ↔ Acknowledgement boundary: exposure != recognition` was already semantically correct. The later Acknowledgement review strengthens and names the neighboring concept; it does not alter the Visibility verdict.

---

# 14. Downstream closure — Acknowledgement v0 (2026-08-12)

Acknowledgement v0 now closes the common-ground side of the existing boundary:

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

The prior `Access/view audit / read receipt` SAFE DEFERRED item is **partially resolved semantically** and remains SAFE DEFERRED only for persistence/audit mechanics:

**Current owner:** Audit / Integration / logical model.  
**Why still safe:** Acknowledgement semantics are canonical; provider/client read/view evidence remains a distinct integration/audit concern.  
**Reopening trigger:** durable read/view evidence cannot coexist with the current Visibility/Acknowledgement separation.  
**Tests to rerun:** CORE-02, CORE-04, CORE-10, CORE-13, MA-05, MA-07, MA-11, XCON-03.

Generic cross-domain Acceptance is not part of Visibility and was rejected downstream as a standalone primitive.

No Visibility hardening failed; structural REOPEN remains **0**.

Normative downstream references:

- `../concepts/acknowledgement.md`;
- `acknowledgement-v0-validation.md`.

---

# 15. Downstream closure — Agreement / Consent v0 (2026-08-13)

Agreement / Consent v0 resolves the historical `Consent` and `Data Use / purpose limitation` semantic dependencies without reopening Visibility.

Current canonical separation:

```text
Visibility
= bounded information-exposure capability for a recipient/access context

Consent
= actor-scoped bounded permission for action/use/exposure under defined target/scope/purpose/context

Agreement
= multi-party mutual assent to materially same terms/version
```

Therefore:

```text
Visibility ↔ Consent   RESOLVED
Visibility ↔ Agreement RESOLVED where relevant
```

Consent may be one basis/constraint for Visibility/use but is not Visibility itself. Visibility can exist under another applicable basis where Consent is not the governing basis. Agreement creates no automatic information exposure or re-disclosure right.

The original `Data Use / purpose limitation` semantic boundary is also downstream-closed: Consent owns actor-scoped purpose/scope permission where applicable, while technical policy/enforcement remains separately SAFE DEFERRED. Inference privacy remains independently open because derived answers can leak private causes even when source exposure and Consent semantics are otherwise correct.

Current remaining Visibility dependencies include inference privacy, Principal/enforcement, recipient/group scope, sensitivity/facet policy, re-disclosure Authority, view audit, retention/copies, qualified persistence and purpose/use enforcement mechanics.

No Visibility hardening failed; **Visibility remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `../concepts/agreement.md`;
- `../concepts/consent.md`;
- `agreement-consent-v0-validation.md`.
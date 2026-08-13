# Authority v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Authority is the contextual governance capability through which an eligible Actor or governed role is legitimately empowered, under an applicable basis, to establish, approve, change, override, revoke, or otherwise make a bounded domain effect effective for a defined target, scope, action, and context. Authority does not create Actor identity and does not by itself imply Responsibility, Participation, Visibility, ownership, Confirmation, truth, technical access, or actual performance.**

Authority answers the bounded governance question:

> **Who or what may legitimately make which domain effect effective, on what target, under what scope/context/basis?**

Authority is therefore a **canonical cross-cutting governance relation/capability**, not a native entity/root and not a generic administrator identity.

---

# 1. Why Authority exists

LifeOS needs to distinguish meaningful agency from legitimate governance effect.

Examples:

- an Actor may propose a Schedule change without being allowed to make it canonical;
- a Responsibility holder may be accountable without being allowed to reassign everybody;
- a participant may respond for themselves without being able to alter other participants;
- a specialist may legitimately establish a bounded specialist state without becoming the owner of the underlying Person/Asset;
- an external Person may hold domain Authority without a LifeOS Account;
- an AI may reason or propose without being authorized to enact a shared-domain change.

Without Authority semantics LifeOS would be forced to infer governance incorrectly from creator, owner, Account, Actor, Responsibility, Participation, Visibility, or technical permissions.

---

# 2. Authority is contextual and scoped

Authority without an effect/target/scope is too vague.

Conceptually, Authority must be able to distinguish dimensions such as:

- eligible holder / Actor or governed role;
- governed target/context;
- action or domain effect;
- applicable scope;
- effective period where relevant;
- conditions/basis;
- delegation constraints where relevant.

This does **not** imply a universal Authority table or eight physical columns.

Canonical rule:

> **Authority to do X does not imply Authority to do Y.**

---

# 3. Authority versus Actor

Actor answers:

> **Who acted?**

Authority answers:

> **Was that Actor legitimately empowered to make this bounded effect effective?**

Therefore:

```text
Actor != Authority
acting != being authorized to govern
```

A proposal may be meaningful Actor behavior without being a canonical state change.

---

# 4. Authority versus Person / Account / Principal

Person is native human identity.

Account is the platform/access identity boundary.

Principal is the future authenticated/authorized request identity/security concept.

Authority is domain governance power.

Therefore:

```text
Person != Authority
Account != Authority
Principal != Authority
```

A Person may hold Authority without an Account. Account creation/deletion must not manufacture or erase historical Authority.

Exact Principal/AuthN/AuthZ enforcement remains deferred.

---

# 5. Authority versus technical permission / authorization

This boundary is canonical:

```text
DOMAIN AUTHORITY
legitimate governance power in domain context

TECHNICAL AUTHORIZATION
whether an authenticated Principal/request may execute an operation now
```

A system administrator may technically access infrastructure without gaining specialist/personal domain Authority.

Conversely, a domain-authoritative Person may lack a current LifeOS Principal/access path.

Canonical rule:

> **Technical ability to execute X is not the same thing as legitimate domain Authority for X.**

---

# 6. Authority versus Responsibility

Responsibility answers who is accountable for ensuring a bounded commitment is handled.

Authority answers who may govern an effect.

```text
Responsibility != Authority
```

A responsible Actor does not automatically gain rights to reassign, disclose, approve, delete, or alter unrelated state.

A manager/coordinator may have Authority to reassign Responsibility without becoming responsible for execution.

---

# 7. Authority versus Participation

Participation is contextual involvement.

```text
Participation != Authority
```

Being invited, attending, organizing, or responding does not automatically grant power to reschedule, disclose, correct another participant's state, or govern the shared object.

---

# 8. Authority versus Visibility

Visibility concerns bounded information exposure.

Authority concerns governance/effect.

```text
Authority != Visibility
can see != can govern
```

The reverse is also not universal: an Actor may be able to approve an aggregate/consequence without seeing every private underlying source.

Authority grants no implicit read/disclosure rights.

See `visibility.md`.

---

# 9. Authority versus Confirmation

Confirmation is contextual attestation.

Authority is governance power.

```text
Confirmation != Authority
```

A Person may confirm a fact without having power to make it canonical for everyone. An authoritative source/process may establish state without a personal Confirmation.

---

# 10. Authority versus truth / Actual

Authority determines legitimate effect within a governed context; it does not make a proposition objectively true.

```text
Authority != truth
Authority != Actual
```

Authoritative effects may later be corrected, contested, superseded, or reconciled while preserving history.

---

# 11. Authority versus ownership

Ownership may be one possible Authority basis in some contexts, but is never universal equality.

```text
ownership != Authority
holder/custodian != Authority
steward != Authority
```

One Asset may simultaneously have different owner, holder, maintenance Responsibility, scheduling Authority, repair performer, and visibility contexts.

---

# 12. Delegation

Delegation is a bounded Authority-establishment/entrustment pattern, not a standalone universal root.

Example:

```text
Anna
Authority: reassign Team X work

Delegates to Luca
scope: same bounded authority
period: 7 days
```

Required rules:

- delegation identifies the Authority being delegated;
- one delegated Authority does not transfer every other Authority;
- delegated Authority does not imply Visibility, Responsibility, Participation, or ownership;
- re-delegation is not implied unless the governing basis permits it;
- expiry/revocation narrows future Authority without rewriting historical validity;
- current Authority != Authority that existed at historical action time.

No universal `Delegation` entity/root is pre-approved.

---

# 13. Approval and Decision boundary

Approval may be an action/effect that exercises Authority.

```text
Approval != Authority
```

The future Decision/effective-change review will determine whether/how decisions, approvals, rationale, reconciliation, and effective state-change records require dedicated structures.

Authority answers **who may make the effect effective**, not what a Decision record is.

---

# 14. Authority claims and epistemic integrity

A claim of Authority does not establish Authority.

```text
claimed Authority
!= established/effective Authority
```

Similarly:

```text
Authority unknown
!= established no Authority
!= explicitly prohibited
```

A security engine may fail closed without collapsing those domain meanings.

Provider role names, credentials, imported flags, or asserted mandates may be evidence/provenance toward Authority without becoming automatic equality.

---

# 15. Historical Authority

Authority is time/context sensitive where material.

```text
T0 Authority exists
T1 Actor acts under it
T2 Authority expires/revokes
```

LifeOS must preserve that T1 may have been legitimate even though current Authority no longer exists.

Canonical rules:

- revoked/expired != never existed;
- current Authority != historical Authority at action time;
- current Account state does not rewrite historical Authority attribution;
- later discovery that a basis was invalid requires explicit reconciliation/correction, not silent history rewrite.

---

# 16. Multi-actor implications

Authority is inherently multi-actor-ready without requiring collaborative infrastructure now.

Key rules:

- Accountless Person may hold domain Authority;
- asymmetric guardian/manager/caregiver/specialist Authority can exist when bounded/contextual;
- relationship existence does not automatically create Authority;
- Responsibility and Participation do not create Authority;
- Authority does not create Visibility;
- Authority can be contested or partially known;
- access revocation does not erase historical attribution;
- no per-user duplicate shared reality is required.

---

# 17. AI boundary

AI reasoning capability does not create Authority.

AI may:

- propose changes;
- rank options;
- prepare decisions;
- suggest responsibility transfer;
- suggest scheduling/resource actions;
- explain applicable policy where authorized.

AI must not silently:

- exceed the applicable Authority made available by its acting Principal/context/policy;
- convert access to information into disclosure Authority;
- convert inference into established Authority;
- establish a human Confirmation/Acceptance;
- enact a shared-domain effect merely because it can reason about it.

Canonical rule:

> **AI effective Authority must not silently exceed the granted/applicable scope.**

---

# 18. Simple UI versus kernel semantics

Ordinary personal UX may hide Authority completely.

A personal object can be self-governed by a simple product policy without displaying roles/grants.

But the kernel must not encode:

```text
creator_id = owner_id = authority_id = account_id
```

as universal truth.

Shared, caregiver, external, specialist, and AI workflows require the boundaries to remain distinct.

---

# 19. Relationship-modeling implication

Authority confirms Relationship v0.

Simple cases may be direct/derived from bounded policy/context.

Rich cases may require a specific qualified Authority relation/context containing material scope, basis, effective period, delegation, or history.

```text
qualified Authority
!= independent entity automatically
```

Query frequency, many-to-many cardinality, permission-check pressure, or row IDs do not create domain identity.

No universal `Relationship` or `Authority` root is required.

---

# 20. Core invariants

1. **Authority is contextual scoped governance relation/capability, not native identity.**
2. **Authority to do X != Authority to do Y.**
3. **Actor != Authority.**
4. **Person/Account/Principal != Authority.**
5. **Domain Authority != technical authorization.**
6. **Responsibility != Authority.**
7. **Participation != Authority.**
8. **Visibility != Authority.**
9. **Confirmation != Authority.**
10. **Ownership != Authority.**
11. **Authority does not establish truth/Actual by itself.**
12. **Delegation is bounded to the delegated Authority; re-delegation is not implied.**
13. **Current Authority != historical Authority at action time.**
14. **Revoked/expired Authority != never existed.**
15. **Claimed Authority != established Authority.**
16. **Authority unknown != explicit no-Authority/prohibition.**
17. **Authority grants no automatic Visibility/disclosure rights.**
18. **AI reasoning/access does not manufacture Authority.**
19. **No universal admin role / Permission object / Authority root is pre-approved.**
20. **Exact persistence and enforcement belong to later logical/security design.**

---

# 21. Adjacent Dependency Sweep

## RESOLVED

- Authority ↔ Actor: agency != governance power.
- Authority ↔ Person/Account: identity/access identity != Authority.
- Authority ↔ Responsibility: accountability != governance.
- Authority ↔ Participation: involvement != governance.
- Authority ↔ Visibility boundary: access/disclosure != governance.
- Authority ↔ Confirmation: attestation != governance power.
- Authority ↔ ownership: may be basis, never universal equality.
- Authority ↔ creator/organizer: creation/organization != automatic Authority.
- Authority ↔ technical Permission: domain governance != current enforcement permission.
- Authority ↔ Delegation: bounded Authority-establishment/entrustment pattern, not universal root.

## SAFE DEFERRED

### Principal / enforcement model

**Owner:** security/logical model.  
**Why safe:** domain Authority and technical request authorization are explicitly separate.  
**Reopening trigger:** LifeOS cannot enforce a domain Authority decision without collapsing Actor/Account/Principal.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, MA-01, MA-17, XCON-01.

### Acceptance / Acknowledgement

**Owner:** common-ground review.  
**Why safe:** willingness/receipt remains independent from Authority.  
**Reopening trigger:** Responsibility/Participation changes require Authority to absorb participant willingness.  
**Tests to rerun:** CORE-04, MA-03, MA-05, MA-06, XCON-04.

### Decision / Approval / effective canonical change

**Owner:** Decision review.  
**Why safe:** Authority answers who may cause an effect, not how the Decision/effect record is represented.  
**Reopening trigger:** an authoritative action cannot be represented without making Authority itself the Decision.  
**Tests to rerun:** CORE-02, CORE-04, CORE-09, MA-06, MA-12, XCON-03.

### Detailed delegation / on-behalf-of

**Owner:** Principal/delegation review.  
**Why safe:** bounded delegation semantics are fixed.  
**Reopening trigger:** attribution/grant/revocation cannot preserve scope/history.  
**Tests to rerun:** CORE-02, MA-01, MA-06, MA-10, MA-11, MA-13, MA-17.

### Consent

**Owner:** Visibility/privacy/common-ground review.  
**Why safe:** consent may establish/limit some Authority or access but is not Authority.  
**Reopening trigger:** privacy/action governance cannot be expressed without merging Consent into Authority.  
**Tests to rerun:** CORE-04, MA-06, MA-07, MA-13, XCON-02.

### Policy / Role / conditions

**Owner:** logical/security/policy model.  
**Why safe:** current semantics need a valid bounded basis/scope, not a universal Role ontology.  
**Reopening trigger:** ordinary Authority cannot be derived/reconstructed without one canonical policy primitive.  
**Tests to rerun:** CORE-03, CORE-04, CORE-10, CORE-13.

### Qualified Authority identity / persistence

**Owner:** logical data model.  
**Why safe:** rich grants/delegations may need structure/history without proving universal Authority identity.  
**Reopening trigger:** direct/derived/qualified Authority cannot preserve revocation/history/scope.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

No current dependency is a structural blocker.

---

# 22. Rejected alternatives

Rejected:

- Authority = Actor;
- Authority = Account/Principal;
- Authority = Responsibility;
- Authority = Participation;
- Authority = Visibility;
- Authority = ownership;
- Authority = Confirmation;
- Authority = technical Permission;
- universal administrator flag;
- universal Authority entity/root;
- unbounded delegation;
- AI authority laundering;
- current Authority applied retroactively to historical actions.

---

# 23. Reopening triggers

Reopen Authority v0 if later evidence shows that:

1. domain governance and technical authorization cannot remain separated without contradiction;
2. a common Authority identity/lifecycle is required across families rather than contextual capability;
3. delegation cannot preserve bounded scope/history without a stronger primitive;
4. Visibility/Consent/Decision semantics require Authority to absorb another distinct question;
5. specialist/external Authority cannot coexist with LifeOS governance without duplicate truth;
6. logical persistence proves direct/derived/qualified Authority cannot preserve required history/revocation.

Until then, Authority remains canonical **cross-cutting contextual governance relation/capability**, not entity/root.

---

# 2026-08-12 — Acknowledgement / generic Acceptance closure amendment

Acknowledgement v0 resolves the common-ground dependency that Authority v0 intentionally left open.

```text
Acknowledgement
= explicit actor-scoped taking-notice of a specific target/material version/change/request
```

Authority remains the distinct governance/effect question:

```text
Acknowledgement != Authority
family-specific accepted response != Authority
```

Representative hand-off:

```text
request delivered/read
→ Acknowledgement
→ role-specific positive response
→ applicable manager/policy/Authority effect
```

The joint review also rejected generic cross-domain `Acceptance` as a standalone kernel primitive. Positive response remains owned by Participation, Responsibility, proposal/effect, or another independently validated family.

The historical `Acceptance / Acknowledgement` SAFE DEFERRED item is now downstream-closed as:

```text
Authority ↔ Acknowledgement             RESOLVED
Authority ↔ family-specific acceptance  RESOLVED
```

Decision/Approval/effective canonical change, Principal/enforcement/detailed delegation, Agreement/Consent, Policy/Role conditions and qualified Authority persistence remain independently owned dependencies. No Authority reopening is required.

---

# 2026-08-13 — Decision / Approval / effective-change closure amendment

Decision v0 resolves the previously deferred `Decision / Approval / effective canonical change` boundary without changing Authority semantics.

Current canonical separation:

```text
Authority
= who/what may legitimately make a bounded governed effect effective

Decision
= what bounded question was resolved to what result

Effective target state
= owned by the affected domain concept
```

Therefore:

```text
Decision != Authority
Approval != Authority
Authority != Decision record/result
Authority != effective state itself
```

Approval is now classified as **scoped Decision/review-result semantics**. An Approval may exercise or depend on Authority, but the existence of an Approval does not create Authority, and satisfying an approval requirement does not itself prove that the governed target state has already changed.

A material target/version change does not inherit prior Approval/Decision automatically. Decision time, effective-change time and later Actual time remain separable.

Reconciliation is a process/pattern that may culminate in Decision; it is not a universal primitive. The affected concept owns the resulting transition, so no universal `EffectiveChange` root is introduced.

The historical Authority SAFE DEFERRED item is downstream-closed as:

```text
Authority ↔ Decision                     RESOLVED
Authority ↔ Approval                     RESOLVED
Authority ↔ effective target state       RESOLVED
```

Principal/enforcement/detailed delegation, Consent, Agreement, Policy/Role conditions, Version/material equivalence and qualified Authority persistence remain independently owned dependencies.

**Authority v0 verdict is unchanged. REOPEN = 0.**
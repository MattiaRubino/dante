# Authority v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Authority is the contextual governance capability through which an eligible Actor or governed role is legitimately empowered, under an applicable basis, to establish, approve, change, override, revoke, or otherwise make a bounded domain effect effective for a defined target, scope, action, and context. Authority does not create Actor identity and does not by itself imply Responsibility, Participation, Visibility, ownership, Confirmation, Acknowledgement, truth, technical access, or actual performance.**

Authority answers:

> **Who or what may legitimately make which domain effect effective, on what target, under what scope/context/basis?**

Authority is a **canonical cross-cutting governance relation/capability**, not a native entity/root and not a generic administrator identity.

---

# 1. Why Authority exists

LifeOS needs to distinguish meaningful agency from legitimate governance effect.

Examples:

- an Actor may propose a Schedule change without being allowed to make it canonical;
- a Responsibility holder may be accountable without being allowed to reassign everybody;
- a participant may respond for themselves without being able to alter other participants;
- a specialist may legitimately establish a bounded specialist state without becoming owner of the underlying Person/Asset;
- an external Person may hold domain Authority without a LifeOS Account;
- an AI may reason or propose without being authorized to enact a shared-domain change.

Without Authority semantics LifeOS would infer governance incorrectly from creator, owner, Account, Actor, Responsibility, Participation, Visibility, Confirmation, Acknowledgement, or technical permissions.

---

# 2. Contextual and scoped

Authority without an effect/target/scope is too vague.

Conceptually distinguish:

- eligible holder / Actor or governed role;
- target/context;
- action or domain effect;
- applicable scope;
- effective period where relevant;
- conditions/basis;
- delegation constraints where relevant.

This does not imply a universal Authority table or fixed physical columns.

> **Authority to do X does not imply Authority to do Y.**

---

# 3. Authority versus Actor

```text
Actor = who acted
Authority = whether that Actor was legitimately empowered to make this bounded effect effective

Actor != Authority
acting != being authorized to govern
```

A proposal may be meaningful Actor behavior without being canonical state change.

---

# 4. Authority versus Person / Account / Principal

```text
Person != Authority
Account != Authority
Principal != Authority
```

Person is human identity. Account is platform/access identity boundary. Principal remains detailed security identity. Authority is domain governance.

A Person may hold Authority without an Account. Account lifecycle must not manufacture or erase historical Authority.

---

# 5. Domain Authority versus technical authorization

```text
DOMAIN AUTHORITY
legitimate governance power in domain context

TECHNICAL AUTHORIZATION
whether an authenticated Principal/request may execute an operation now
```

Technical ability to execute X is not the same as legitimate domain Authority for X.

A system administrator may access infrastructure without gaining personal/specialist domain Authority; an authoritative Person may lack a current LifeOS Principal/access path.

---

# 6. Authority versus Responsibility

```text
Responsibility != Authority
```

Accountability does not grant automatic rights to reassign, disclose, approve, delete, or alter unrelated state.

An Authority holder may reassign Responsibility without becoming responsible for execution.

---

# 7. Authority versus Participation

```text
Participation != Authority
```

Being invited, attending, organizing, or responding does not automatically grant power to reschedule, disclose, correct another participant's state, or govern the shared object.

---

# 8. Authority versus Visibility

```text
Authority != Visibility
can see != can govern
```

Authority grants no implicit read/disclosure rights. Conversely, an Actor may approve an aggregate/consequence without seeing every private underlying source.

---

# 9. Authority versus Confirmation

```text
Confirmation != Authority
```

A Person may affirm a target without power to make it canonical for everyone. An authoritative source/process may establish state without personal Confirmation.

---

# 10. Authority versus Acknowledgement / family-specific acceptance

Acknowledgement records explicit taking-notice. Family-specific acceptance records a response/willingness where the owning workflow defines that meaning. Authority determines legitimate effect.

```text
Acknowledgement != Authority
family-specific accepted response != Authority
```

Examples:

```text
recipient acknowledges a Responsibility hand-off request
!= recipient accepts the role
!= manager/policy makes transfer effective
```

```text
participant accepts invitation
!= participant may reschedule everyone
```

The Acknowledgement v0 review also rejected generic cross-domain Acceptance as a standalone primitive. Authority must therefore not absorb willingness merely because the UI uses `Accept`.

---

# 11. Authority versus truth / Actual

```text
Authority != truth
Authority != Actual
```

Authority determines legitimate effect within a governed context; it does not make a proposition objectively true.

Authoritative effects may later be corrected, contested, superseded or reconciled while preserving history.

---

# 12. Authority versus ownership

Ownership may be one possible basis in some contexts but is never universal equality.

```text
ownership != Authority
holder/custodian != Authority
steward != Authority
```

One Asset may have different owner, holder, maintenance Responsibility, scheduling Authority, repair performer and Visibility contexts.

---

# 13. Delegation

Delegation is a bounded Authority-establishment/entrustment pattern, not a standalone universal root.

Required rules:

- identify the Authority being delegated;
- one delegated Authority does not transfer every other Authority;
- delegation does not imply Visibility, Responsibility, Participation or ownership;
- re-delegation is not implied unless the governing basis permits it;
- expiry/revocation narrows future Authority without rewriting historical validity;
- current Authority != historical Authority at action time.

Detailed Principal/on-behalf-of mechanics remain deferred.

---

# 14. Approval and Decision boundary

Approval may be an action/effect that exercises Authority.

```text
Approval != Authority
```

Decision/effective-change review remains responsible for whether/how decisions, approvals, rationale, reconciliation and effective state-change records require dedicated semantics.

Authority answers **who may make the effect effective**, not what a Decision record is.

---

# 15. Authority claims and epistemic integrity

```text
claimed Authority != established/effective Authority
Authority unknown != established no Authority != explicitly prohibited
```

A security engine may fail closed without collapsing those domain meanings.

Provider role names, credentials, imported flags or asserted mandates may be Evidence/Provenance toward Authority without automatic equality.

---

# 16. Historical Authority

```text
T0 Authority exists
T1 Actor acts under it
T2 Authority expires/revokes
```

Required rules:

- revoked/expired != never existed;
- current Authority != Authority applicable at historical action time;
- current Account state does not rewrite historical Authority attribution;
- later discovery that a basis was invalid requires explicit reconciliation/correction, not silent history rewrite.

---

# 17. Multi-actor implications

Authority is multi-actor-ready without requiring collaboration infrastructure.

Key rules:

- Accountless Person may hold domain Authority;
- asymmetric guardian/manager/caregiver/specialist Authority may exist when bounded/contextual;
- relationship existence does not automatically create Authority;
- Responsibility, Participation, Visibility, Confirmation and Acknowledgement do not create Authority;
- Authority can be contested or partially known;
- access revocation does not erase historical attribution;
- no per-user duplicate shared reality is required.

---

# 18. AI boundary

AI reasoning/action capability does not create Authority.

AI may propose changes, rank options, prepare decisions, suggest Responsibility transfer, suggest scheduling/resource actions or explain policy where authorized.

AI must not silently:

- exceed applicable Authority of its acting Principal/context/policy;
- convert source access into disclosure Authority;
- convert inference into established Authority;
- fabricate human Confirmation/Acknowledgement/family response;
- enact shared-domain effect merely because it can reason about it.

> **AI effective Authority must not silently exceed the granted/applicable scope.**

---

# 19. Product simplicity

Ordinary personal UX may hide Authority completely. A personal object can be self-governed by simple product policy without displaying roles/grants.

The kernel must not encode:

```text
creator_id = owner_id = authority_id = account_id
```

as universal truth.

Shared, caregiver, external, specialist and AI workflows require the boundaries to remain distinct.

---

# 20. Relationship-modeling implication

Simple cases may be direct/derived from bounded policy/context. Rich cases may require a specific qualified Authority context containing material scope, basis, effective period, delegation or history.

```text
qualified Authority != independent entity automatically
```

Query frequency, cardinality, permission-check pressure or row IDs do not create domain identity.

---

# 21. Core invariants

1. **Authority is contextual scoped governance relation/capability, not native identity.**
2. **Authority to do X != Authority to do Y.**
3. **Actor != Authority.**
4. **Person/Account/Principal != Authority.**
5. **Domain Authority != technical authorization.**
6. **Responsibility != Authority.**
7. **Participation != Authority.**
8. **Visibility != Authority.**
9. **Confirmation != Authority.**
10. **Acknowledgement != Authority.**
11. **Family-specific accepted response != Authority.**
12. **Ownership != Authority.**
13. **Authority does not establish truth/Actual by itself.**
14. **Delegation is bounded; re-delegation is not implied.**
15. **Current Authority != historical Authority at action time.**
16. **Revoked/expired != never existed.**
17. **Claimed Authority != established Authority.**
18. **Authority unknown != explicit no-Authority/prohibition.**
19. **Authority grants no automatic Visibility/disclosure rights.**
20. **AI reasoning/access does not manufacture Authority.**
21. **No universal admin role / Permission object / Authority root is pre-approved.**
22. **Exact persistence/enforcement belongs to later logical/security design.**

---

# 22. Adjacent Dependency Sweep

## RESOLVED

- Authority ↔ Actor: agency != governance power.
- Authority ↔ Person/Account: identity/access identity != Authority.
- Authority ↔ Responsibility: accountability != governance.
- Authority ↔ Participation: involvement != governance.
- Authority ↔ Visibility: exposure != governance.
- Authority ↔ Confirmation: attestation != governance power.
- Authority ↔ Acknowledgement: explicit taking-notice != governance power.
- Authority ↔ family-specific acceptance: willingness/response != governance power.
- Authority ↔ ownership: may be basis, never universal equality.
- Authority ↔ creator/organizer: creation/organization != automatic Authority.
- Authority ↔ technical Permission: domain governance != enforcement permission.
- Authority ↔ Delegation: bounded Authority establishment/entrustment pattern, not universal root.

## SAFE DEFERRED

### Principal / enforcement model

**Owner:** security/logical model.  
**Why safe:** domain Authority and technical request authorization are explicitly separate.  
**Reopening trigger:** LifeOS cannot enforce domain Authority without collapsing Actor/Account/Principal.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, MA-01, MA-17, XCON-01.

### Decision / Approval / effective canonical change

**Owner:** Decision review.  
**Why safe:** Authority answers who may cause an effect, not how Decision/effect record is represented.  
**Reopening trigger:** authoritative action cannot be represented without making Authority itself the Decision.  
**Tests to rerun:** CORE-02, CORE-04, CORE-09, MA-06, MA-12, XCON-03.

### Detailed delegation / on-behalf-of

**Owner:** Principal/delegation review.  
**Why safe:** bounded delegation semantics are fixed.  
**Reopening trigger:** attribution/grant/revocation cannot preserve scope/history.  
**Tests to rerun:** CORE-02, MA-01, MA-06, MA-10, MA-11, MA-13, MA-17.

### Agreement / Consent

**Owner:** common-ground/privacy review.  
**Why safe:** mutual assent/permission may constrain some effects but are not Authority.  
**Reopening trigger:** action/privacy governance cannot be expressed without merging Agreement/Consent into Authority.  
**Tests to rerun:** CORE-04, MA-05, MA-06, MA-07, MA-13, XCON-02.

### Policy / Role / conditions

**Owner:** logical/security/policy model.  
**Why safe:** valid bounded basis/scope does not require a universal Role ontology now.  
**Reopening trigger:** ordinary Authority cannot be derived/reconstructed without one canonical policy primitive.  
**Tests to rerun:** CORE-03, CORE-04, CORE-10, CORE-13.

### Qualified Authority identity / persistence

**Owner:** logical data model.  
**Why safe:** rich grants/delegations may need structure/history without proving universal identity.  
**Reopening trigger:** direct/derived/qualified Authority cannot preserve revocation/history/scope.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

```text
REOPEN                         0
unclassified material items    0
```

---

# 23. Rejected alternatives

Rejected:

- Authority = Actor;
- Authority = Account/Principal;
- Authority = Responsibility;
- Authority = Participation;
- Authority = Visibility;
- Authority = ownership;
- Authority = Confirmation/Acknowledgement/family-specific acceptance;
- Authority = technical Permission;
- universal administrator flag;
- universal Authority entity/root;
- unbounded delegation;
- AI Authority laundering;
- current Authority applied retroactively to historical actions.

---

# 24. Reopening triggers

Reopen Authority v0 if later evidence shows that:

1. domain governance and technical authorization cannot remain separate;
2. one common Authority identity/lifecycle is required across families rather than contextual capability;
3. delegation cannot preserve bounded scope/history without a stronger primitive;
4. Visibility/Consent/Decision/common-ground semantics require Authority to absorb another distinct question;
5. specialist/external Authority cannot coexist with LifeOS governance without duplicate truth;
6. logical persistence proves direct/derived/qualified Authority cannot preserve required history/revocation.

Until then, Authority remains canonical **cross-cutting contextual governance relation/capability**, not entity/root.

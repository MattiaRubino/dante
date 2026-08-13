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

Decision v0 closes this boundary canonically: Approval is scoped Decision/review-result semantics whose governance significance depends on applicable Authority/policy; the resulting effective state remains owned by the affected domain concept.

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
- Agreement does not automatically create Authority;
- Consent may be one applicable basis/constraint for a bounded effect but does not manufacture general Authority;
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
- establish a human Confirmation/Acceptance/Agreement/Consent;
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

Agreement or Consent may be policy inputs/bases in some contexts without becoming Authority.

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
10. **Agreement != Authority.**
11. **Consent != Authority; Consent may be one bounded basis/constraint under applicable policy.**
12. **Ownership != Authority.**
13. **Authority does not establish truth/Actual by itself.**
14. **Delegation is bounded to the delegated Authority; re-delegation is not implied.**
15. **Current Authority != historical Authority at action time.**
16. **Revoked/expired Authority != never existed.**
17. **Claimed Authority != established Authority.**
18. **Authority unknown != explicit no-Authority/prohibition.**
19. **Authority grants no automatic Visibility/disclosure rights.**
20. **AI reasoning/access does not manufacture Authority, Agreement or Consent.**
21. **No universal admin role / Permission object / Authority root is pre-approved.**
22. **Exact persistence and enforcement belong to later logical/security design.**

---

# 21. Adjacent Dependency Sweep

## RESOLVED

- Authority ↔ Actor: agency != governance power.
- Authority ↔ Person/Account: identity/access identity != Authority.
- Authority ↔ Responsibility: accountability != governance.
- Authority ↔ Participation: involvement != governance.
- Authority ↔ Visibility boundary: access/disclosure != governance.
- Authority ↔ Confirmation: attestation != governance power.
- Authority ↔ Agreement: mutual assent != governance power.
- Authority ↔ Consent: bounded permission may be basis/constraint but != governance capability.
- Authority ↔ ownership: may be basis, never universal equality.
- Authority ↔ creator/organizer: creation/organization != automatic Authority.
- Authority ↔ technical Permission: domain governance != current enforcement permission.
- Authority ↔ Delegation: bounded Authority-establishment/entrustment pattern, not universal root.
- Authority ↔ Decision/Approval/effective target state: governance capability != resolution != resulting state.

## SAFE DEFERRED

### Principal / enforcement model

**Owner:** security/logical model.  
**Why safe:** domain Authority and technical request authorization are explicitly separate.  
**Reopening trigger:** LifeOS cannot enforce a domain Authority decision without collapsing Actor/Account/Principal.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, MA-01, MA-17, XCON-01.

### Detailed delegation / on-behalf-of

**Owner:** Principal/delegation review.  
**Why safe:** bounded delegation semantics are fixed.  
**Reopening trigger:** attribution/grant/revocation cannot preserve scope/history.  
**Tests to rerun:** CORE-02, MA-01, MA-06, MA-10, MA-11, MA-13, MA-17.

### Policy / Role / conditions

**Owner:** logical/security/policy model.  
**Why safe:** current semantics need a valid bounded basis/scope, not a universal Role ontology.  
**Reopening trigger:** ordinary Authority cannot be derived/reconstructed without one canonical policy primitive.  
**Tests to rerun:** CORE-03, CORE-04, CORE-10, CORE-13.

### Version / material equivalence

**Owner:** Version/logical model.  
**Why safe:** Authority/Decision/Consent/Agreement applicability already requires material-scope/version sensitivity where relevant.  
**Reopening trigger:** historical/current Authority basis cannot be reconstructed after material target/policy changes.  
**Tests to rerun:** CORE-02, CORE-09, CORE-10, CORE-13, MA-11, XCON-03.

### Qualified Authority identity / persistence

**Owner:** logical data model.  
**Why safe:** rich grants/delegations may need structure/history without proving universal Authority identity.  
**Reopening trigger:** direct/derived/qualified Authority cannot preserve revocation/history/scope.  
**Tests to rerun:** CORE-06, CORE-10, CORE-13, XCON-01, XCON-04.

### Consent purpose/use enforcement

**Owner:** Consent/privacy/policy/security logical model.  
**Why safe:** Consent semantics are now distinct and may constrain Authority/effect under policy without becoming Authority.  
**Reopening trigger:** enforcement requires Consent and Authority to collapse into one semantic concept.  
**Tests to rerun:** CORE-04, CORE-10, CORE-13, MA-06, MA-07, MA-13, MA-17, XCON-02.

No current dependency is a structural blocker.

---

# 22. Rejected alternatives

Rejected:

- Authority = Actor;
- Authority = Account/Principal;
- Authority = Responsibility;
- Authority = Participation;
- Authority = Visibility;
- Authority = Agreement;
- Authority = Consent;
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
4. Visibility/Consent/Agreement/Decision semantics require Authority to absorb another distinct question despite current closures;
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

---

# 2026-08-13 — Agreement / Consent downstream closure amendment

Agreement / Consent v0 closes Authority's former Agreement/Consent semantic dependencies without changing Authority.

```text
Authority
= legitimate bounded governance capability

Agreement
= multi-party mutual assent to materially same terms/version

Consent
= actor-scoped bounded permission for action/use/exposure under defined scope/purpose/context
```

Therefore:

```text
Authority ↔ Agreement  RESOLVED
Authority ↔ Consent    RESOLVED
```

Agreement may exist without Authority to make the agreed downstream effect effective. Authority may exist without mutual Agreement of all affected parties. Consent may establish or constrain a bounded basis under applicable policy, but does not create general Authority and does not imply unrelated Visibility or technical authorization.

Consent withdrawal may change future governed action/use where policy makes Consent relevant; it does not rewrite Authority/action history that was legitimate at the historical time under the applicable basis.

Generic Assent/Acceptance remains rejected. Principal/enforcement/detailed delegation, Policy/Role conditions, Version/material equivalence, qualified Authority persistence and purpose/use enforcement remain separately SAFE DEFERRED.

No Authority hardening failed; **Authority remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `agreement.md`;
- `consent.md`;
- `../checkpoints/agreement-consent-v0-validation.md`.

---

# 2026-08-13 — Representation / delegation downstream closure amendment

Representation v0 closes Authority's previously deferred detailed on-behalf-of semantic boundary without changing Authority itself.

Canonical separation:

```text
Actor
= who/what actually acts semantically

Representation / on-behalf-of
= actual Actor acts for a distinct represented party for a bounded action/context

Authority
= whether that Actor/role may legitimately make the bounded governed effect effective

Principal
= technical security identity used for request authentication/authorization
```

Therefore:

```text
Representation != Authority
represented party != Authority holder automatically
Principal != Authority
claim of Representation != established Authority
```

Delegation remains **bounded Authority-establishment / entrustment semantics** rather than a universal root. The delegated scope names the Authority/action being entrusted; it does not transfer all Authority, Responsibility, Visibility, Agreement/Consent capacity or re-delegation rights.

The former `Detailed delegation / on-behalf-of` SAFE DEFERRED item is now:

```text
Representation / on-behalf-of semantic relation   RESOLVED
Delegation universal primitive                    REJECTED
exact Principal/AuthN/AuthZ enforcement            SAFE DEFERRED
specific delegation-policy mechanics               SAFE DEFERRED
legal/specialist representation validity           SAFE DEFERRED
multi-hop re-delegation persistence                 SAFE DEFERRED
```

Historical action-time Authority remains reconstructible after expiry/revocation. A later invalid action can preserve the attempted Representation attribution without making the attempted effect legitimate.

No Authority hardening failed. **Authority remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `representation.md`;
- `../checkpoints/representation-delegation-principal-v0-validation.md`.

---

# 2026-08-13 — Version / Material-State downstream closure amendment

Version / Material-State v0 resolves Authority's former `Version / material equivalence` SAFE DEFERRED dependency without changing Authority semantics.

Where Authority depends on a materially specific target/scope/policy/basis state, historical legitimacy must be evaluated against the state that actually applied at action time:

```text
Authority basis/policy state B1
Actor acts at T1 under B1
later material state B2 narrows/revokes scope
→ T1 is evaluated under B1
→ B2 does not rewrite T1 as though B1 never existed
```

Conversely a materially changed policy/target state does not silently inherit old Authority scope merely because target identity or technical access remains the same.

Materiality is purpose/scope specific. Technical row versions, provider revision IDs, ETags/MVCC tokens, content hashes or `updated_at` values do not define domain Authority applicability.

Canonical separation:

```text
Version != Authority
Version != technical authorization
Version != Decision / reconciliation
Version != Provenance
current Authority state != historical Authority state at action time
```

Version supplies reconstructible state binding; Authority still answers who/what may legitimately govern the bounded effect. The owning domain + Authority/Decision/policy still determine effective state.

Remaining SAFE DEFERRED Authority dependencies include exact Principal/AuthN/AuthZ enforcement, Policy/Role/conditions, qualified Authority persistence, Consent purpose/use enforcement, specific delegation-policy mechanics and specialist validity.

AI/system effective action must preserve/re-evaluate its material Authority/policy base state where consequence requires it; a materially changed basis cannot be ignored merely because the technical Principal can still issue a request.

No Authority hardening failed. **Authority remains PASS WITH HARDENING, REOPEN = 0**.

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

---

# 2026-08-13 — Reconciliation / Source Precedence downstream closure amendment

Reconciliation v0 resolves Authority's conflict/source-precedence dependency without changing Authority semantics.

Canonical separation:

```text
Authority
= legitimate bounded power to make a governed effect effective

Reconciliation
= contextual process/capability for handling materially competing states/assertions

Source Precedence
= bounded contextual policy/basis where justified
```

Authority may be one input/basis used by Reconciliation, but it is not objective truth and does not create a universal source hierarchy. An authoritative specialist source may have precedence only for the target/facet/purpose/context/time for which that Authority actually applies.

Reconciliation may remain unresolved when applicable Authority/policy is insufficient or contested. Where an already-authorized deterministic rule establishes a result, no fabricated human Decision is required. Where judgment/resolution is material, a Decision may occur separately.

The affected domain concept still owns the resulting current/effective state. Later correction/reversal preserves prior Authority-at-action-time and resolution history.

Technical access, Principal identity, provider role names, source recency and creator status do not become Authority or source precedence automatically. Conflict/basis/rationale Visibility remains independently governed.

Downstream classification:

```text
Authority ↔ Reconciliation       RESOLVED
Authority ↔ Source Precedence    RESOLVED — bounded basis only
Authority ↔ objective truth      RESOLVED — not equal
```

Exact Principal/AuthN/AuthZ enforcement, Policy/Role/conditions, specialist validity, retention/audit and physical representation remain independently SAFE DEFERRED.

No Authority hardening failed. **Authority remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `reconciliation.md`;
- `../checkpoints/reconciliation-source-precedence-v0-validation.md`.
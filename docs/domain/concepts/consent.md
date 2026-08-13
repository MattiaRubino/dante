# Consent v0

**Status:** Current accepted candidate pending post-write QA  
**Reviewed:** 2026-08-13  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Consent is the contextual actor-scoped permission relation/declaration through which an eligible consent-giver explicitly permits a bounded action, exposure, use, processing or interaction concerning a defined target/subject for a defined scope, purpose and context where Consent is an applicable basis. Consent records that permission state; it does not by itself prove legal validity, create Authority or Visibility, execute the permitted action, or prove compliance with its scope.**

Consent answers:

> **Who explicitly permitted what bounded action/use/exposure concerning what target, for which scope/purpose/context?**

Consent is therefore a **specific contextual actor-scoped permission relation/capability**, not a universal Permission entity, not technical authorization and not a legal-validity engine.

---

# 1. Why Consent exists

LifeOS needs a semantic boundary between information/action capability and a person's own bounded permission.

Examples include:

- permit free/busy exposure for one trip-planning purpose without sharing underlying events;
- permit a caregiver to receive selected practical information without broad medical visibility;
- permit use of a portrait for one publication context without agreeing to every future use;
- permit a trusted helper to perform a bounded action without transferring all Authority;
- withdraw future consent while preserving historical facts about prior authorized disclosure/use.

Without Consent semantics LifeOS would be pushed toward false equivalences:

```text
Visibility = Consent
Authority = Consent
technical Permission = Consent
Agreement = Consent
membership = Consent
silence = Consent
```

All fail ordinary privacy and multi-actor cases.

---

# 2. Consent is actor-scoped and explicit

Consent belongs to an eligible consent-giver in context.

```text
Consent by Actor A
!= Consent by Actor B
!= group Consent automatically
```

Canonical rule:

> **Silence, delivery, read state, Acknowledgement, behavioral inference, relationship membership or continued participation do not establish Consent by themselves.**

Where a specialist/legal regime requires stronger validity conditions, LifeOS must not claim those conditions merely because a Consent record exists.

---

# 3. Action / use / exposure scope

Consent is not meaningful as an unbounded `yes`.

It must be able to distinguish the bounded thing permitted, for example:

```text
view free/busy
share one document
use one image
process one category of data
perform one interaction
contact one provider
```

Canonical rule:

> **Consent to action/use/exposure X does not imply Consent to unrelated action/use/exposure Y.**

Exact action taxonomy remains downstream policy/logical-model work.

---

# 4. Purpose / context scope

Consent may be purpose-sensitive where the reason for use materially changes what the actor permitted.

Example:

```text
Consent:
use free/busy projection
purpose: coordinate Trip A
```

must not silently become:

```text
use full private calendar history
purpose: unrelated analytics / AI training
```

Canonical rule:

> **Consent for purpose/context A does not silently cover materially different purpose/context B.**

This does not make every LifeOS action purpose-tagged; consequence determines whether purpose is a material part of Consent semantics.

---

# 5. Target / subject / material-version scope

Consent may concern a Person, Asset, information projection, relationship, action or other bounded target.

Material changes can invalidate prior applicability.

```text
Consent C1 applies to terms/scope v1
materially expanded scope v2
→ C1 does not automatically apply
```

Exact material-equivalence/version mechanics remain deferred.

---

# 6. Consent versus Visibility

Visibility answers:

> **What bounded information may this recipient context be exposed to?**

Consent answers:

> **What bounded action/use/exposure did this actor explicitly permit for this scope/purpose/context?**

Therefore:

```text
Consent != Visibility
```

Consent can exist before any exposure actually occurs.

Visibility may also exist under another applicable legitimate basis in contexts where Consent is not the relevant basis.

Canonical rule:

> **Consent may be one basis/constraint for Visibility or use; it is not the resulting exposure capability itself.**

---

# 7. Consent versus Authority

Authority is legitimate bounded governance power.

Consent is a bounded permission declaration by the consent-giver.

```text
Consent != Authority
```

Consent may establish or constrain some Authority under applicable policy, but it does not manufacture general governance power.

A manager/guardian/specialist may hold bounded Authority in a context without that implying unrestricted Consent from every affected person.

---

# 8. Consent versus technical authorization

Technical authorization asks whether a request/Principal may execute an operation now.

Consent is domain/privacy permission semantics.

```text
Consent != technical Permission
Consent != Principal
```

The system may enforce a Consent-derived rule technically, but storage/enforcement architecture is downstream.

---

# 9. Consent versus Agreement

Agreement is multi-party mutual assent to shared terms.

Consent is actor-scoped bounded permission.

```text
Agreement != Consent
```

Examples:

```text
service terms agreed
+
separate image-use Consent absent
```

and:

```text
Anna consents to bounded free/busy exposure
without reciprocal Consent from recipient
```

One does not manufacture the other.

---

# 10. Consent versus Decision

Decision records a bounded resolution.

Consent records permission by a consent-giver.

```text
Consent != Decision
```

A Decision can resolve whether to proceed under policy after checking Consent, but the Decision does not become the person's Consent.

An actor can withdraw Consent even though an earlier Decision historically existed.

---

# 11. Consent versus Acknowledgement / Confirmation / family response

```text
Acknowledgement != Consent
Confirmation != Consent
Participation response != Consent
Responsibility hand-off response != Consent
```

Taking notice, affirming a target, intending to participate or accepting a role does not universally authorize unrelated use/disclosure.

UI words such as `Accept`, `Allow`, `Agree`, `Continue` must map to the actual semantic action rather than automatically creating Consent.

---

# 12. Lifecycle / withdrawal / revocation

Consent is lifecycle-sensitive where material.

```text
T0 Consent granted
T1 permitted disclosure/use occurs
T2 Consent withdrawn for future use
```

At T2:

```text
current future permission = withdrawn/absent as applicable
```

but not:

```text
T0 never happened
T1 disclosure/use never happened
recipient forgets information already learned
```

Canonical rule:

> **Withdrawal/revocation changes future applicability; it does not silently rewrite legitimate historical Consent, disclosure, use or knowledge.**

Exact retention/deletion effects remain privacy/retention work.

---

# 13. Unknown / absent / refused

These semantic states must not collapse:

```text
Consent unknown
!= no applicable Consent found
!= explicit refusal
!= withdrawn prior Consent
```

Technical policy may fail closed without turning enforcement defaults into stronger domain claims.

---

# 14. Legal validity / capacity / coercion boundary

A LifeOS Consent record does not prove legal, medical or regulatory validity.

Potential specialist factors include:

- capacity;
- age;
- coercion / power imbalance;
- jurisdiction;
- information requirements;
- formality/signature;
- legal basis other than Consent.

Canonical rule:

> **LifeOS records bounded consent semantics where applicable; it does not certify universal legal validity.**

Specialist systems may remain authoritative sources for regulated consent state.

---

# 15. Unequal power

Manager/employee, guardian/minor, caregiver/vulnerable-person and similar relationships require caution.

LifeOS must not silently interpret:

```text
clicked acknowledgement
continued using system
complied with instruction
relationship membership
```

as freely given Consent.

Where voluntariness or legal validity matters, specialist/product policy must establish that separately.

---

# 16. Assisted / on-behalf-of Consent

The actor interacting with LifeOS may differ from the Person whose Consent is at stake.

Where material preserve:

- actual acting Actor;
- represented Person/party;
- applicable Authority/delegation/basis;
- Provenance of the declaration;
- target/scope/purpose/version.

Canonical rule:

> **A helper operating the interface must not silently become the represented person's personal Consent.**

Exact Principal/delegation mechanics remain deferred.

---

# 17. Consent Visibility / privacy

Consent records can themselves be sensitive.

```text
Visibility(target)
!= Visibility(Consent record/history)
```

A recipient may be permitted to know the operational result while not seeing every private reason, source or historical consent detail.

Consent grants no automatic right to re-disclose its contents.

---

# 18. AI / Context Builder boundary

AI may:

- check whether an applicable Consent exists where authorized;
- request explicit Consent through a bounded interaction;
- use consented context within scope;
- generate a safe projection without exposing private reasons.

AI must not:

- infer human Consent from behavior, probability or silence;
- expand purpose/scope because broader context would improve a recommendation;
- convert source access into disclosure permission;
- fabricate Consent for a represented person;
- treat AI recommendation or user Acknowledgement as Consent;
- leak private reasons through explanations or tool-call arguments.

Canonical rule:

> **AI informational access and inference capability do not create or enlarge human Consent.**

---

# 19. Simple UI versus kernel semantics

Ordinary UI may say:

```text
Allow
Share for this trip
Use for scheduling
Stop sharing
```

rather than exposing ontology terms.

The UI must still preserve the underlying material scope/purpose where consequence requires it.

High-consequence or specialist flows may expose recipient, action, target, scope, purpose, period, history and basis through progressive disclosure.

---

# 20. Relationship-modeling implication

Consent follows Relationship v0 discipline.

Simple bounded permission may be represented directly/derived where semantics remain complete.

Rich cases may require a qualified Consent context carrying material target/action/purpose/scope/lifecycle/provenance/history.

```text
qualified Consent != native entity/root automatically
```

No universal Permission/ACL/Consent root is pre-approved.

---

# 21. Core invariants

1. **Consent is contextual actor-scoped permission semantics, not native identity.**
2. **Consent is explicit; silence/behavior/inference do not establish it by themselves.**
3. **Consent is bounded by action/use/exposure and target.**
4. **Purpose/context is part of Consent where materially relevant.**
5. **Consent for X != Consent for Y.**
6. **Consent for purpose A != purpose B after material change.**
7. **Material target/scope/version change does not inherit prior Consent automatically.**
8. **Consent != Visibility.**
9. **Consent != Authority.**
10. **Consent != technical authorization/Permission.**
11. **Consent != Agreement.**
12. **Consent != Decision.**
13. **Consent != Acknowledgement/Confirmation/family-specific response.**
14. **Consent does not prove permitted action/use actually occurred.**
15. **Withdrawal/revocation does not rewrite legitimate history.**
16. **No current Consent != explicit refusal by default.**
17. **Membership/relationship/Participation does not imply Consent.**
18. **Assisted/on-behalf-of Consent preserves actor/represented-party/basis.**
19. **AI may not infer/fabricate/enlarge human Consent.**
20. **A LifeOS Consent record does not prove legal validity/capacity.**
21. **Consent history has independent Visibility/privacy requirements.**
22. **Consent workflows remain consequence-sensitive and specialist-aware.**
23. **No universal Permission or legal-consent engine is accepted.**
24. **Exact policy/enforcement/persistence belongs downstream.**

---

# 22. Adjacent Dependency Sweep

## RESOLVED

- Consent ↔ Acknowledgement: taking notice != permission.
- Consent ↔ generic/family response: willingness in another workflow != permission for unrelated use.
- Consent ↔ Agreement: mutual terms != actor-scoped permission.
- Consent ↔ Decision: permission != bounded resolution.
- Consent ↔ Authority: permission != governance capability.
- Consent ↔ Visibility: permission/basis != resulting exposure capability.
- Consent ↔ downstream use: scope/purpose semantics are distinct from actual use/enforcement.
- generic Assent/Acceptance root: rejected.

## SAFE DEFERRED

### Principal / delegation / representation

**Owner:** Principal/delegation/security review.  
**Why safe:** acting Actor, represented party and applicable basis already remain distinct.  
**Reopening trigger:** on-behalf-of Consent cannot preserve attribution without identity/Authority collapse.  
**Tests:** CORE-02/06/09/13, MA-01/06/10/11/13/17, XCON-01/02.

### Version / material scope

**Owner:** Version + logical model.  
**Why safe:** material scope/version applicability is already mandatory.  
**Reopening trigger:** system cannot determine whether prior Consent remains applicable after change.  
**Tests:** CORE-02/09/10/13, MA-11/12, XCON-03.

### Consent validity / capacity / legal basis

**Owner:** specialist/legal/product policy.  
**Why safe:** LifeOS explicitly claims no universal legal-validity proof.  
**Reopening trigger:** product must itself establish regulated consent validity.  
**Tests:** CORE-03/04/09/12, MA-06/10/13/18, XCON-02.

### Purpose/use enforcement

**Owner:** privacy/policy/security/logical model.  
**Why safe:** scope/purpose semantics are fixed independently from enforcement.  
**Reopening trigger:** enforcement requires Consent to collapse into Visibility/Authority/technical Permission.  
**Tests:** CORE-04/10/13, MA-06/07/08/17, XCON-02/04.

### Collective/group consent

**Owner:** collective/group semantics.  
**Why safe:** one Actor's Consent does not imply collective Consent.  
**Reopening trigger:** ordinary workflows require collective consent identity/quorum independent from individual declarations.  
**Tests:** CORE-04/06/12, MA-01/02/05/13/19/20, XCON-01/04/05.

### Retention/deletion

**Owner:** privacy/retention.  
**Why safe:** history requirement does not imply indefinite source-payload retention.  
**Reopening trigger:** deletion/privacy rules conflict with required historical proof/reconstruction.  
**Tests:** CORE-02/09, MA-07/11/13, XCON-03.

No current dependency requires structural reopening.

---

# 23. Reopening triggers

Reopen Consent v0 if later evidence shows that:

1. bounded permission can be fully represented through Visibility/Authority/policy without semantic loss;
2. purpose/use semantics prove inseparable from another accepted primitive;
3. on-behalf-of attribution cannot be preserved without changing Consent semantics;
4. regulated validity/capacity requirements must become first-class LifeOS domain semantics rather than specialist boundaries;
5. Version/persistence cannot preserve Consent applicability and withdrawal history;
6. product evidence shows explicit Consent structure creates more risk/burden than value in ordinary LifeOS coordination.

Until then Consent remains the current specific contextual actor-scoped permission relation/capability.
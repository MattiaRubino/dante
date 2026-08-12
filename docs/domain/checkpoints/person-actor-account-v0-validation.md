# Person / Actor / Account v0 — Validation Checkpoint

**Status:** PASS WITH HARDENING — accepted current baseline  
**Validated:** 2026-08-12  
**Validation standard:** Domain Validation Methodology v3  
**Cluster:** Data / Subjects  
**Branch:** `feature/domain-model`

## 1. Scope

- Candidate set: Person / Actor / Account boundary
- Accepted semantic outcomes:
  - Person = canonical native human-identity entity;
  - Actor = canonical semantic agency role/capability, not entity/root;
  - Account = real platform/access identity boundary, distinct from Person and Actor;
  - User = product/implementation term, not domain primitive;
  - Principal = SAFE DEFERRED security/authority concept.
- Why this review exists: LifeOS must support non-account humans, historical attribution, software/AI agency, caregiver scenarios, external participants, credential changes, and future multi-actor authority without building the kernel around `users.id`.

---

# 2. Evidence reviewed

## Internal

Reviewed:

- Subject v0 and its native-referent role model;
- Observation v0 subject/observer/recorder/source separation;
- Provenance v0 actor/source/transformer lineage boundaries;
- Multi-Actor Readiness v1;
- caregiver, child, external participant, employee/manager, account deletion, provider change, automation, integration and AI scenarios;
- accepted Account != Person direction from prior multi-actor work.

## External benchmark evidence

External products/standards were used as benchmark evidence only.

| Pattern | Useful lesson | Classification |
|---|---|---|
| Person/contact/profile systems | human identity can be distinct from account/contact/source representations | ADAPT |
| health/interoperability Person patterns | same human may persist across multiple role-specific/digital representations | ADAPT |
| provenance agent patterns | agency may belong to Person, Organization, software/service etc. | ADAPT |
| OpenID/OAuth-style subject/security identifiers | authentication identifiers are scoped security/account identifiers, not global real-human identity | ADAPT |
| SCIM/account provisioning patterns | service `User`/account resources represent service access/provisioning lifecycle | ADAPT |
| identity-provider account linking | several provider identities can map to one application account/profile only after reconciliation/linking | ADAPT |
| `users.id` as universal Person/Actor/Subject identity | collapses real human, access and agency lifecycles | ANTI-PATTERN |
| universal Actor superclass/entity | duplicates native identity merely for common references | ANTI-PATTERN |

---

# 3. Candidate definitions

## Person

> **A Person is a persistent native representation of a human individual in LifeOS reality whose identity is independent of Accounts, credentials, contact/profile representations, participation, Subject roles, Actor roles, responsibility, authority, visibility, and current access to LifeOS.**

Classification: **CANONICAL NATIVE ENTITY**.

## Actor

> **Actor is the contextual semantic role/capability of a native referent or system when agency for an action, assertion, transformation, proposal, confirmation, participation, or other meaningful behavior is attributed to it. Actor does not create independent identity and does not by itself imply responsibility, authority, ownership, Account identity, Principal identity, participation, or any specific action role.**

Classification: **CANONICAL SEMANTIC AGENCY ROLE / CAPABILITY**; no independent Actor entity/root.

## Account boundary

> **Account is an application/platform access or membership identity through which LifeOS usage can be authenticated and managed. Account identity does not define Person identity, Subject identity, or Actor identity.**

Classification: **REAL PLATFORM / ACCESS IDENTITY BOUNDARY; detailed Account/auth schema deferred**.

## User

Product/implementation language only; no kernel primitive.

## Principal

Authenticated/authorized security identity semantics are SAFE DEFERRED to Authority/security modeling.

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | Yes | self-use, caregiver, external participant, AI/service action | PASS | simple UI can still hide distinctions while kernel remains correct |
| CORE-02 Deep chronology | Yes | Person exists before Account, changes provider, Account later deleted | PASS WITH HARDENING | historical Person/Actor attribution must survive access changes where policy permits |
| CORE-03 Reductio | Yes | remove/merge Person-Account-Actor; universal User/Actor root | PASS | Person and agency semantics survive; universal roots fail |
| CORE-04 Redundancy | Yes | Person vs Subject/Actor/Account/Principal | PASS | each answers different identity/agency/security question |
| CORE-05 Traceability | Yes | caregiver records another Person under own Account | PASS | Person/Actor/Account context remains reconstructable |
| CORE-06 Orphan/independence | Yes | non-account Person; software Actor; Account holder not current Actor | PASS | independent existence/roles demonstrated |
| CORE-07 External benchmark | Yes | identity/contact/provenance/auth patterns | PASS WITH HARDENING | adapt separation; do not inherit external taxonomies |
| CORE-08 Anti-pattern review | Yes | `users.id` universal root; synthetic Accounts; Actor wrapper entity | PASS | rejected explicitly |
| CORE-09 Correction/reconciliation/epistemic integrity | Yes | duplicate contacts/person match, wrong identity merge, provider relink | PASS WITH HARDENING | identity resolution/merge must preserve material history |
| CORE-10 Scale/performance/history | Yes | many contacts/accounts/source identities/actor references | PASS WITH HARDENING | typed-reference/identity-map physical shape deferred |
| CORE-11 Simple vs power user | Yes | self-use vs caregiver/admin/history | PASS | distinctions may remain invisible in simple UI |
| CORE-12 Product value/complexity cost | Yes | ordinary personal workflow | PASS | no additional visible Actor/User objects required |
| CORE-13 Implementation pressure | Yes | auth IDs, historical attribution, service identities | PASS WITH HARDENING | Account/Principal schema deliberately deferred |

Core Gate verdict: **PASS WITH HARDENING**.

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | Yes | non-account Person, later Account creation | PASS | Person identity explicitly independent |
| MA-02 Shared canonical fact / actor overlay | Yes | one shared Person referenced by several actors | PASS WITH HARDENING | no per-account Person duplication; identity linkage still privacy-scoped |
| MA-03 Responsibility/assignment/claim | Yes | performer vs accountable actor | PASS | Actor does not absorb Responsibility |
| MA-04 Stewardship/mental load | Yes | caregiver/manager coordination | PASS | Actor/Person identity does not imply stewardship |
| MA-05 Common ground/state separation | Yes | different actors assert facts about one Person | PASS | one Person identity does not create one shared opinion/state |
| MA-06 Authority/canonical change | Yes | account holder acts without automatic authority | PASS WITH HARDENING | agency/authentication != authority |
| MA-07 Selective disclosure | Yes | Person linkage and Actor attribution may be sensitive | PASS WITH HARDENING | visibility remains separate |
| MA-08 Inference privacy | Yes | identity matching across contexts | PASS WITH HARDENING | inferred same-Person linkage is not disclosure permission |
| MA-09 Partial adoption/external participant | Yes | external Person without Account | PASS | ordinary supported case |
| MA-10 Assisted participation/provenance | Yes | caregiver uses own Account for another Person | PASS | Person/Actor/Account roles remain reconstructable |
| MA-11 Relationship lifecycle/revocation | Yes | Account deleted/revoked after historical action | PASS | current access != historical attribution |
| MA-12 Conflict/adversarial relationship | Yes | disputed identity/action attribution | PASS WITH HARDENING | conflicts may remain unresolved pending reconciliation |
| MA-13 Unequal power | Yes | guardian/caregiver/manager | PASS WITH HARDENING | power does not collapse Person, Actor, Account or Authority |
| MA-14 Multi-resource/capacity | Limited | Person may later also be Resource | PASS | role composition allowed |
| MA-15 Coordination-burden distribution | Yes | actor performing vs steward coordinating | PASS | no burden inference from agency |
| MA-16 Formality/progressive disclosure | Yes | personal UI vs admin/security detail | PASS | internal distinctions need not surface routinely |
| MA-17 AI authority/multi-party context | Yes | AI/service acts on behalf of human | PASS WITH HARDENING | Actor/Principal/delegation/Authority remain separable |
| MA-18 Specialist-system boundary | Yes | external identity/auth/contact systems | PASS | adapters map source identities without owning Person truth |
| MA-19 Multi-actor primitive redundancy | Yes | universal User/Actor entity | PASS | rejected |
| MA-20 Actor-scoped reality attribution | Yes | Person A Subject; Person B recorder; Account B authenticates | PASS | distinct roles preserved |

Multi-Actor Gate verdict: **PASS WITH HARDENING**.

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | Yes | PASS WITH HARDENING | Person native identity; Actor role; Account access identity; no wrapper identity |
| XCON-02 Ownership/authority compatibility | Yes | PASS | none of Person/Actor/Account automatically establishes Authority/ownership |
| XCON-03 Planned/current/actual/history compatibility | Yes | PASS | Account lifecycle does not rewrite historical Person/Actor attribution |
| XCON-04 Relationship compatibility | Yes | PASS WITH HARDENING | typed roles must later express performer/recorder/delegation rather than generic Actor edge |
| XCON-05 Multi-actor readiness compatibility | Yes | PASS | non-account humans and service actors supported |
| XCON-06 Language-map compatibility | Yes | PASS | User stays product/implementation term |

Cross-Concept Gate verdict: **PASS WITH HARDENING**.

---

# 7. Adversarial reductio

## REMOVE Person

Human identity is forced into Account/contact/Subject/Actor roles and breaks non-account/history scenarios.

**Result:** FAIL.

## Person = Account

Non-account humans and account lifecycle fail.

**Result:** FAIL.

## Person = Actor

Passive humans and non-human/software actors fail.

**Result:** FAIL.

## Account = Actor

Service/external actors and semantic action attribution fail; authentication is confused with action.

**Result:** FAIL.

## Account = Person

Provider/access lifecycle becomes human identity.

**Result:** FAIL.

## Actor as universal entity/root

Native Person/system identities are duplicated to create a common FK/root.

**Result:** FAIL.

## User as universal kernel concept

UI/auth terminology absorbs Person, Actor, Account, Principal and participation semantics.

**Result:** FAIL.

## Person native entity + Actor contextual role + Account separate access identity

All tested workflows remain representable with bounded concepts.

**Result:** PASS.

---

# 8. Adjacent Dependency Sweep

| Dependency / boundary | Closure class | Current resolution / why safe | Owner / future stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|
| Person vs Subject | RESOLVED | Person native identity may play Subject role | current Person/Subject | Subject requires separate Person wrapper identity | CORE-04, XCON-01 |
| Person vs Actor | RESOLVED | human identity != contextual agency | current Person/Actor | future role model cannot preserve passive Person/non-human Actor cases | CORE-03, MA-19, XCON-01 |
| Person vs Account | RESOLVED at conceptual level | human identity independent of access lifecycle | current boundary | auth model requires `Person.id = Account.id` to remain coherent | CORE-02, MA-01, XCON-01 |
| Actor vs Account | RESOLVED | semantic agency != authenticated access identity | current boundary | workflows cannot reconstruct actor without collapsing to Account | CORE-04, MA-10 |
| User term | RESOLVED | product/implementation language only | Language Map | UI term begins driving kernel identity | CORE-08, XCON-06 |
| Account vs Principal/credentials/providers | SAFE DEFERRED | security details do not block current identity boundary | Authority/security + logical model | authorization/authentication requirements materially alter Account semantics | CORE-13, MA-06, MA-17 |
| Actor vs Performer/Participant/Responsibility/Stewardship | SAFE DEFERRED | Actor deliberately does not replace typed roles | Relationships / Reasoning | specific roles cannot reference native actors naturally | CORE-04, MA-03, MA-15, XCON-04 |
| Actor vs Organization/System/AI native identities | SAFE DEFERRED | role semantics work without final native type set | later identity/Relationships | recurring workflow requires a native non-human identity with independent lifecycle not representable under current approach | CORE-06, MA-17, XCON-01 |
| Person reconciliation / merge / split | SAFE DEFERRED | identity invariant fixed; mechanics not needed yet | logical model + Provenance/Version/Decision | duplicate/import workflows cannot preserve identity/history | CORE-09, XCON-03 |
| deletion/anonymization/historical attribution | SAFE DEFERRED | current access and identity/history already separated | Visibility/Authority/retention + logical model | legal/privacy requirement conflicts with retained identity attribution | MA-07, MA-11, MA-13 |
| delegated/on-behalf-of action | SAFE DEFERRED | Actor/Account/Principal distinction leaves room | Relationships/Authority | AI/service/caregiver action requires semantics that collapse current boundary | MA-06, MA-10, MA-17, XCON-04 |

No current dependency is a structural blocker.

---

# 9. Representative scenarios

## Non-account caregiver subject

```text
Person Maria
Subject of Observation

Person Anna
Actor role: recorder

Account Anna-A1
authenticates LifeOS access
```

**PASS** — no synthetic Account for Maria.

## Person later creates Account

```text
2026 Person P17 exists
2028 Account A9 linked after onboarding
```

**PASS** — Person identity predates access identity.

## Account provider migration

```text
Person P17
Account A9
provider identity old -> new
```

**PASS** — neither Person nor historical Actor attribution changes merely because credentials change.

## Account deletion

```text
Person Anna recorded O17 in 2027
Account disabled 2030
```

**PASS** — historical actor may remain Person Anna where retention policy permits.

## Software/AI action

```text
AI Agent X
Actor role: proposer
service Principal Y
authorized under delegated policy
```

**PASS WITH HARDENING** — Principal/delegation/Authority remain future explicit semantics.

## Wrong duplicate Person merge

Two imported contacts are incorrectly treated as one human.

**PASS WITH HARDENING** — silent merge prohibited; reconciliation/history required.

---

# 10. Concept verdict

- [ ] PASS
- [x] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Accepted baseline

```text
PERSON
CANONICAL NATIVE ENTITY

ACTOR
CANONICAL SEMANTIC AGENCY ROLE / CAPABILITY
NOT AN ENTITY / ROOT

ACCOUNT
REAL PLATFORM / ACCESS IDENTITY BOUNDARY
DETAILED AUTH MODEL DEFERRED

USER
PRODUCT / IMPLEMENTATION TERM ONLY
NO DOMAIN PRIMITIVE

PRINCIPAL
SAFE DEFERRED
AUTHORITY / SECURITY MODEL
```

## Hardenings incorporated

1. Person identity is not Account/provider/contact identity.
2. Actor is agency semantics over native identity, not a wrapper entity.
3. Account/authentication context is distinct from semantic Actor attribution.
4. current Account access != historical Person/Actor attribution.
5. agency != Responsibility/Authority/ownership.
6. User is not a kernel root.
7. identity reconciliation/merge is explicit and history-preserving.
8. AI/service agency does not launder human authorship, authority or responsibility.
9. Person linkage and actor/delegation information remain privacy-sensitive.
10. Principal/delegation/security details are intentionally deferred rather than pre-modeled.

---

# 11. Mandatory future re-tests

1. Asset review — Person must not become a generic managed-object/party superclass.
2. Resource review — Person may also play Resource role without identity collapse.
3. Relationships / Reasoning — Participant, Performer, Responsibility, Stewardship and typed actor roles.
4. Authority / Visibility — Account, Principal, delegation, access and historical attribution.
5. Provenance/Version/Decision — identity reconciliation and correction lineage.
6. AI Proposal/authority — service/AI actor versus human approval and delegation.
7. logical data model — heterogeneous native actor references, Person↔Account linkage, merge/split/history.
8. Cross-Cluster Validation v4.

---

# 12. Documentation propagation

Before closing:

- [x] Person concept created;
- [x] Actor concept created;
- [x] Account boundary recorded without premature `account.md`;
- [x] Subject wording aligned;
- [x] Observation wording aligned;
- [x] Provenance wording aligned;
- [x] Language Map updated;
- [x] Domain README updated;
- [x] workstream handoff updated;
- [x] no universal `users.id`, User root or Actor entity pre-approved;
- [x] dependency owners/reopening triggers recorded.

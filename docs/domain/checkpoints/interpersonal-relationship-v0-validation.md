# Interpersonal Relationship v0 — Validation Record

**Date:** 2026-08-16  
**Method:** Domain Validation Methodology v3, including product-need closure hardening  
**Branch pre-scope:** `feature/domain-model` @ `c6c7fb40be95669d77e8dbe159ccb85ccb71788e`  
**Status:** semantic PASS WITH HARDENING; propagation/post-write closure pending

---

# 1. Product-need gate

## Current LifeOS evidence

Current product evidence requires persistent person-related context before full account-to-account collaboration:

- `docs/product/v1-adaptive-intelligence-and-future-social.md` requires person-related commitments without account-to-account collaboration and distinguishes purely private items from commitments involving another person;
- `docs/product/v1-global-search-and-command.md` requires people/clients/commitments as searchable context and person-scoped questions such as outstanding commitments to a named Person;
- `docs/domain/concepts/person.md` already treats family member, friend, doctor, teacher, client, child, older adult and other external Persons as ordinary native reality without Account creation and deliberately leaves specific relationship semantics to Relationships / Reasoning.

Representative product questions:

```text
remind me to call my mother
which commitments to Marco are still open?
buy this for my partner
show items involving my colleague Luca
```

## Need disposition

```text
CURRENT LIFEOS NEED
REQUIRED BY CURRENT LIFEOS
```

Free text alone is insufficient because the relation must survive across search, commitments, reminders, history, natural-language resolution and future collaboration without fabricating Account identity.

---

# 2. Candidate formation

```text
H0  No canonical interpersonal relation; free text/tags only.
H1  Use Collective/Membership.
H2  Use generic Personal Knowledge / related_to graph edge.
H3  Specific contextual Person↔Person Interpersonal Relationship + bounded/extensible kind vocabulary.
H4  Universal social-graph / Relationship root.
H5  Primitive/entity per label: Mother, Friend, Partner, Colleague, etc.
```

## Candidate results

### H0 — free text only

**FAIL.** Cannot reliably preserve durable person-scoped semantic context across product queries, history and reference resolution.

### H1 — Collective/Membership

**FAIL.** `Maria is my mother` does not mean Maria is a member of an irreducible Collective; Membership answers belonging to a Collective, not interpersonal relation.

### H2 — generic Personal Knowledge / related_to edge

**FAIL.** Semantic-free links lose the exact relationship meaning and violate the accepted Relationship specificity rule.

### H3 — specific relation family

**PASS WITH HARDENING.** Preserves current product need with the smallest semantic addition and no new native referent.

### H4 — universal social graph

**FAIL / OVERMODELED.** Reopens the explicitly rejected universal Relationship root and encourages inappropriate transitivity/rights/identity inference.

### H5 — primitive per label

**FAIL / OVERMODELED.** Vocabulary distinctions do not imply separate native identities or relation-family primitives.

Winner:

```text
H3
```

---

# 3. Canonical definition

> **Interpersonal Relationship is the bounded contextual Person-to-Person relation through which LifeOS retains materially useful interpersonal context between two persistent Persons, independently from Participation, Collective Membership, Responsibility, Coordination Stewardship, Authority, Visibility, Agreement, Consent, Representation, Contribution or any particular Activity/Event.**

Classification:

```text
Interpersonal Relationship
SPECIFIC CONTEXTUAL PERSON↔PERSON RELATION FAMILY

relationship kind
BOUNDED / EXTENSIBLE VOCABULARY

new native referent
NO
```

---

# 4. CORE Semantic Validation

## CORE-01 — workflow inversion

**PASS.** The relation does not require fabricating Activities, Events, Collectives or Account records merely to preserve interpersonal context.

## CORE-02 — deep chronology

**PASS WITH HARDENING.** Relationship establishment, change, ending, correction, Account lifecycle and later contextual roles remain separately reconstructible.

Chronology:

```text
T0 Maria exists as Person without Account
T1 Mattia establishes Maria = mother
T2 natural-language command resolves "my mother" to Maria
T3 Maria later becomes member of a Family Collective
T4 Maria creates Account
T5 provider import suggests relationship metadata
T6 AI proposes a relation for Luca
T7 partner relation with Anna ends
T8 Anna later participates in an Event
T9 historical query reconstructs prior state where materially retained
```

Required invariants:

```text
current relationship != historical relationship
correction != silent overwrite
Account lifecycle != relationship lifecycle
Participation/Membership lifecycle != relationship lifecycle
```

## CORE-03 — adversarial reductio

**PASS WITH HARDENING.** Tested collapses fail:

```text
relationship = Membership             FAIL
relationship = Participation          FAIL
relationship = Responsibility         FAIL
relationship = Authority              FAIL
relationship = Visibility             FAIL
relationship = Consent                FAIL
relationship = generic related_to     FAIL
relationship label = rights/duties    FAIL
```

## CORE-04 — redundancy / merge-split

**PASS WITH HARDENING.** No accepted relation fully answers persistent interpersonal context. Conversely, Interpersonal Relationship must not absorb specific operational/governance relation families.

## CORE-05 — traceability

**PASS.** The relation can remain attributable to user assertion, provider/import Evidence, AI proposal, correction and historical provenance without claiming universal truth.

## CORE-06 — independence

**PASS.** Endpoints remain native Persons independent of Accounts, Actor roles, Events, Collectives and relation state.

## CORE-07 — external/product benchmark pressure

**PASS.** Product/research materials repeatedly surface family/friend/partner/colleague/client/caregiver context, while no external taxonomy is treated as ontology authority. The accepted abstraction is narrower than CRM/social-network models.

## CORE-08 — anti-pattern resistance

**PASS WITH HARDENING.** Reject:

- universal social graph;
- one primitive per relationship label;
- implicit Authority/Visibility/Consent from interpersonal label;
- semantic-free `related_to` kernel truth;
- forced reciprocity/transitivity.

## CORE-09 — correction / epistemic safety

**PASS WITH HARDENING.** Imported or inferred relationship metadata remains Evidence/Provenance/proposal until established. Conflict may remain unresolved. No universal provider/newest/creator/AI-confidence winner.

## CORE-10 — scale / history

**PASS WITH HARDENING.** Search/index/traversal pressure does not manufacture a universal Relationship entity. Consequential history is retained only where product/privacy policy requires it.

## CORE-11 — simple / power-user fit

**PASS.** Ordinary UI can remain `Maria · Mother`; more history/context is progressive and consequence-sensitive.

## CORE-12 — product value / complexity

**PASS WITH HARDENING.** The relation directly supports V1 person-related commitments and search while avoiding CRM/social-network bureaucracy.

## CORE-13 — implementation pressure

**PASS WITH HARDENING.** No SQL, junction-table, API, index, contact-sync or authorization shape is selected by semantic acceptance.

```text
CORE GATE
PASS WITH HARDENING
```

---

# 5. Mandatory hardenings incorporated

The accepted concept incorporates all of:

```text
IPR-01..IPR-30
```

as recorded in `../concepts/interpersonal-relationship.md`.

High-risk boundaries include:

```text
Interpersonal Relationship != universal Relationship/social graph
Interpersonal Relationship != Collective/Membership
Interpersonal Relationship != Participation
Interpersonal Relationship != Responsibility/Stewardship
Interpersonal Relationship != Authority/Visibility
Interpersonal Relationship != Agreement/Consent
Interpersonal Relationship != Representation
Interpersonal Relationship != Contribution
relationship kind != rights/duties
provider/AI inference != established human relationship truth
```

---

# 6. Multi-Actor Compatibility Gate

| Test | Result | Finding |
|---|---|---|
| MA-01 Identity/account independence | PASS | neither Person requires Account |
| MA-02 Shared fact / actor overlay | PASS WITH HARDENING | one actor's asserted/perspective relation need not equal another actor's stance |
| MA-03 Responsibility | PASS WITH HARDENING | relationship grants no accountability |
| MA-04 Coordination Stewardship | PASS | relationship grants no ongoing coordination burden |
| MA-05 Common ground | PASS WITH HARDENING | actor-scoped relation assertion need not be mutually acknowledged/agreed |
| MA-06 Authority | PASS WITH HARDENING | labels such as manager/parent do not automatically establish bounded LifeOS Authority |
| MA-07 Selective disclosure | PASS WITH HARDENING | Person, relation kind, history and supporting Evidence may have distinct Visibility |
| MA-08 Inference privacy | PASS WITH HARDENING | derived answers must not leak hidden relationship basis |
| MA-09 Partial adoption | PASS | accountless Persons ordinary |
| MA-10 Representation | PASS | actual Actor/represented party remains separate from interpersonal relation |
| MA-11 Lifecycle/revocation | PASS WITH HARDENING | ending/changing relation affects future state without rewriting history |
| MA-12 Conflict/adversarial | PASS WITH HARDENING | competing assertions may coexist unresolved |
| MA-13 Unequal power | PASS WITH HARDENING | interpersonal label does not create Consent/Authority/Visibility |
| MA-14 Resource/capacity | PASS | Person may separately play Resource role |
| MA-15 Burden distribution | PASS | relation alone creates no reminder/stewardship burden |
| MA-16 Progressive formality | PASS | simple labels to qualified history only where useful |
| MA-17 AI/automation | PASS WITH HARDENING | AI may propose/resolve references but not fabricate human relationship truth |
| MA-18 Specialist systems | PASS | legal/clinical/HR taxonomies remain bounded adapters |
| MA-19 Primitive redundancy | PASS WITH HARDENING | no social-graph root or per-label primitive |
| MA-20 Actor-scoped attribution | PASS WITH HARDENING | shared Person identity does not force identical interpersonal assertions across actors |

```text
MULTI-ACTOR GATE
PASS WITH HARDENING
```

---

# 7. Cross-Concept Consistency Gate

```text
XCON-01 Identity                         PASS WITH HARDENING
XCON-02 Authority                        PASS WITH HARDENING
XCON-03 current/history/material state   PASS WITH HARDENING
XCON-04 Relationships / Reasoning        PASS WITH HARDENING
XCON-05 Multi-Actor                      PASS WITH HARDENING
XCON-06 Language                         PASS WITH UPDATE

XCON GATE
PASS WITH HARDENING
```

No accepted concept requires reopening.

---

# 8. Adjacent Dependency Sweep with hardened need disposition

## REQUIRED NOW — resolved by this review

```text
persistent Person↔Person interpersonal context
→ RESOLVED by Interpersonal Relationship v0
```

## ALREADY COVERED / COMPOSABLE

```text
Collective/family/team identity
→ Collective + Membership where irreducible plurality actually exists

participation in a commitment/event
→ Participation

who must ensure something is handled
→ Responsibility

ongoing coordination burden
→ Coordination Stewardship

who may govern/change
→ Authority

who may see
→ Visibility

mutual assent / bounded permission
→ Agreement / Consent

on-behalf-of action
→ Representation

actual material contribution
→ Contribution
```

## REJECTED / OVERMODELED

```text
universal social graph
universal Relationship root
semantic-free PersonalKnowledgeLink root
one primitive/entity per relationship label
universal reciprocity/transitivity rules
```

## NOT REQUIRED BY CURRENT LIFEOS KERNEL

```text
legal kinship/civil-status engine
legal guardianship/capacity taxonomy
HR organization-chart semantics as universal kernel
formal social-network follow/friend-request lifecycle
relationship strength/intimacy score
relationship quality/health score
```

These are closed out of the current kernel. They may be reconsidered only from new concrete product evidence, not because they are semantically possible.

## STAGE-DEFERRED — non-semantic only

```text
SQL / persistence shape
API resources
indexes/traversal optimization
contact/provider sync and reconciliation mechanics
technical authorization enforcement
retention/anonymisation implementation
exact storage of extensible relationship-kind vocabulary
```

These later-stage questions do not reopen semantic acceptance unless implementation proves that no representation can preserve the accepted invariants.

```text
SEMANTIC SAFE DEFERRED 0
REOPEN                 0
UNCLASSIFIED           0
```

---

# 9. Adversarial regression corpus

```text
R-IPR-01 mother relation + no Account
R-IPR-02 mother relation + later Family Collective Membership
R-IPR-03 colleague label does not create Responsibility or Authority
R-IPR-04 manager label does not grant arbitrary governance
R-IPR-05 partner relation ends; historical state preserved
R-IPR-06 friend relation asserted by A does not force reciprocal assertion by B
R-IPR-07 friend(A,B)+friend(B,C) does not infer friend(A,C)
R-IPR-08 provider metadata suggests relation but remains Evidence until established
R-IPR-09 AI infers close-friend relation but cannot silently establish it
R-IPR-10 private relation kind supports bounded command resolution without leaking hidden basis
R-IPR-11 several related Persons do not automatically form Collective
R-IPR-12 Participation in later Event does not recreate ended interpersonal relationship
```

---

# 10. Final semantic verdict

```text
INTERPERSONAL RELATIONSHIP v0

PASS WITH HARDENING

CURRENT LIFEOS NEED        YES
NEW NATIVE REFERENT        NO
NEW SPECIFIC RELATION      YES
CORE                       PASS WITH HARDENING
MA                         PASS WITH HARDENING
XCON                       PASS WITH HARDENING
ADS                        COMPLETE
SEMANTIC SAFE DEFERRED      0
REOPEN                      0
UNCLASSIFIED                0
```

This file does **not** claim repository `CLOSED`. The approved propagation must first pass remote compare/payload/history/main-isolation QA. Only then may `interpersonal-relationship-v0-validation-part-2.md` record durable closure.
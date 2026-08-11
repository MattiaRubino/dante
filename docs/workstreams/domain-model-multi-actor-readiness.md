# Workstream Addendum — Multi-Actor Readiness

**Status:** EVIDENCE-BACKED CROSS-CUTTING BASELINE COMPLETE  
**Established:** 2026-08-11  
**Evidence synthesis completed:** 2026-08-11  
**Active branch:** `feature/domain-model`  
**Parent workstream:** `domain-model.md`

## Purpose

This addendum records the current handoff state after the initial multi-actor hardening was tested against the completed collaboration discovery simulation and consolidated external Deep Research.

The product remains personal-first. The domain kernel is now explicitly multi-actor-ready.

This does **not** mean the full collaboration feature set, authorization architecture, organizations, chat or enterprise workflow have been designed.

---

# Required reading

Read in this order for multi-actor-sensitive domain work:

1. [`../domain/README.md`](../domain/README.md)
2. [`../domain/language-map.md`](../domain/language-map.md)
3. [`../domain/multi-actor-readiness-v1.md`](../domain/multi-actor-readiness-v1.md)
4. [`../domain/checkpoints/multi-actor-evidence-synthesis-v0.md`](../domain/checkpoints/multi-actor-evidence-synthesis-v0.md)
5. [`../domain/validation-methodology-v2.md`](../domain/validation-methodology-v2.md)
6. [`../domain/validation-methodology-v2-multi-actor-addendum.md`](../domain/validation-methodology-v2-multi-actor-addendum.md)
7. [`../product/multi-actor-collaboration-discovery-simulation-2026-08.md`](../product/multi-actor-collaboration-discovery-simulation-2026-08.md)
8. [`../product/multi-actor-collaboration-research-2026-08.md`](../product/multi-actor-collaboration-research-2026-08.md)

Historical/pre-research baseline:

- [`../domain/multi-actor-readiness-v0.md`](../domain/multi-actor-readiness-v0.md)
- [`../domain/checkpoints/multi-actor-readiness-v0.md`](../domain/checkpoints/multi-actor-readiness-v0.md)

These are preserved for history; v1 + evidence synthesis are current.

---

# Current validation state

```text
Intention & Execution v0
PASS

Time v0
PASS

Cross-Cluster Validation v2
PASS

Multi-Actor Evidence Synthesis v0
PASS WITH EVIDENCE-BACKED HARDENING
```

Results:

- structural reopenings: **0**;
- removed concepts: **0**;
- merged concepts: **0**;
- mandatory new primitives introduced: **0**;
- actor-neutral wording hardened: **Goal / Activity / Routine**;
- terminology governance established: **Domain & Product Language Map**.

---

# Current canonical multi-actor rules

```text
Goal identity       != governor / stakeholder / subject
Plan identity       != coordinator / contributor / responsible actor
Activity identity   != requester / assignee / performer
Event identity      != organizer / participant / response
Routine identity    != performer
Milestone identity  != stakeholder / approver / governor
Occurrence identity != assigned actor
Schedule identity   != participant acceptance / capacity owner
Session identity    != performer count
Constraint identity != authority actor
Recurrence identity != assignment rotation
Capacity identity   != one mandatory user/account
```

And:

```text
shared canonical fact
+
actor-scoped personal overlay
```

is preferred over per-user semantic copies when actors genuinely coordinate around one real object.

---

# New evidence-backed hardenings

The completed research adds the following permanent validation requirements.

## Responsibility

`assigned_to` is insufficient as the universal model.

Future review must account for, where justified:

- accountability/responsibility;
- expected performer;
- actual performer;
- open/claimable work;
- substitution;
- approval;
- hand-off.

No Responsibility primitive/table has been pre-approved.

## Coordination stewardship

Assignment does not prove that anticipation, reminding, monitoring or repair burden transferred.

This is a mandatory product/domain validation question but not yet an accepted primitive.

## Common ground

Where consequence matters, preserve the possible distinction:

```text
sent
!= seen
!= acknowledged
!= accepted/agreed
!= authoritative
!= acted upon
!= Actual
```

Do not expose this complexity universally in casual UX.

## Privacy

Useful derived consequences may be shared without exposing private source facts.

Privacy review also includes inference/explanation/tool-call leakage, not only raw-field visibility.

## Authority

Creator, owner label, participant and viewer are not automatic authority synonyms.

AI authority remains bounded by the principal/context/policy under which it acts.

## Participation lifecycle

External/partial/assisted participants are normal. Future access/revocation must remain independent from historical attribution.

## Coordination burden

Every collaboration feature must be evaluated per actor: who performs setup, state maintenance, acknowledgements, monitoring and repair versus who receives the benefit.

---

# Terminology baseline

The current terminology architecture is now explicit.

Reference:

- [`../domain/language-map.md`](../domain/language-map.md)

The map separates:

```text
Domain
Product
UI
Implementation
```

and prevents familiar UX nouns from automatically becoming kernel primitives.

Important mappings:

```text
Task           -> Activity UI/profile
Project        -> Plan product profile (current direction)
Program        -> Plan product profile (current direction)
Calendar Block -> product/UI representation over temporal/capacity semantics
Deadline       -> latest-bound Temporal Constraint semantics
Occurrence     -> canonical domain concept, usually hidden in UI
```

Future Actor/Subject/Resource/Responsibility/Authority terms remain PROVISIONAL/DEFERRED until dedicated reviews.

---

# Current branch coherence

The domain branch was merged non-destructively with the updated `main` after PR #6 integrated the multi-actor evidence documents.

Merge commit:

```text
08595f9526e08db53d9b446b8a7a76cd46adcd55
```

The branch therefore contains both:

- the complete Domain Atlas work;
- the canonical multi-actor discovery/research evidence from `main`.

Do not re-import or duplicate those evidence documents on another domain branch.

---

# How to work from now on

Every new concept review must:

1. follow Validation Methodology v2;
2. apply the Multi-Actor Addendum where applicable;
3. use the Language Map terminology/status rules;
4. preserve progressive disclosure;
5. introduce new primitives only after distinct identity/lifecycle/authority/query semantics are demonstrated.

At minimum ask:

```text
What is shared?
What remains actor-private?
Can roles change without replacing the object?
Who is subject / responsible / performer / authority?
Can non-LifeOS actors participate?
Can private data be used without disclosure?
Does the feature reduce total coordination burden?
```

---

# Downstream areas materially affected

Later reviews must explicitly use the multi-actor evidence for:

```text
Actual / Outcome
Confirmation / Observation / Evidence / Provenance
Subject / Person / Actor
Resource / Asset
Relationship / Dependency
Responsibility / Assignment / Hand-off
Authority / Visibility
Decision / Version
AI Proposal / Context Builder
```

This is a review agenda, not a pre-selected set of tables.

---

# What remains deliberately unbuilt

Do not introduce merely because the research mentions them:

- organization/team/household hierarchy;
- universal Group object;
- ACL/RBAC/ABAC/ReBAC infrastructure;
- Zanzibar/OpenFGA dependency;
- collaboration chat;
- generic approval engine;
- universal responsibility workflow;
- AI multi-agent orchestration;
- specialist clinical/legal/workforce administration.

Those require later evidence and implementation need.

---

# Current next step

The multi-actor synthesis/terminology hardening is complete as a cross-cutting baseline.

The project state remains:

```text
first two clusters validated
multi-actor readiness evidence-backed
canonical language map established
next cluster not automatically started
```

Continue user-led architecture/product brainstorming or explicitly select the next Domain Atlas cluster when ready.
# Validation Methodology v2 — Multi-Actor Addendum

**Status:** Mandatory evidence-backed extension to the current validation standard  
**Established:** 2026-08-11  
**Evidence-backed revision:** 2026-08-11  
**Applies to:** all Domain Atlas concept reviews, cluster checkpoints, final domain validation, and collaborative product proposals

## Purpose

This addendum ensures that LifeOS does not accidentally encode structural single-user assumptions while the product remains personal-first.

The initial addendum was established before the dedicated multi-actor discovery simulation was complete. It is now strengthened by:

- `../multi-actor-readiness-v1.md`;
- `checkpoints/multi-actor-evidence-synthesis-v0.md`;
- `../product/multi-actor-collaboration-discovery-simulation-2026-08.md`;
- `../product/multi-actor-collaboration-research-2026-08.md`.

This addendum **supplements** Validation Methodology v2. It does not replace workflow inversion, chronological simulation, reductio, redundancy analysis, traceability, scale/history stress or simple-user/power-user validation.

---

# 1. Governing principle

For every concept, ask whether its identity or lifecycle has been accidentally defined as though one registered user must simultaneously be:

```text
owner
participant
responsible actor
performer
subject
authority
viewer
source
capacity owner
```

Canonical validation rule:

> **Coincidence of these roles in the personal-first case must not become a universal domain invariant.**

---

# 2. Multi-Actor Compatibility Test

Every new concept must answer the applicable questions.

## Identity

- Can the concept exist for one actor or many?
- Does changing participant/assignee/performer change object identity?
- Is identity accidentally derived from `user_id`?
- Can an external/non-LifeOS person be represented where needed?

## Shared vs personal state

- Which facts are genuinely shared/canonical?
- Which facts belong to an actor's personal overlay?
- Would the current model duplicate the same real object per user?
- Can personal notes/reminders/Goals remain private around a shared fact?

## Actor dimensions

- Who is the subject?
- Who participates?
- Who is responsible?
- Who actually performs?
- Who coordinates/stewards the work?
- Who has authority?
- Who can see what?
- Who supplied the fact?

Do not require every concept to model every dimension. Require only that the kernel not collapse dimensions that can differ materially.

---

# 3. Shared Fact / Personal Overlay Test

For a candidate collaborative object, explicitly attempt:

```text
one shared canonical object
+
actor-scoped context
```

Then compare against:

```text
one semantic duplicate per user
```

Prefer the first when multiple actors genuinely refer to the same real-world fact.

Failure signals:

- schedule changes must be copied manually between user-owned clones;
- one participant declining deletes/changes the event for everyone;
- every actor must expose personal notes to preserve shared identity;
- provider/import records are confused with canonical shared identity.

---

# 4. Responsibility / Assignment Test

Do not validate an Activity/Occurrence model solely with `assigned_to`.

Where relevant stress:

```text
requester
accountable/responsible actor
expected performer
actual performer
open/claimable work
substitute
approver
hand-off recipient
fallback responsibility
```

Required questions:

- Can responsibility change without replacing the Activity?
- Can work be validly unassigned/open?
- Can a hand-off be requested but not accepted?
- Can planned performer differ from Actual performer?

Do not create a universal workflow engine merely to pass this test.

---

# 5. Coordination Stewardship / Mental-Load Test

External evidence shows that visible execution can be assigned while anticipation, reminding, monitoring and repair remain with another person.

For household, caregiving, team-management and other coordination-heavy scenarios ask:

- Who notices that work is needed?
- Who remembers timing/preferences?
- Who prompts another actor?
- Who monitors completion?
- Who repairs the plan if work fails?

This may reveal a future domain relation or only a product burden problem.

Canonical rule:

> **Do not treat task assignment as proof that coordination burden transferred.**

---

# 6. Common-Ground / State-Separation Test

For high-consequence coordination test the following distinctions:

```text
proposed / sent
!= delivered
!= seen
!= understood
!= acknowledged
!= accepted/agreed
!= authoritative/confirmed
!= acted upon
!= Actual
```

The test asks whether these states **can** be distinguished when needed, not whether every UI must expose them.

Use consequence-sensitive product design:

- casual plans may collapse stages;
- shift swaps, care hand-offs and approvals may require more explicit grounding.

Failure signal:

> a message being sent automatically changes canonical responsibility or proves execution.

---

# 7. Authority Test

Ask:

- Who may propose a change?
- Who may accept it personally?
- Who may make it canonical for the shared object?
- Who may override a rule?
- Is authority external/institutional?
- Does the creator actually possess the authority the model grants them?

Canonical guardrail:

> **Creation, participation, visibility and ownership labels do not automatically establish social/legal/institutional authority.**

---

# 8. Selective-Disclosure Test

For every multi-actor query ask:

> Does the other actor need the source fact, or only a consequence/projection?

Examples:

```text
need: coordinate time
share: unavailable 18:00-20:00
not automatically: medical appointment
```

```text
need: verify resource usable
share: unavailable
not automatically: private trip purpose
```

Failure signal:

> useful coordination is possible only by granting raw access to another person's personal context.

---

# 9. Inference-Privacy Test

Privacy validation must cover more than direct field access.

Inspect possible leakage through:

- recommendation;
- explanation;
- availability pattern;
- derived state;
- notification wording;
- AI answer;
- AI tool/API argument;
- ranking or status.

Required questions:

- Can the system compute a safe result from private inputs?
- Can it explain the result without exposing the private cause?
- Does the tool schema force raw private context into free-text parameters?

Canonical guardrail:

> **AI knowledge and computation do not create disclosure permission.**

---

# 10. Partial-Adoption / External-Participant Test

Re-run important collaborative flows under at least three states:

```text
all participants use LifeOS
some participants use LifeOS
only one participant uses LifeOS
```

Where relevant also test:

- bounded web/link response;
- external provider interaction;
- assisted participation;
- non-interacting represented subject.

Failure signal:

> an ordinary real-world coordination flow becomes impossible unless every person creates and actively maintains a LifeOS account.

---

# 11. Assisted-Participation / Provenance Test

When one person helps another act, ask:

- who is the subject?
- who physically entered/performed the action?
- who confirmed/approved it?
- whose assertion is represented?

Failure signal:

> the helper is silently recorded as though the subject personally asserted/performed the fact.

---

# 12. Relationship-Lifecycle Test

Chronological simulation must include where applicable:

```text
join
role change
temporary substitution
access narrowing
responsibility transfer
leave
future access revocation
historical attribution retained
```

For sensitive relationships additionally test immediate/emergency revocation.

Canonical guardrail:

> **Current access and historical participation are different questions.**

---

# 13. High-Conflict / Adversarial Test

Do not validate collaboration only with cooperative actors.

Where materially relevant test:

- disagreement;
- refusal;
- silence;
- conflicting reports;
- strategic behavior;
- relationship exit;
- ongoing coordination despite low trust;
- attempts to use visibility/audit as surveillance or pressure.

Ask whether LifeOS can preserve bounded coordination without pretending that the relationship is friendly or consensual in every dimension.

---

# 14. Guardian / Caregiver / Unequal-Power Test

Do not generalize peer collaboration to relationships with legitimate asymmetric authority.

Stress:

- guardian vs minor;
- caregiver vs cared-for person;
- manager vs worker;
- clinician vs patient;
- teacher vs student.

Required checks:

- legitimate authority remains context-bounded;
- visibility does not automatically expand with authority;
- personal autonomy can differ by domain/context;
- consent assumptions remain realistic under power imbalance.

Jurisdiction-specific legal rules remain separate legal/product work.

---

# 15. Resource-and-Capacity Test

For collaborative scheduling include people **and** non-person resources where applicable:

- rooms;
- vehicles;
- equipment;
- devices;
- facilities;
- stock/capacity pools.

Verify that:

```text
shared Schedule
```

can produce several independent capacity claims without duplicating the scheduled object.

---

# 16. Coordination-Burden Distribution Test

For every proposed collaboration feature ask:

```text
Who does setup?
Who maintains state?
Who gets notifications?
Who must acknowledge?
Who monitors failure?
Who repairs exceptions?
Who receives the primary benefit?
```

Rate the feature on:

1. total coordination work;
2. distribution of that work;
3. cognitive burden;
4. privacy cost;
5. accessibility cost;
6. maintenance cost.

Failure signal:

> organizer efficiency is achieved by imposing recurring maintenance on everyone else.

---

# 17. Formality / Progressive-Disclosure Test

Run the same semantic capability across consequence levels.

Example:

### Low consequence

```text
Dinner Saturday?
Yes / Maybe / No
```

### Medium consequence

```text
Project review request
recipient acknowledges / completes review
```

### High consequence

```text
shift/care hand-off
request
acceptance
required authority approval
effective canonical transfer
```

The domain should preserve enough semantics for the high-consequence case while the UI avoids imposing that machinery on the low-consequence case.

---

# 18. AI Authority Test

For any AI-mediated multi-actor operation ask:

- On whose behalf is the AI acting?
- What authority does that principal actually have?
- Which private contexts can the AI use internally?
- Which outputs may be disclosed to each recipient?
- Is the AI proposing, deciding, confirming or merely explaining?

Canonical rule:

> **AI effective authority <= acting principal/context/policy authority.**

Failure signal:

> AI optimization is presented as agreement, authoritative fact or permission it does not possess.

---

# 19. Specialist-Boundary Test

For healthcare, education, workforce, legal, accounting or other specialist contexts ask:

- Is LifeOS coordinating around authoritative external facts?
- Is the external specialist system still the proper authority?
- Are we accidentally rebuilding specialist administration?

The stress case may justify integration semantics without justifying product-scope expansion.

---

# 20. Multi-actor redundancy / primitive test

Before introducing any multi-actor primitive perform the standard REMOVE / MERGE / SPLIT tests plus:

```text
Can this be a typed Relationship?
Can this be actor-scoped state on an existing object?
Can this be derived?
Is it only UI vocabulary?
Does it have independent identity/lifecycle/authority/query behavior?
```

A research finding is not enough by itself to justify a table/entity.

---

# 21. Required cluster checkpoint section

Every future cluster checkpoint must include a short `Multi-Actor Compatibility` section answering:

- scenarios tested;
- shared vs actor-scoped truth;
- authority/responsibility issues;
- privacy/inference issues;
- partial-adoption issues;
- coordination-burden issues;
- any structural reopening required.

A checkpoint may state `not materially applicable` for a dimension, but should not silently omit multi-actor consideration.

---

# 22. Final-domain multi-actor gate

Before physical persistence/API implementation is treated as broadly stable, rerun at minimum:

1. friends planning an outing;
2. household shared work with open responsibility;
3. team meeting + assigned follow-up;
4. shift swap requiring authority;
5. caregiver hand-off with conflicting evidence;
6. parent/guardian/child coordination;
7. shared resource booking;
8. external non-LifeOS participant;
9. privacy-preserving common-time calculation;
10. relationship revocation;
11. high-conflict ongoing coordination;
12. assisted/low-digital participant;
13. collaborative Session/Actual attribution;
14. AI recommendation using private multi-party context.

The domain fails the gate if ordinary representation requires per-user duplicates, fabricated consensus, source disclosure, mandatory universal adoption or loss of historical truth.

---

# 23. Current status

The first two clusters have passed this evidence-backed compatibility review.

Reference:

- `checkpoints/multi-actor-evidence-synthesis-v0.md`

Current result:

```text
Intention & Execution v0 — PASS
Time v0                 — PASS
Multi-Actor Readiness   — PASS WITH HARDENING
```

No full collaboration implementation is implied by this PASS.
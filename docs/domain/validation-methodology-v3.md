# Domain Validation Methodology v3

**Status:** Current mandatory validation standard  
**Established:** 2026-08-11  
**Current revision:** 2026-08-12 — dependency-closure discipline added  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`  
**Supersedes for active work:** `validation-methodology-v2.md` plus `validation-methodology-v2-multi-actor-addendum.md`

## Purpose

Validation Methodology v3 turns the previous semantic validation suite and the later evidence-backed Multi-Actor Addendum into one ordered, auditable validation pipeline.

The objective is not to maximize the number of tests. It is to minimize the chance that LifeOS accepts a concept which works in a clean personal scenario but fails under real chronology, contradictory reality, shared state, partial adoption, privacy, authority, historical correction, scale, or product-complexity pressure.

The governing rule is:

> **A concept is not validated because the team discussed many edge cases. It is validated only when the required test registry has been executed, recorded, and resolved at the appropriate level.**

This methodology remains cumulative. It preserves the strongest parts of the original Domain Atlas review, Validation Methodology v2, and Multi-Actor Readiness v1 while making execution order and PASS criteria explicit.

---

# 1. Validation architecture

Every Domain Atlas concept passes through four ordered semantic stages plus a dependency-closure step:

```text
A. EVIDENCE + CANDIDATE FORMATION
              ↓
B. CORE SEMANTIC VALIDATION GATE
              ↓
C. MULTI-ACTOR COMPATIBILITY GATE
              ↓
D. CROSS-CONCEPT CONSISTENCY GATE
              ↓
E. ADJACENT DEPENDENCY SWEEP
              ↓
        CONCEPT VERDICT
```

Every completed cluster then passes:

```text
CLUSTER INTEGRATION GATE
        ↓
CLUSTER MULTI-ACTOR STRESS GATE
        ↓
CLUSTER VERDICT
```

For the already-started Data / Subjects cluster, the project will finish the cluster using the current concept-by-concept sequence, then run a dedicated **Deferred Dependency Closure** across clusters 1–4 before Cross-Cluster Validation v4. From the following cluster onward, the Adjacent Dependency Sweep is mandatory before each concept is accepted, so unresolved adjacency does not accumulate silently.

Before broad logical/physical persistence is treated as stable, the whole accepted model passes:

```text
WHOLE-DOMAIN SEMANTIC REGRESSION
        ↓
WHOLE-DOMAIN MULTI-ACTOR REGRESSION
        ↓
PERSISTENCE / API PRESSURE TEST
        ↓
IMPLEMENTATION-READINESS VERDICT
```

Multi-actor readiness is therefore both:

1. a **design guardrail** while the candidate model is being formed; and
2. a **dedicated adversarial gate after the ordinary semantic suite**.

The second function is mandatory even when the candidate was designed with multi-actor concerns in mind.

---

# 2. Governing principles

## V3-GP-01 — LifeOS semantics first

External products, schemas, standards and APIs are evidence, not design authorities.

## V3-GP-02 — Real life does not have to fit LifeOS

Do not simplify a realistic workflow merely to make the candidate model pass.

Preserve ambiguity, failure, incomplete information, contradictory sources, spontaneous behavior, late correction, reassignment, privacy boundaries, disagreement and external authority.

## V3-GP-03 — Representation alone is insufficient

For each scenario evaluate:

1. coverage;
2. naturalness;
3. information preservation;
4. improvement over the real workflow;
5. semantic cost;
6. product/coordination cost.

## V3-GP-04 — Kernel precision must not force UI complexity

A sophisticated kernel must remain compatible with simple, contextual UI language and progressive disclosure.

## V3-GP-05 — Historical truth is not silently rewritten

Later correction, newly discovered relevance, synchronization or a changed policy must not fabricate earlier intention or erase material historical state.

## V3-GP-06 — Shared reality does not imply universal visibility

One canonical fact may coexist with actor-scoped participation, responsibility, private overlays, selective disclosure and different authority.

## V3-GP-07 — Research findings do not automatically become primitives

A new entity/value object/relationship is justified only by materially distinct identity, lifecycle, authority, invariants, query behavior or historical requirements.

## V3-GP-08 — No silent test omission

An applicable registered test must receive an explicit result. `N/A` is allowed only with a written reason.

## V3-GP-09 — No unclassified dependency limbo

A neighboring semantic question discovered during validation must not survive merely as "review later". Before the applicable closure point it must be classified as `RESOLVED`, `SAFE DEFERRED`, or `REOPEN`, with an explicit owner/trigger for any deferral.

---

# 3. Evidence and candidate formation

Before formal gating, the candidate concept must be grounded in sufficient evidence.

### EV-01 — Existing LifeOS evidence

Inspect applicable:

- current Domain Atlas concepts and checkpoints;
- product definitions;
- feature-discovery simulations;
- multi-actor discovery simulation/research;
- architecture/ADR constraints;
- relevant prototype/product assumptions.

### EV-02 — Real-world workflow evidence

Describe at least representative workflows **without LifeOS** before mapping them into LifeOS.

### EV-03 — Targeted external benchmark

Use mature external systems, standards, research or specialist software when they expose hard semantics not obvious from LifeOS alone.

Classify each meaningful pattern as:

- BORROW;
- ADAPT;
- ALREADY STRONGER;
- ANTI-PATTERN;
- NOT APPLICABLE.

### EV-04 — Candidate minimality

Propose the smallest semantic model that explains the evidence.

Do not add concepts merely to make the ontology look complete.

---

# 4. Core Semantic Validation Gate

The following tests execute before the dedicated multi-actor gate.

## CORE-01 — Real-World Workflow Inversion

Start from reality rather than LifeOS screens.

For each representative scenario:

```text
real-world problem
→ current tools/memory/messages/specialist systems
→ actual actions and decisions
→ information created/lost
→ friction/failure
→ LifeOS mapping
→ improvement / cost
```

Failure signals include fake LifeOS-only steps, duplicate objects, historical rewriting or greater user burden without material benefit.

## CORE-02 — Deep Chronological Simulation

Run the concept through time, not one snapshot.

Inject where applicable:

- creation;
- revision;
- rescheduling;
- postponement without replacement date;
- cancellation;
- partial execution;
- non-execution;
- spontaneous reality;
- imported data;
- contradictory provider data;
- correction;
- policy revision;
- exception;
- temporary disruption;
- timezone/context change;
- retroactive relevance;
- historical query months later.

Mandatory historical questions include:

- What was expected then?
- What was canonical then?
- What changed, by whom/what, and why?
- What actually happened?
- What was learned or corrected later?

## CORE-03 — Adversarial Reductio

Execute all applicable destructive alternatives:

- REMOVE;
- MERGE;
- SPLIT;
- MAKE UNIVERSAL;
- INVERT;
- EXTREME.

Each result must explain what semantic capability is lost or what artificial complexity appears.

## CORE-04 — Semantic Redundancy / Merge-Split Pair Test

For each nearest-neighbor concept pair ask:

1. different identity?
2. can A change without B?
3. can B change without A?
4. different lifecycle?
5. different authority/provenance?
6. different domain question?
7. different historical query?
8. A without B?
9. B without A?
10. realistic one-without-the-other case?
11. merge causes overloaded state?
12. further split creates behavior or only labels?

Classify:

- DISTINCT;
- SOFT BOUNDARY;
- SPECIALIZATION / PRODUCT LANGUAGE;
- REDUNDANT CANDIDATE;
- DEFERRED.

## CORE-05 — Multidirectional Traceability

Test three directions:

### Downward

Intention/strategy → execution/reality.

### Upward

Reality/import → possible context without fabricating historical intention.

### Lateral

One real fact may affect several Goals/domains without source-object duplication.

## CORE-06 — Orphan / Independence

Test whether the concept can exist without adjacent concepts where semantically legitimate.

Distinguish:

- independent identity;
- contextual identity;
- capability/value semantics;
- derived projection.

A dependency is acceptable only when semantic, not because an early schema made it convenient.

## CORE-07 — External Cross-Domain Benchmark

Benchmark outside personal productivity when another field solves the hard problem better.

Evaluate:

- identity;
- lifecycle;
- correction/history;
- provenance;
- derived versus persisted state;
- queryability;
- extensibility;
- scale;
- offline/sync;
- automation boundary;
- progressive disclosure;
- provider lock-in.

## CORE-08 — External Anti-Pattern Review

Deliberately check for:

- universal generic entity;
- arbitrary JSON core semantics;
- status explosion;
- provider IDs as LifeOS identity;
- duplicated temporal truth;
- calendar presence treated as truth;
- recurrence by date mutation;
- destructive overwrite;
- automation spaghetti;
- forced hierarchy;
- inability to store contradiction;
- simple-user configuration overload.

## CORE-09 — Correction / Reconciliation / Epistemic Integrity

This is explicit in v3 rather than being left implicit inside chronological simulation.

Ask:

- Can a captured value be corrected without erasing material source history?
- Can two providers disagree?
- Can user correction outrank an import without pretending the import never existed?
- Can unknown remain unknown?
- Is absence of evidence incorrectly converted into negative truth?
- Are proposal, inference, confirmation and authoritative fact separable where needed?
- Can retrospective logging exist without fabricated prior intention?

Failure signal:

> current-state convenience destroys the ability to explain how LifeOS came to believe something.

## CORE-10 — Scale / Performance / History Stress

Stress semantics at:

- ten-year history;
- high-volume imports;
- long recurring series;
- many corrections/revisions;
- offline edits;
- multiple providers;
- heavy cross-domain querying.

Ask whether correctness requires eager infinite state, repeated full-history scans or physical duplication of semantic truth.

Physical optimization may later denormalize, but it must not redefine truth.

## CORE-11 — Simple User / Power User

Run the same capability through:

- minimal consumer interaction;
- advanced configuration/history/automation needs.

Fail if simple users must learn the ontology or power users hit an artificial semantic ceiling.

## CORE-12 — Product Value / Complexity Cost

A representable model can still be a bad product model.

Evaluate:

- user decisions introduced;
- configuration burden;
- maintenance burden;
- ambiguity reduced;
- memory/search/coordination burden reduced;
- whether the kernel distinction can remain hidden when not valuable to the user.

## CORE-13 — Implementation Pressure Without Premature Schema

Ask:

- Can high-value queries be expressed?
- Does the concept require stable identity for sync/offline/history?
- Is lifecycle state distinguishable from derived state?
- Can provider mappings remain external?
- Are there obvious persistence contradictions?

Do **not** choose final tables/API shapes at this stage unless the workstream has explicitly reached logical/physical modeling.

---

# 5. Dedicated Multi-Actor Compatibility Gate

After the Core Semantic Gate passes provisionally, rerun the candidate under explicitly multi-actor reality.

This gate uses the following registry.

## MA-01 — Identity / Account Independence

Test:

- one actor;
- multiple actors;
- participant/assignee/performer change;
- non-LifeOS person;
- actor with no account;
- account change without domain-identity change.

Failure signal: domain identity depends on `user_id` coincidence.

## MA-02 — Shared Canonical Fact / Actor-Scoped Overlay

Compare:

```text
one shared canonical object
+ actor-scoped state
```

against per-user semantic duplication.

Test personal reminders, notes, responses, private constraints and local organization around shared truth.

## MA-03 — Responsibility / Assignment / Claim / Substitution

Where applicable stress:

- requester;
- accountable/responsible actor;
- expected performer;
- actual performer;
- unassigned/open work;
- claimable work;
- substitute;
- hand-off recipient;
- fallback responsibility;
- approver.

Changing responsibility must not replace domain identity unless the underlying intention truly changed.

## MA-04 — Coordination Stewardship / Mental Load

Ask who:

- notices work;
- remembers timing/preferences;
- prompts others;
- monitors completion;
- repairs failure.

Do not assume assignment transfers coordination burden.

This test may produce a future relationship requirement or only a product-burden finding; it does not automatically create a primitive.

## MA-05 — Common Ground / State Separation

At higher consequence, verify that the domain can distinguish where necessary:

```text
proposed/sent
!= delivered
!= seen
!= understood
!= acknowledged
!= accepted/agreed
!= authoritative/confirmed
!= acted upon
!= Actual
```

Low-consequence UI may collapse stages; the kernel must not destroy needed semantics.

## MA-06 — Authority / Canonical Change

Ask:

- who may propose?
- who may personally accept?
- who may make shared state canonical?
- who may override?
- is authority external/institutional?
- does creator actually possess authority?

Creation, visibility and participation do not establish authority automatically.

## MA-07 — Selective Disclosure

Test whether collaboration can use a derived consequence without exposing its private source.

Example:

```text
share: unavailable 18:00–20:00
not automatically: medical appointment
```

## MA-08 — Inference Privacy

Inspect leakage through:

- recommendations;
- explanations;
- rankings;
- notification wording;
- derived availability;
- AI responses;
- AI tool/API arguments.

Canonical rule:

> AI/system knowledge does not create disclosure permission.

## MA-09 — Partial Adoption / External Participant

Run important scenarios with:

1. everyone on LifeOS;
2. some participants on LifeOS;
3. only one LifeOS user.

Where relevant also test bounded link/email/provider interaction, assisted participation and non-interacting represented subjects.

## MA-10 — Assisted Participation / Assertion Provenance

When one person helps another, distinguish:

- subject;
- physical actor/enterer;
- asserted-by;
- approved/confirmed-by;
- performer.

Do not record the helper as though the subject personally asserted or performed the fact.

## MA-11 — Relationship Lifecycle / Revocation

Chronologically test:

- join;
- role change;
- temporary substitution;
- access narrowing;
- responsibility transfer;
- leave;
- future access revocation;
- immediate/emergency revocation where relevant;
- retained historical attribution.

Current access and historical participation are different questions.

## MA-12 — Conflict / Adversarial Relationship

Test:

- disagreement;
- refusal;
- silence;
- conflicting reports;
- strategic behavior;
- exit;
- low-trust continuing coordination;
- attempts to turn audit/visibility into surveillance or pressure.

Do not validate only cooperative friendships/teams.

## MA-13 — Unequal Power / Guardian / Caregiver

Where applicable test context-bounded asymmetric authority:

- guardian/minor;
- caregiver/cared-for person;
- manager/worker;
- clinician/patient;
- teacher/student.

Authority must not silently expand visibility or erase subject autonomy outside its proper context.

## MA-14 — Multi-Resource / Capacity

Include people and non-person resources:

- rooms;
- vehicles;
- equipment;
- devices;
- facilities;
- shared capacity pools.

One shared scheduled object must be able to generate independent capacity claims without semantic duplication.

## MA-15 — Coordination-Burden Distribution

For any collaboration behavior ask:

```text
Who sets it up?
Who maintains state?
Who receives notifications?
Who must acknowledge?
Who monitors failure?
Who repairs exceptions?
Who receives the primary benefit?
```

Evaluate total work and its distribution, not organizer efficiency alone.

## MA-16 — Formality / Progressive Disclosure

Run the same semantic capability at:

- low consequence;
- medium consequence;
- high consequence.

Example:

```text
Dinner RSVP
vs
project review acknowledgement
vs
shift/care hand-off with authority
```

The kernel must support necessary formality without forcing it into casual UX.

## MA-17 — AI Authority / Multi-Party Context

Ask:

- on whose behalf is AI acting?
- what authority does that principal have?
- which private contexts may AI use internally?
- what may be disclosed to each recipient?
- is AI proposing, deciding, confirming or explaining?

Canonical rule:

> AI effective authority <= acting principal/context/policy authority.

## MA-18 — Specialist-System Boundary

For healthcare, workforce, education, legal, finance or other specialist contexts ask whether LifeOS is coordinating around externally authoritative truth rather than accidentally rebuilding specialist administration.

## MA-19 — Multi-Actor Primitive Redundancy

Before adding a collaboration primitive, additionally ask:

- can this be a typed Relationship?
- can this be actor-scoped state?
- can this be derived?
- is this only product/UI vocabulary?
- does it have independent identity/lifecycle/authority/query behavior?

## MA-20 — Actor-Scoped Reality Attribution

Mandatory for reality/evidence/execution concepts.

Ask:

- Is there one shared Actual plus actor-specific participation?
- Can different actors have different actual intervals/quantities/outcomes?
- Can planned performer differ from actual performer?
- Can conflicting actor assertions coexist until resolved?
- Does a shared Event occurring imply attendance by every participant? It must not.
- Can reality be corrected per actor without rewriting unrelated shared truth?

This test is especially important for Session, Actual, Outcome, Observation, Confirmation, Evidence and Provenance.

---

# 6. Cross-Concept Consistency Gate

A candidate that passes its own tests may still conflict with the current atlas.

Run:

### XCON-01 — Identity compatibility

No two concepts should accidentally claim the same identity/lifecycle.

### XCON-02 — Ownership / authority compatibility

One concept must not silently override another concept's established authority boundary.

### XCON-03 — Planned / current / actual / historical compatibility

No candidate may collapse existing distinctions.

### XCON-04 — Relationship compatibility

Do not introduce a hidden universal hierarchy or duplicate facts merely because a relation is not yet formally modeled.

### XCON-05 — Multi-actor compatibility

New semantics must remain compatible with Multi-Actor Readiness v1 and previously accepted actor-neutral hardenings.

### XCON-06 — Language-map compatibility

Kernel terminology, product profiles and UI aliases must remain correctly classified. A UI term does not become a primitive through accidental reuse.

---

# 7. Adjacent Dependency Sweep

After the Cross-Concept Consistency Gate and before the final concept verdict, inspect every material boundary or neighboring semantic question exposed by the candidate.

For each dependency ask:

1. Does this dependency materially affect the candidate's identity, lifecycle, authority, history, privacy, arithmetic/evaluation behavior, or query semantics?
2. Is there enough accepted evidence to resolve it now?
3. Would deferring it force the candidate to guess a future model?
4. Which future concept/cluster/logical-model stage owns the unresolved question?
5. What exact trigger requires revalidation?

Every material dependency must receive exactly one closure classification:

### RESOLVED

The neighboring question has enough evidence now and is resolved in the current concept/boundary. Record the resulting invariant/hardening.

### SAFE DEFERRED

The candidate remains valid without deciding the neighboring representation now. A SAFE DEFERRED item must record:

- the unresolved question;
- why it does not block current acceptance;
- the owning future concept/cluster/stage;
- the exact reopening trigger;
- the tests/boundaries that must be rerun.

`SAFE DEFERRED` is not permission to write `TBD` without ownership.

### REOPEN

The dependency exposes a material contradiction or missing semantic decision that prevents current acceptance. Reopen the affected candidate/previous concept immediately rather than carrying the problem forward.

Canonical rule:

> **No material dependency may remain in unclassified limbo at the applicable closure point.**

## Transition rule for Data / Subjects

Because clusters 1–3 were validated before this sweep became mandatory and Data / Subjects has already started, use the following one-time transition:

```text
finish Data / Subjects concept reviews
        ↓
Data / Subjects cluster integration + multi-actor stress
        ↓
DEFERRED DEPENDENCY CLOSURE — clusters 1–4
        ↓
resolve now / safe defer / reopen
        ↓
CROSS-CLUSTER VALIDATION v4 — clusters 1–4
        ↓
only after PASS: Relationships / Reasoning
```

From Relationships / Reasoning onward, execute the Adjacent Dependency Sweep before each concept verdict rather than accumulating a cluster-wide limbo backlog.

---

# 8. Concept verdicts

Only four concept verdicts are allowed.

## PASS

All applicable gates passed with no unresolved material semantic issue.

## PASS WITH HARDENING

The concept survives, but wording/invariants/boundaries require explicit changes before acceptance.

A concept is not accepted until those hardenings are actually incorporated.

## REOPEN

A material identity, lifecycle, authority, privacy, history or redundancy problem remains. The candidate must be redesigned/retested.

## DEFERRED DEPENDENCY

The concept is not currently disproven, but a material decision cannot be completed until an adjacent concept/cluster exists.

A deferred dependency must name:

- what is unresolved;
- which future concept/cluster should resolve it;
- whether the current concept may be accepted despite the dependency;
- what test must be rerun later.

The Adjacent Dependency Sweep adds the operational `SAFE DEFERRED` classification for dependencies that are explicitly non-blocking; this does not add a fifth concept verdict.

`UNCHECKED`, `PROBABLY PASS`, `GOOD ENOUGH`, or silent omission are not valid final states.

---

# 9. Mandatory validation coverage matrix

Every concept checkpoint must include a matrix using stable test IDs.

Minimum columns:

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferred dependency |
|---|---|---|---|---|

Rules:

1. every registered test must appear or be covered by an explicit grouped reference;
2. `N/A` requires a reason;
3. an unresolved applicable failure prevents PASS;
4. a DEFERRED result must identify its reopening trigger;
5. test evidence should point to concrete scenarios, not only general prose;
6. repeated stable evidence may be referenced rather than rewritten in full;
7. every material adjacent dependency must be represented in the dependency sweep/register.

This matrix exists to prevent validation by memory.

---

# 10. Cluster Integration Gate

After all concepts in a cluster are individually accepted, test them as one system.

## CL-01 — Representative reconstruction

Reconstruct representative feature-discovery workflows using only accepted/current concepts.

## CL-02 — Deep integrated chronology

Run several days/weeks/months so lifecycle interactions appear.

## CL-03 — Cross-concept redundancy

Repeat REMOVE/MERGE/SPLIT on the **cluster**, not only on individual concepts.

## CL-04 — Top-down traceability

Can intention/strategy naturally reach schedule/execution/reality?

## CL-05 — Bottom-up reconstruction

Can spontaneous/imported reality acquire context without fabricated intent?

## CL-06 — Lateral propagation

Can one fact affect multiple contexts without duplication?

## CL-07 — History/correction integrity

Can the cluster answer historical questions after revisions and conflicting evidence?

## CL-08 — Scale/product complexity

Does integration create hidden combinatorial complexity or require simple users to configure internals?

---

# 11. Cluster Multi-Actor Stress Gate

Every cluster must then run integrated multi-actor scenarios separately from the ordinary cluster gate.

Minimum scenario families where applicable:

1. shared object with different actor-scoped state;
2. responsibility reassignment/hand-off;
3. actual performer differs from planned performer;
4. external/non-LifeOS participant;
5. private underlying fact with safe shared projection;
6. conflicting actor/provider assertions;
7. access narrowing or revocation;
8. unequal authority;
9. shared non-person resource;
10. AI operating on private multi-party context;
11. coordination burden distributed across actors;
12. collaborative execution with actor-specific Actual attribution.

For the Observed Reality & Evidence cluster, the mandatory stress set includes at least:

```text
A. shared meeting — one Event occurrence, different attendance intervals
B. shared Activity — one responsible actor, multiple performers, partial execution
C. shift hand-off — planned worker != actual worker, authority required
D. caregiving — helper records reality about another Subject with provenance
E. conflicting reality — actor A, actor B and integration disagree
F. external participant — represented without LifeOS account
G. privacy — shared Actual can coexist with private Observation
H. correction — later correction preserves earlier assertion/provenance
I. collaborative Session — common episode, different participation intervals
J. AI — reasons from private facts without disclosing private causes
```

---

# 12. Cluster verdicts

Cluster verdicts use the same four states:

- PASS;
- PASS WITH HARDENING;
- REOPEN;
- DEFERRED DEPENDENCY.

A cluster PASS requires:

- all constituent concepts accepted;
- ordinary cluster integration gate executed;
- cluster multi-actor gate executed;
- no unresolved applicable failure;
- all deferred dependencies recorded with reopening triggers.

A cluster PASS does not erase SAFE DEFERRED dependencies. They remain executable obligations and must be revisited at their registered trigger.

---

# 13. Whole-Domain Gate

Before broad logical/physical persistence is treated as stable, rerun the whole accepted model.

## WD-01 — Whole-domain semantic regression

Re-run cross-domain chronological and adversarial scenarios across all accepted clusters.

## WD-02 — Whole-domain redundancy

Search again for primitives that became redundant only after later clusters were added.

## WD-03 — Whole-domain historical reconstruction

Ask historical questions across intention, scheduling, reality, evidence, relationship and decision layers.

## WD-04 — Whole-domain multi-actor regression

At minimum rerun:

1. friends planning outing;
2. household shared work with open responsibility;
3. team meeting + assigned follow-up;
4. shift swap requiring authority;
5. caregiver hand-off with conflicting evidence;
6. parent/guardian/child coordination;
7. shared resource booking;
8. external non-LifeOS participant;
9. privacy-preserving common-time calculation;
10. relationship revocation;
11. high-conflict continuing coordination;
12. assisted/low-digital participant;
13. collaborative Session/Actual attribution;
14. AI recommendation using private multi-party context.

## WD-05 — Persistence/API pressure test

Only at this stage translate semantics toward logical persistence and API contracts.

Verify that the proposed persistence/API does not accidentally collapse distinctions the Domain Atlas preserves.

## WD-06 — Simple-user regression

Confirm that the accumulated kernel has not leaked into required consumer configuration.

## WD-07 — Specialist-boundary regression

Confirm that LifeOS remains an integrating/personal coordination system rather than silently becoming every specialist system.

---

# 14. Reopening severity and handling

Findings are classified operationally as:

## CRITICAL

Contradiction involving identity, historical truth, authority, privacy, security boundary, source attribution, or an impossible ordinary workflow.

Effect: REOPEN concept/cluster immediately.

## STRUCTURAL

A concept survives only by duplication, overloaded state, universal wrappers, or an unjustified primitive split/merge.

Effect: normally REOPEN or PASS WITH HARDENING if bounded wording/invariants fully resolve it.

## HARDENING

Definition/invariant/boundary needs strengthening but concept identity remains sound.

Effect: PASS WITH HARDENING until the hardening is written and retested.

## DEFERRED DEPENDENCY

Requires an adjacent future model. Must have explicit reopening trigger and one of the dependency-sweep treatments (`SAFE DEFERRED` or `REOPEN`) at the applicable closure point.

## PRODUCT / UX

Kernel survives; issue belongs to progressive disclosure, workflow burden, terminology or product defaults.

Effect: record for product work; does not by itself reopen the kernel.

---

# 15. Regression corpus policy

Important scenarios discovered during any concept/cluster validation become reusable regression evidence.

Promote a scenario into the regression corpus when it exposes at least one of:

- identity boundary;
- lifecycle/history boundary;
- multi-actor state separation;
- privacy/authority boundary;
- contradiction/reconciliation behavior;
- performance/materialization pressure;
- simple-user/power-user conflict;
- specialist-system boundary.

Do not grow the corpus with near-duplicate stories that test nothing new.

The checkpoint should reference existing corpus scenarios whenever possible and add only genuinely new coverage.

---

# 16. Validation execution discipline

## 16.1 Candidate first, verdict later

Do not write the desired verdict first and select confirming scenarios afterward.

## 16.2 Evidence diversity

Use at least multiple domain families when the concept claims universal applicability.

## 16.3 Negative cases are mandatory

Include absent, skipped, unknown, conflict, failure, correction or rejection where applicable.

## 16.4 Multi-actor gate is never inferred

A concept does not pass MA tests merely because its wording is actor-neutral. Execute the relevant scenarios.

## 16.5 `N/A` is explicit

Not every concept needs every test, but omission requires a reason.

## 16.6 Hardening is written before PASS

Do not call the concept PASS and leave the required hardening only in conversation notes.

## 16.7 Deferrals are executable obligations

Every deferral names the future trigger that forces revalidation. From the point at which the Adjacent Dependency Sweep applies, every material deferral must also be classified `SAFE DEFERRED` or force `REOPEN`.

## 16.8 Checkpoints are durable

The durable repository checkpoint, not conversation memory, is the authoritative record of what was actually tested.

## 16.9 Dependency closure precedes forward motion

Do not start a later cluster when the applicable closure plan requires a deferred-dependency sweep or cross-cluster regression first.

---

# 17. Current applicability

The first three accepted clusters are validated current baselines under v3 and Cross-Cluster Validation v3.

Data / Subjects is the transition cluster for the new dependency discipline: finish its concept reviews and cluster gates, then execute a dedicated dependency closure across clusters 1–4 followed by Cross-Cluster Validation v4 before Relationships / Reasoning begins.

From Relationships / Reasoning onward, the Adjacent Dependency Sweep is mandatory before every concept verdict.

All accepted concepts remain reopenable when the sweep, later cluster evidence or final whole-domain regression exposes a material contradiction.

---

# 18. Relationship to historical methodology documents

The following remain preserved for audit/history:

- `validation-methodology-v2.md` — original expanded semantic validation suite;
- `validation-methodology-v2-multi-actor-addendum.md` — evidence-backed detailed multi-actor extension.

V3 integrates and orders those requirements. New validation work should use this document as the primary methodology and may consult the historical documents for rationale/detail where useful.

Canonical operational references:

1. `validation-methodology-v3.md`;
2. `validation-execution-template-v3.md`;
3. `multi-actor-readiness-v1.md`;
4. applicable accepted concept/checkpoint documents;
5. discovery/research evidence where relevant.

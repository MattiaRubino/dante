# Actual v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **An Actual is a persistent contextual realization record representing whether and how a specific intended or expected domain subject was realized in reality. It preserves the realized truth of that expectation without replacing the Sessions, Observations, Outcomes, participation records, Confirmations, or Provenance that describe particular facets of what happened or how LifeOS knows it.**

Actual answers the reconciliation question:

> **How did this specific intention or expectation resolve in reality?**

It does not answer every possible question about reality.

The central distinction is:

```text
Intention / expectation
Activity / Event / Occurrence
          │
          ↓
        Actual
how that expectation was realized
          │
   ┌──────┼─────────┬──────────────┐
   ↓      ↓         ↓              ↓
Session  Outcome  Observation   participation
   │      │         │              │
   └──────┴─────────┴──────────────┘
          ↓
Confirmation / Provenance
          ↓
Evidence when used in evaluation
```

Not every branch is required, and Actual is not a universal parent object for all reality records.

---

# 1. Why Actual exists

LifeOS already separates:

- intended work from actual execution;
- Schedule from actual timing;
- expected Occurrence identity from what happened;
- Session from broader execution result;
- Event expectation from attendance and event outcome;
- source/provenance from truth;
- evidence from the source fact used in an evaluation.

Without Actual, LifeOS would be forced toward one of several weak alternatives:

1. overwrite intended/expected objects with reality;
2. overload Session with all realization semantics;
3. overload Outcome with timing, measurements, and participation;
4. turn Observation into a universal event/fact container;
5. infer non-execution merely from absence of data;
6. create ad-hoc reconciliation logic independently for Activity, Event, and Occurrence.

Actual supplies the contextual bridge between an expectation and its realized reality while keeping the richer facts in their proper concepts.

---

# 2. Actual is contextual, not universal reality

Actual exists because there is a meaningful expected/intended subject whose realization needs to be reconciled.

Canonical guardrail:

> **Observed reality does not require an Actual wrapper when there is no expectation being reconciled.**

Examples that may exist without Actual:

```text
Observation
weight = 66.4 kg
```

```text
Observation
rainfall = 12 mm
```

```text
Session
40 minutes of spontaneous debugging
```

```text
Imported transaction
€18.50 grocery purchase
```

If later analysis finds those facts relevant to a Goal or Plan, LifeOS may relate them without fabricating a historical intention that did not exist.

Therefore:

> **Actual is a realization/reconciliation concept, not the database of everything that happened.**

---

# 3. Actual versus Session

Session answers:

> **When did this logically continuous execution episode actually take place?**

Actual answers:

> **How was the related intended/expected subject realized overall?**

Example:

```text
Activity
Write report

Sessions
Monday 18:00-19:10
Tuesday 20:00-21:25
Wednesday 17:30-18:00

Actual
realization of the Activity across those execution episodes

Outcome
completed
```

There are three Sessions and normally one Actual for the Activity realization.

Conversely, an ordinary Event can have an Actual occurrence without requiring a Session:

```text
Event
Client meeting

Schedule
10:00-11:00

Actual
meeting occurred 10:08-11:23
```

Creating a Session merely to record that an Event happened would duplicate semantics unless distinct performed-work tracking is genuinely needed.

Therefore:

> **Actual != Session.**

---

# 4. Actual versus Outcome

Outcome describes the result/disposition of the realized expectation.

Actual provides the contextual realization to which that result belongs.

Examples:

```text
Actual
meeting occurred 10:08-11:23

Outcome
decision postponed
```

```text
Actual
training occurrence was performed

Outcome
partially completed
```

```text
Actual
expected activity was not performed

Outcome
skipped
```

Outcome may carry domain-specific result semantics that do not belong to Actual itself.

Therefore:

> **Actual != Outcome.**

The exact Outcome ontology is reviewed separately.

---

# 5. Actual versus Observation

Observation represents a measured, perceived, asserted, imported, or otherwise observed fact about reality.

Examples:

```text
Observation
distance = 3.8 km
```

```text
Observation
pain = 4/10
```

```text
Observation
weight = 66.4 kg
```

Observations may contextualize an Actual, but they do not become Actual merely because they are true facts.

Example:

```text
Activity
Run 5 km

Actual
realized execution of this Activity

Session
18:07-18:43

Observations
- distance = 3.8 km
- average HR = 155 bpm

Outcome
partial
```

The distance and heart-rate data remain Observations rather than duplicated fields on Actual.

Therefore:

> **Actual != Observation.**

---

# 6. Actual versus Evidence

Evidence is contextual use of information in an evaluation.

A reality record may exist independently of whether it is later used as Evidence.

Example:

```text
Observation
walked 10.4 km
```

Later:

```text
Goal
walk >= 30 km/week
```

The Observation may be used as Evidence for that criterion.

LifeOS must not rewrite the source Observation or Actual to claim that the Goal was the original reason for the walk.

Therefore:

> **Actual != Evidence.**

Evidence semantics are reviewed separately.

---

# 7. Actual versus Confirmation and Provenance

Actual represents realized domain truth as currently accepted in context.

Confirmation and Provenance explain epistemic and source history around that truth.

Examples:

```text
Actual
run partially realized

Provenance
Garmin import

Correction
user changed distance

Confirmation
user accepted corrected result
```

A source does not automatically become authority merely because it supplied the record.

An AI inference does not become canonical Actual merely because it is plausible.

Canonical guardrails:

```text
source != truth
provenance != Actual
inference != confirmed Actual
```

The detailed models for Confirmation and Provenance remain separate reviews.

---

# 8. Unknown versus known non-realization

This is a core Actual invariant.

Example:

```text
Occurrence
Take medicine at 20:00

22:00
no user response
no trusted source
```

LifeOS knows the expectation existed. It does **not** know the realization.

Canonical representation:

```text
Actual
not established / absent
```

This must not be interpreted as:

```text
not taken
missed
skipped
failed
```

Now consider:

```text
User confirms
I did not take it
```

Reality is now known:

```text
Actual
known non-realization of the expected occurrence

Outcome
skipped / not performed

Provenance
user declaration
```

Therefore:

> **No established Actual != known non-realization.**

And:

> **Passage of time does not establish Actual.**

This preserves the existing LifeOS rule that scheduled time passing does not imply completion or failure.

---

# 9. Positive realization is not required

Actual is not equivalent to successful execution.

A valid Actual may establish that:

- the expectation was fully realized;
- it was partially realized;
- it was realized differently from the plan;
- it was replaced by another execution;
- it did not occur;
- an Event occurred but an expected participant did not attend;
- the intended work happened through several Sessions;
- the realized result remains qualitatively unresolved even though occurrence/execution is known.

This keeps reality and evaluation separate.

---

# 10. Replacement and substitution

Replacement must preserve both original expectation and actual resolution.

Example:

```text
Activity A
Take bus to appointment

Actual A
not realized as planned

Replacement
Taxi ride

Outcome A
replaced
```

The replacement may itself have its own Activity/Actual or exist as retrospective reality depending on whether it was intended before execution.

LifeOS must not mutate Activity A into `Take taxi` merely because that is what happened.

The exact typed replacement Relationship remains deferred.

---

# 11. Corrections and competing assertions

Actual is persistent contextual truth, but LifeOS must preserve how the current accepted representation was reached.

Example:

```text
Provider import
meeting ended 11:20

Participant assertion
meeting ended 11:25

Organizer correction
meeting ended 11:23
```

The final current representation may become:

```text
Actual
10:08-11:23
```

but audit/provenance must preserve relevant earlier assertions and authority/context.

Canonical rule:

> **Correction changes current accepted realized truth without silently deleting the assertion history that produced it.**

Actual does not itself define the conflict-resolution algorithm. That belongs to Authority/Provenance/Version/Decision/reconciliation design.

Authority v0 now fixes one part of that boundary: **Authority answers who/what may legitimately make a bounded reconciliation/correction effect effective; Authority does not itself prove which assertion is objectively true and does not replace Actual.**

---

# 12. Shared Actual and actor-scoped reality

Multi-actor reality must not flatten a shared occurrence and individual participation into one fact.

Example:

```text
Shared Event
Project meeting

Shared Actual
meeting occurred 10:08-11:23
```

Actor-specific reality:

```text
Mattia
participated 10:08-11:23

Luca
participated 10:08-10:45

Sara
did not attend
```

The shared Event Actual does not establish identical attendance for every participant.

Canonical rule:

> **Shared Actual != actor-specific Actual participation.**

Likewise for collaborative Activity execution:

```text
Activity
Move sofa upstairs

Actual
activity realized

Collaborative Session
17:00-17:30

Mattia participation
17:00-17:30

Luca participation
17:05-17:25
```

The Session envelope does not imply equal actor participation duration.

The exact Participation/Relationship persistence is deferred, but Actual must remain compatible with those distinctions.

---

# 13. Assisted and delegated reality

The actor who enters or confirms reality may differ from:

- the subject;
- the responsible actor;
- the expected performer;
- the actual performer;
- the person whose outcome is being tracked.

Example:

```text
Medication Occurrence
Subject: older adult

Actual
medicine taken

Actual performer
caregiver assisted administration

Recorded by
caregiver
```

LifeOS must not record the cared-for person as having personally entered or asserted the fact merely because they are the subject.

---

# 14. Privacy and selective disclosure

An Actual may depend on private underlying facts while another actor is authorized to see only a derived consequence.

Example:

```text
Private Event Actual
medical appointment occurred 18:00-20:00

Shared authorized projection
unavailable 18:00-20:00
```

The ability to compute or use the private Actual does not imply permission to disclose it.

Visibility v0 now makes this boundary canonical:

```text
Visibility(derived projection)
!= Visibility(private Actual)
!= Visibility(underlying Observation/Evidence/Provenance/Participation)
```

A recipient may legitimately see the consequence without seeing the Actual or source cause. Conversely, a visible Actual does not automatically expose every supporting source, participant relation, or lineage detail.

Canonical rule:

> **AI/system knowledge or authorized processing of Actual does not create disclosure permission.**

---

# 15. Identity and continuity

Actual requires stable contextual identity independent from ordinary corrections to its content.

If an imported end time is corrected from 11:20 to 11:23, the realization remains the same Actual unless the correction establishes that the original record referred to a different real-world realization.

Actual identity must not be derived solely from timestamps or provider IDs.

A provider record may map to an Actual or supporting record, but provider identity remains integration/provenance context rather than LifeOS canonical identity.

The physical identifier and version model remain deferred.

---

# 16. Cardinality and scope

The semantic default is one contextual Actual for one realized/reconciled expectation, but the physical relationship must not be frozen prematurely.

Potential complications include:

- an Activity realized through multiple Sessions;
- composite work where sub-Activity Actuals coexist with parent-level realization;
- Event occurrence plus actor-specific participation facts;
- replacement/substitution chains;
- imported duplicates later reconciled;
- one expectation whose realization is progressively established over time.

Current guardrail:

> **Do not multiply Actual records merely because reality has multiple facets. Split only when distinct realization identities/lifecycles are demonstrated.**

---

# 17. Derived comparisons

LifeOS may derive comparisons between expectation and Actual, for example:

```text
started 20m early
finished 23m late
performed 3.8 km of planned 5 km
2 of 3 intended sections completed
actual performer differed from expected performer
```

These comparisons are contextual projections, not universal fields on Actual.

Derived comparison must not rewrite either the original expectation or the accepted Actual.

---

# 18. External benchmark findings

External systems were used as evidence, not copied as LifeOS architecture.

## FHIR Procedure / Observation / Provenance

Useful pattern:

- a performed action/occurrence can have its own realization record;
- measurements/simple assertions remain separate Observation records;
- Provenance remains separate metadata describing how records were produced/changed.

LifeOS adapts this separation but does not inherit healthcare-specific resource structure.

## Android Health Connect

Useful pattern:

- an exercise session is a central workout record;
- heart rate, speed, distance and other measurements remain separate associated record types;
- planned exercise sessions and executed sessions are distinct record concepts.

LifeOS is already broader because Session is specifically temporal execution while Actual captures contextual realization beyond workout/session semantics.

## FHIR Task anti-pattern for LifeOS kernel

FHIR Task intentionally tracks an activity across intended/initiated/completed workflow state in one resource.

That can be appropriate for a specialist workflow engine, but LifeOS rejects importing that collapse into the general kernel because accepted LifeOS semantics intentionally distinguish Activity intention, Schedule, Session, Actual, Outcome and Provenance.

Classification:

```text
FHIR Procedure/Observation/Provenance separation -> ADAPT
Health Connect session + associated measurements  -> ADAPT
FHIR Task intention/execution collapse            -> ANTI-PATTERN for LifeOS core
```

---

# 19. Current invariants

1. `Actual != Activity`.
2. `Actual != Event`.
3. `Actual != Occurrence`.
4. `Actual != Schedule`.
5. `Actual != Session`.
6. `Actual != Outcome`.
7. `Actual != Observation`.
8. `Actual != Evidence`.
9. `Actual != Confirmation`.
10. `Actual != Provenance`.
11. Actual reconciles one intended/expected subject with realized reality.
12. Actual is contextual rather than a universal reality container.
13. Observed reality may exist without Actual when no expectation is being reconciled.
14. No established Actual does not imply failure, miss, skip, cancellation or non-execution.
15. Passage of time does not establish Actual.
16. A valid Actual may establish known non-realization.
17. Successful completion is not required for Actual to exist.
18. One Activity/Occurrence may use multiple Sessions while retaining one broader realization context.
19. Ordinary Event occurrence does not require a redundant Session.
20. Actual does not duplicate measurements whose proper identity belongs to Observation or other specialist facts.
21. Actual does not own source/Authority/confidence semantics that belong to Provenance/Confirmation/governance.
22. Correction updates current accepted realization while preserving relevant assertion history.
23. Actual identity does not depend solely on timestamps or provider identity.
24. Shared Actual does not establish identical actor-specific participation.
25. Subject, recorder, responsible actor, expected performer and actual performer may differ.
26. Private Actual may yield authorized derived projections without disclosing its source facts.
27. AI knowledge of Actual does not create disclosure Authority or Visibility for a recipient.
28. Later relevance does not fabricate historical intention.
29. Replacement/substitution preserves the original expectation rather than rewriting it.
30. Physical persistence/cardinality remains deferred until adjacent Reality/Evidence concepts are validated.
31. Reported/asserted reality does not automatically establish Actual; conflicting assertions may remain unresolved until the applicable reconciliation/Authority/policy context establishes a current realization.
32. Authority to establish/correct a current Actual interpretation does not make that interpretation infallible truth.
33. Visibility of an Actual/projection does not imply Visibility of all supporting sources, Provenance, Evidence, or Participation details.

---

# 20. Stress-test coverage

Representative cases validated under Methodology v3 include:

| Scenario | Representation/result |
|---|---|
| Run planned 5 km, performed 3.8 km | Activity + Actual + Session + Observation + later Outcome |
| Report written across three work episodes | one Activity realization + multiple Sessions |
| Meeting planned 10-11, occurred 10:08-11:23 | Event + Schedule + Actual; no artificial Session required |
| Medication time passed, no response | no established Actual; outcome remains unknown |
| User confirms medication not taken | Actual known non-realization + Outcome/Provenance |
| Spontaneous debugging | Session may exist without fabricated Activity/Actual |
| Weight measurement | Observation without Actual wrapper |
| Planned bus replaced by taxi | original expectation preserved + Actual non-realization/replacement relation |
| Conflicting provider/user times | assertions preserved until reconciliation; current Actual established only under applicable reconciliation context |
| Shared meeting with partial attendance | shared Event Actual + actor-scoped participation reality |
| Collaborative sofa move | shared execution context + actor-specific participation intervals |
| Caregiver enters fact for cared-for person | subject/performer/recorder remain separable |
| Private medical appointment | private Actual may support shareable unavailable projection |
| AI infers likely completion | inference does not become canonical Actual without Authority/policy |

No reviewed case requires Actual to become a universal fact object or to absorb Session, Outcome, Observation, Confirmation, or Provenance.

---

# 21. Deliberately deferred questions

Actual v0 does not decide:

- exact Outcome ontology/state/value-object design;
- exact Observation model;
- exact Evidence role/record model;
- exact Confirmation/acknowledgement model;
- exact Provenance/source/assertion model;
- exact replacement Relationship type;
- exact Version/Decision model;
- exact physical cardinality/table shape;
- whether some specialist domains use specialized realization records in addition to Actual;
- API and PostgreSQL representation.

Participation, Authority, and Visibility semantic boundaries are now resolved. Still mandatory later re-tests include:

- Actual establishment under future Decision/reconciliation semantics;
- final Principal/enforcement mapping;
- final whole-domain multi-actor and persistence-pressure gates.

---

# 22. Decision note

Actual v0 is accepted as the current contextual realization concept for the Domain Atlas.

The accepted shape is deliberately narrow:

```text
expected/intended subject
        ↕
contextual Actual realization
```

It is **not** accepted as:

```text
universal Reality object
universal Event log
Session replacement
Outcome container
Observation container
Evidence container
Provenance container
```

Future adjacent concepts may harden the boundary, but any proposal to broaden Actual into a generic reality mega-entity must explicitly reopen this decision under Methodology v3.

---

# 23. Cross-cluster v3 hardening — assertions do not establish Actual by themselves

The first-three-cluster regression exposed the need to make the epistemic boundary explicit.

Scenario:

```text
Actor A: medicine taken
Actor B: medicine not taken
Device: dispenser unopened
```

LifeOS may preserve these as separate assertions/Observations with their own Provenance and optional Confirmations while the realization remains unresolved.

Canonical rule:

> **Reported or asserted reality is not automatically established Actual. Actual represents the currently established realization in context; conflicting assertions may coexist without creating multiple competing canonical Actuals or forcing premature resolution.**

Authority v0 now supplies the governance boundary for who/what may legitimately make a bounded reconciliation effect effective; Decision/reconciliation still owns how competing evidence is adjudicated. Authority remains separate from truth and from Actual itself.

---

# 2026-08-12 — Participation v0 closure amendment

Participation v0 resolves the previously deferred actor-participation boundary while preserving Actual as shared/contextual realization.

Current authoritative separation:

```text
Shared Event Actual
= how the shared expected occurrence resolved

Participation response
= actor-scoped intended/expressed stance

Actual Participation
= actor-scoped reality of involvement
```

Therefore:

```text
shared Actual != identical actor-specific Actual Participation
Participation response != Actual Participation
accepted != attended
declined != proved absent
no attendance evidence != established absence
```

Actual Participation may contain actor-specific actual state/intervals without becoming a Session by default. Provider attendance telemetry remains supporting source/Evidence/Provenance until the applicable reconciliation/Authority context establishes current Participation truth.

The older `exact actor Participation model` deferral is superseded at the semantic level by `concepts/participation.md`. Exact direct/qualified persistence, Acceptance/Acknowledgement integration, provider reconciliation and retention remain SAFE DEFERRED.

No Actual identity/cardinality rule changes: multiple actor Participation facets do not justify multiplying the shared Actual merely because reality has several participant-specific facets.

See:

- `concepts/participation.md`;
- `checkpoints/participation-v0-validation.md`.

---

# 2026-08-12 — Authority + Visibility closure amendment

Authority v0 and Visibility v0 close two core Actual dependencies without changing Actual's realization semantics.

```text
Actual
= currently established contextual realization

Authority
= who/what may legitimately make a bounded establishment/correction effect effective

Visibility
= what bounded representation of Actual or its projections may be exposed
```

Therefore:

```text
Authority != Actual
Authority != truth
Visibility != Actual
visible projection != visible private Actual/source
```

A correction may be authoritative in context and still be historically traceable/correctable later. A recipient may see a safe consequence without seeing the private Actual, its participant relations, Evidence, or full Provenance. AI may process authorized source Actuals but must independently satisfy output Visibility before disclosing them or source-revealing inferences.

Decision/reconciliation, detailed enforcement, and retention remain separately deferred.

---

# 2026-08-13 — Decision / reconciliation closure amendment

Decision v0 closes the semantic part of the earlier `Decision/reconciliation` dependency without changing what Actual means.

Current canonical separation:

```text
assertions / Observations / source reports
→ may conflict

Reconciliation
= process/pattern for comparing/selecting/merging/correcting/splitting or retaining conflict

Decision
= bounded contextual resolution to a specific result where an explicit material resolution occurs

Actual
= current established contextual realization
```

Therefore:

```text
Decision != Actual
Decision != objective truth
Reconciliation != Actual
Authority != Decision
Authority != Actual
```

A Decision may establish/correct which interpretation becomes current under the applicable Authority/policy, but it does not make that interpretation infallible and does not erase the competing assertions that led to it.

A deterministic reconciliation rule may update the current Actual under already-authorized policy without fabricating a human Decision. Conversely, a Decision may reject a proposed correction and leave the current Actual unchanged.

Required history remains:

```text
prior assertions/versions
+ reconciliation basis/process where material
+ Decision where material
+ resulting current Actual
+ later correction/reversal
```

The affected `Actual` concept owns its current realized-state transition. No universal `EffectiveChange` object is introduced.

Version/material-equivalence mechanics, detailed reconciliation/source-precedence policy, Principal/enforcement and physical Actual persistence remain SAFE DEFERRED.

**Actual v0 verdict is unchanged. REOPEN = 0.**

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 closes Actual's former `Version / material-equivalence` semantic dependency without changing Actual's realization meaning.

Canonical separation:

```text
Actual identity
= the contextual realization being established/reconciled

Actual material state
= the materially relevant current representation of that realization

Version
= a reference to that materially relevant state for a defined purpose/facet
```

Therefore:

```text
Actual identity != Actual Version
correction != new Actual identity by default
provider/ETag revision != material Actual revision automatically
```

Where an assertion, Confirmation, Decision, reconciliation result or derived comparison concerns a particular Actual state, it binds to the material state it actually evaluated. A later material correction does not silently rewrite the earlier evaluation or make it apply to the corrected state by default.

Competing Actual assertions may diverge from a shared prior state and remain simultaneously attributable until the applicable reconciliation/Authority/Decision policy selects or constructs the current interpretation. Version therefore preserves divergence/history; it does not choose the winner.

Materiality is purpose/facet scoped: a metadata-only or unrelated private-facet change need not invalidate every use of the Actual, while a change to the fact relied upon by an evaluation does. Historical state references may remain reconstructible without retaining every sensitive payload indefinitely.

The historical `Version / material-equivalence` dependency is now downstream-closed at the semantic boundary. Detailed reconciliation/source precedence, Principal/enforcement, retention and physical persistence remain independently owned.

No Actual hardening failed. **Actual remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.

---

# 2026-08-13 — Reconciliation / Source Precedence downstream closure amendment

Reconciliation v0 closes Actual's former detailed reconciliation/source-precedence semantic dependency without changing Actual identity or realization semantics.

Canonical separation:

```text
competing assertions / material states
= candidate accounts of the same bounded realization

Reconciliation
= process/capability that handles their competition under an applicable bounded basis

Actual
= current established contextual realization owned by Actual semantics
```

Therefore:

```text
Reconciliation != Actual
source recency != Actual truth
source identity != Authority != truth
unresolved conflict is valid
```

Reconciliation may preserve competing assertions unresolved, apply bounded source-of-record policy, use Evidence and Provenance, culminate in a Decision, or deterministically establish/correct the current Actual under already-authorized policy. It must not fabricate a human Decision or silently use last-write-wins, provider-always-wins or user-always-wins.

Where resolution establishes a new material Actual state, Version preserves the predecessor/current state relationship and Provenance preserves the materially relevant basis/lineage. Earlier assertions remain historical facts; later correction does not rewrite what those sources originally asserted.

The affected Actual owns the resulting current/effective realization. Reconciliation owns neither Actual identity nor universal truth. Conflict/source/basis Visibility remains independently governed.

The historical detailed reconciliation/source-precedence dependency is now downstream-closed at the semantic boundary. Per-domain precedence policy, Principal/enforcement, native-identity deduplication, retention and physical persistence remain separately owned.

No Actual hardening failed. **Actual remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `reconciliation.md`;
- `../checkpoints/reconciliation-source-precedence-v0-validation.md`.
# Outcome v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-11  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Observed Reality & Evidence cluster

## Canonical definition

> **An Outcome is a contextual representation of the result or disposition established for a specific Actual realization, describing what that realization achieved, produced, satisfied, failed to satisfy, or otherwise resolved in the relevant evaluation context. Outcome does not replace lifecycle/operational state, Observations or measurements, produced artifacts, Milestone attainment, Confirmation, Provenance, or actor-specific participation facts.**

Outcome answers the result question:

> **What resulted from this realized expectation, in the context that currently matters?**

Outcome is therefore downstream of realization semantics but does not absorb every fact produced by reality.

Conceptually:

```text
Intention / expectation
Activity / Event / Occurrence
          │
          ↓
        Actual
how it was realized
          │
          ↓
       Outcome
what resulted / how it resolved
```

Additional reality may remain separate:

```text
Session       -> actual execution episode
Observation   -> measured/asserted fact
Artifact      -> produced file/object/output
Milestone     -> contextual meaningful checkpoint
Confirmation  -> epistemic/acceptance state
Provenance    -> source / assertion / correction history
Participation -> actor-specific involvement
```

---

# 1. Why Outcome exists

LifeOS needs to distinguish between:

- whether/how an expectation was realized (`Actual`);
- when execution happened (`Session`);
- what measurable/asserted facts were observed (`Observation`);
- what result/disposition followed (`Outcome`);
- what larger checkpoint became true (`Milestone`);
- how LifeOS knows or accepts the result (`Confirmation` / `Provenance`).

Without Outcome, LifeOS would be pushed toward weak alternatives:

1. one overloaded `status` field attempting to represent planning state, execution state, result, certainty, and history;
2. storing result meaning directly on Activity/Event/Occurrence and rewriting intention objects with reality;
3. overloading Observation so every semantic conclusion becomes a measurement record;
4. overloading Milestone with local execution-result semantics;
5. interpreting produced artifacts or measurements as the result itself;
6. duplicating domain-specific result logic independently across every Activity/Event subtype.

Outcome provides a bounded place for result/disposition semantics while preserving the facts and history from which that result may be established.

---

# 2. Outcome is contextual rather than universal

Outcome is not required for every Actual or every reality record.

Examples where Outcome is meaningful:

```text
Activity
Run 5 km

Actual
run performed

Outcome
partially completed
```

```text
Event
Exam

Actual
exam occurred

Outcome
passed
```

```text
Event
Design review

Actual
review occurred

Outcome
changes requested
```

Examples where no Outcome may be needed:

```text
Event
Birthday gathering

Actual
event occurred
```

```text
Observation
weight = 66.4 kg
```

```text
Session
40 minutes spontaneous debugging
```

Canonical guardrail:

> **Outcome exists only when a result/disposition has semantic value; LifeOS must not manufacture meaningless outcomes for every realized fact or occurrence.**

---

# 3. Outcome versus Actual

Actual answers:

> **How did this expectation resolve in reality?**

Outcome answers:

> **What result/disposition followed from that realization?**

Examples:

```text
Actual
meeting occurred 10:08-11:23

Outcome
decision postponed
```

```text
Actual
expected workout was not performed

Outcome
skipped
```

```text
Actual
exam occurred

Outcome
passed
```

Actual may exist without a meaningful Outcome, and Outcome does not replace realization itself.

Therefore:

> **Outcome != Actual.**

---

# 4. Outcome versus lifecycle / operational state

Lifecycle or operational state describes where an object/process currently is.

Outcome describes the result/disposition of a realized expectation.

These dimensions must not be collapsed.

Examples:

```text
Operational state
closed

Outcome
partially completed
```

```text
Event state
finished

Outcome
no decision reached
```

```text
Process state
completed

Outcome
failed validation
```

External systems frequently preserve this distinction. FHIR Procedure separates resource/process status from outcome, and GitHub Checks separates execution status from final conclusion.

Canonical rule:

> **`completed`, `closed`, `cancelled`, `in progress`, and similar lifecycle/operational states do not by themselves define Outcome.**

Some words can appear in both ordinary language and result semantics; their domain meaning must come from context rather than one universal enum.

---

# 5. Outcome versus Observation

Observation represents a measured, perceived, asserted, imported, or otherwise observed fact.

Outcome represents a contextual result/disposition established from the realization and, where applicable, one or more facts.

Example:

```text
Event
Exam

Observation
score = 78/100

Outcome
passed
```

The score is not the Outcome.

Another example:

```text
Activity
Run 5 km

Observation
distance = 3.8 km

Outcome
partially completed
```

The observation may support or determine the Outcome under a known rule, but the concepts answer different questions.

Therefore:

> **Outcome != Observation.**

Outcome must not become a generic measurement store.

---

# 6. Outcome versus produced output / artifact

Execution may produce tangible or digital outputs:

```text
report.pdf
photo set
invoice
code patch
recording
prescription
exported file
```

Those outputs are not automatically Outcome.

Example:

```text
Activity
Prepare report

Actual
work performed

Produced artifact
report.pdf

Outcome
completed and accepted
```

The artifact may be Evidence for the Outcome, may exist independently, and may have its own lifecycle.

Therefore:

> **Outcome != produced output/artifact.**

No universal `output = Outcome` mapping is accepted.

---

# 7. Outcome versus Milestone

Milestone is a contextual checkpoint whose significance comes from a broader Goal/Plan path.

Outcome is the result/disposition of a specific realization.

Example:

```text
Event
Design review

Outcome
changes requested

Milestone
Design approved
not reached
```

or:

```text
Event
Exam

Outcome
passed

Milestone
Certification checkpoint reached
```

A Milestone may be reached through one Outcome, multiple Outcomes, external Evidence, imported state, a threshold, or another qualifying fact.

Therefore:

> **Outcome != Milestone.**

The Milestone-vs-Outcome watchlist remains satisfied by this separation and will be re-tested at the Reality/Evidence cluster checkpoint.

---

# 8. Outcome versus Confirmation / Provenance

Outcome describes result meaning.

Confirmation/Provenance describe how LifeOS knows, accepts, attributes, or reconciles the result.

Example:

```text
Outcome
passed

Source assertion
university result import

Confirmation
authoritative external result
```

or:

```text
Outcome
completed

Source assertion
AI inference

Confirmation
provisional / awaiting authorized confirmation
```

The same claimed Outcome may have different epistemic states depending on source, authority, and reconciliation.

Therefore:

> **Outcome != Confirmation and Outcome != Provenance.**

An assertion that an Outcome occurred must not silently become canonical merely because it was received.

---

# 9. Outcome taxonomies are contextual, not universal

LifeOS must not define one global enum that attempts to serve every domain.

Possible outcome semantics include, depending on context:

```text
completed
partially completed
skipped
known not performed
replaced
passed
failed
approved
rejected
won
lost
decision reached
decision deferred
changes requested
resolved
unresolved
```

These do not all share one universal lifecycle or applicability.

For example:

- `passed` is meaningful for exams/tests but not groceries;
- `approved` may be meaningful for review/authorization contexts;
- `skipped` applies to an expected execution but not every Event;
- `replaced` requires relationship/history semantics;
- `decision deferred` may be a meaningful meeting Outcome;
- `completed` can be result language for some Activity contexts but must not be confused with generic operational state.

Canonical rule:

> **Outcome is a semantic capability with contextual result vocabulary; no one-size-fits-all Outcome enum is accepted at the domain level.**

The logical/physical model may later provide typed result families or extensible validated structures without weakening this invariant.

---

# 10. Unknown result versus known negative result

Outcome inherits the epistemic distinction established by Actual.

```text
Expectation elapsed
no reliable information
```

must not automatically produce:

```text
Outcome
missed / failed / not completed
```

By contrast:

```text
user confirms not performed
```

may establish:

```text
Actual
known non-realization

Outcome
skipped / known not performed
```

Canonical rule:

> **Absence of an Outcome is not itself a negative Outcome. Unknown, unconfirmed, and known-negative reality must remain distinguishable.**

`unconfirmed` belongs to Confirmation/epistemic semantics rather than being treated as a universal Outcome value.

---

# 11. Partial and replacement semantics

Partial execution is not universally failure.

Example:

```text
Activity
Run 5 km

Observation
3.8 km

Outcome
partial
```

Whether that partial result is acceptable for a Goal/criterion belongs to contextual evaluation, not the Outcome record alone.

Replacement similarly requires preserved relationship/history:

```text
Expected transport
train

Actual realization
train not used

Replacement
rental car
```

The original expectation must remain historically reconstructible.

Outcome may express a replacement disposition where useful, but the relationship to the replacement object must not be flattened into one text/status field.

---

# 12. Outcome and Evidence

An Outcome can itself become Evidence in a later evaluation, but Evidence is contextual use rather than intrinsic identity.

Example:

```text
Outcome
exam passed
        ↓ used by
Evidence relation
        ↓
Milestone
Certification checkpoint reached
```

Another example:

```text
Outcome
weekly review accepted
        ↓
Evidence for Plan checkpoint
```

Canonical rule:

> **Outcome may participate as Evidence, but Outcome != Evidence.**

The same Outcome may support several evaluations without being duplicated.

---

# 13. Multi-actor Outcome semantics

A shared Actual may have a shared/common Outcome while actor-specific results remain distinct.

Example:

```text
Shared Event
Project meeting

Shared Actual
meeting occurred

Shared Outcome
decision postponed
```

Actor-specific consequences may differ:

```text
Mattia -> follow-up Activity assigned
Luca   -> no action
Sara   -> did not attend
```

Those facts must not be flattened into the shared Outcome.

Another scenario:

```text
Manager assertion
work accepted

Customer assertion
changes required
```

These may be competing contextual assertions rather than one universal Outcome.

Canonical guardrails:

1. **Shared Outcome does not imply identical actor-specific consequences.**
2. **One actor's asserted Outcome does not automatically become canonical for every context.**
3. **Authority, source, confirmation, and provenance remain separate from Outcome identity.**
4. **Actor-specific participation or personal evaluation should not be hidden inside a shared Outcome blob.**
5. **Non-LifeOS actors may be source/subject/participant in Outcome-related reality without requiring an account.**

---

# 14. Corrections and reconciliation

Outcome can be corrected when later authoritative information changes the accepted result.

Example:

```text
Initial import
Outcome: passed

Later correction
Outcome: failed
```

The current accepted Outcome may change, but LifeOS must preserve enough history to understand:

- previous assertion/result;
- source;
- correction source;
- effective time where relevant;
- reason/context where available;
- authority/confirmation state.

A corrected Outcome does not rewrite earlier knowledge as though the earlier assertion never existed.

The exact version/provenance persistence is deferred.

---

# 15. AI boundary

AI may:

- infer a provisional likely Outcome from trusted facts;
- suggest an Outcome classification;
- explain which Observations support an Outcome;
- surface conflicting assertions;
- propose follow-up/replanning based on accepted Outcomes.

AI must not:

- silently convert uncertainty into a confirmed result;
- reveal private source facts merely to explain a shared Outcome;
- treat its own recommendation as authoritative Outcome;
- overwrite source/authority history;
- interpret every partial result as failure;
- convert lifecycle state into Outcome without semantic basis.

Canonical rule:

> **AI inference may propose Outcome semantics but does not establish authority, confirmation, or disclosure permission.**

---

# 16. Identity and persistence implications

This concept review establishes Outcome semantics, not its final storage shape.

Outcome may later become:

- a contextual record/value associated with Actual;
- a typed result structure;
- one or several domain-specific result components;
- a relation-backed result assertion where conflicting contexts exist.

No decision is made yet that Outcome must be:

- an aggregate root;
- a standalone SQL table;
- a single enum column;
- one JSON blob;
- one record per Session;
- one record per participant.

Physical cardinality depends on Observation, Confirmation, Provenance, Relationship, and logical data model reviews.

---

# 17. Current invariants

1. `Outcome != Actual`.
2. `Outcome != Session`.
3. `Outcome != Observation`.
4. `Outcome != produced output/artifact`.
5. `Outcome != Milestone`.
6. `Outcome != Confirmation`.
7. `Outcome != Provenance`.
8. `Outcome != Evidence`.
9. Outcome describes result/disposition of a specific realization in a relevant context.
10. Outcome is optional; not every Actual/Observation/Event requires one.
11. No universal Outcome enum is accepted.
12. Lifecycle/operational state and Outcome remain distinct dimensions.
13. Absence of Outcome is not a negative Outcome.
14. `unconfirmed` is epistemic/Confirmation semantics, not universal Outcome semantics.
15. Partial does not universally mean failure.
16. Produced files/records/measurements are not automatically Outcomes.
17. Replacement must preserve relationship/history rather than collapse into one status field.
18. An Outcome may later be used as Evidence without becoming Evidence intrinsically.
19. Shared Outcome does not imply identical actor-specific consequences or participation.
20. One actor/provider assertion does not automatically establish a universal canonical Outcome.
21. Corrections preserve relevant prior assertion/provenance history.
22. AI inference does not create canonical authority or disclosure permission.
23. Provider identity does not define Outcome identity.
24. Final aggregate/value-object/table shape remains deferred to logical/persistence design.

---

# 18. Representative stress cases

| Scenario | Representation |
|---|---|
| Run planned 5 km, actual 3.8 km | Observation 3.8 km + Outcome partial |
| Exam score 78/100 and pass threshold met | Observation score + Outcome passed |
| Design review happened, changes requested | Actual occurred + Outcome changes requested |
| Meeting happened but no decision | Actual occurred + Outcome decision deferred/unresolved where semantically useful |
| Birthday occurred normally | Actual may exist; no Outcome required |
| User did not perform expected Routine occurrence | Actual known non-realization + contextual Outcome skipped/not performed |
| No response after expected occurrence | no automatic Outcome; unknown/Confirmation semantics |
| Report produced and approved | produced artifact + Outcome completed/accepted |
| Manager accepts work, customer rejects | competing contextual assertions; authority/provenance decides canonical use |
| Event occurred, participant absent | shared Actual/Outcome + actor-specific participation state |
| Outcome corrected by authoritative provider | current accepted Outcome changes; prior assertion retained |
| AI predicts likely completion | provisional inference only; not canonical Outcome by itself |

---

# 19. Rejected alternatives

## One universal completion/status enum

Rejected because it conflates operational state, result, epistemic certainty, cancellation, schedule movement, and domain-specific conclusions.

## Put Outcome directly on Activity/Event

Rejected as the canonical model because it encourages intention objects to absorb reality/history and weakens multi-realization/correction semantics.

## Make every Observation an Outcome

Rejected because measurements and assertions can exist without a result/disposition.

## Make every Outcome a Milestone

Rejected because local result semantics do not automatically have strategic checkpoint identity.

## Treat produced artifact as Outcome

Rejected because outputs can exist independently and may themselves need lifecycle/history.

## Create one Outcome per participant by default

Rejected because shared result and actor-specific consequence/participation are different questions.

---

# 20. Deliberately deferred questions

- exact Outcome value-object/entity/relationship representation;
- exact result-family/type system;
- whether multiple simultaneous contextual Outcomes can be canonical for different scopes;
- final relationship between Outcome and conflicting assertions;
- exact Confirmation/authority/provenance state model;
- Outcome correction/version persistence;
- Outcome-to-Evidence relationship shape;
- replacement relationship model;
- specialist-module extensions;
- API/SQL representation.

These are downstream dependencies, not failures of Outcome v0.

---

# 21. Decision note

Outcome v0 is accepted as a bounded contextual result/disposition concept.

The accepted model deliberately rejects:

- one universal completion enum;
- mixing lifecycle state with result semantics;
- treating every measurement/artifact as Outcome;
- conflating Outcome with Milestone or Evidence;
- treating one actor/provider assertion as universal truth.

The concept remains reopenable if Observation, Confirmation, Provenance, Relationship, or persistence modeling demonstrates that a simpler structure preserves all required semantics without loss.

---

# 2026-08-13 — Version / material-equivalence downstream closure amendment

Version v0 closes Outcome's former `Outcome correction / version persistence` dependency without changing Outcome semantics.

Canonical separation:

```text
Outcome meaning/identity
= contextual result/disposition for the realization

Outcome material state
= the materially relevant result state currently represented

Version
= purpose/facet-scoped reference to that material state
```

A correction from `passed` to `failed`, or another materially different result, creates a new material state of the same Outcome context unless evidence shows the earlier record concerned a different result identity/context. Historical assertions, Confirmation, Evidence use and Decisions remain bound to the Outcome state they actually concerned.

A later material Outcome revision does not silently rewrite earlier evaluations. Conversely, metadata-only or irrelevant-facet changes need not invalidate every dependent semantic action. Material equivalence is therefore purpose/facet scoped, not global field equality.

Competing actor/provider Outcome assertions are not automatically Versions of one canonical Outcome. They may remain distinct attributed assertions until reconciliation establishes whether they concern the same result context and which state becomes current. Version preserves state history; Authority/Decision/reconciliation own current-state selection.

Provider revisions, hashes, ETags and storage versions may support lineage/concurrency but do not define semantic Outcome materiality. Retaining historical state references does not mandate indefinite retention of all sensitive supporting payloads.

The historical Outcome correction/version dependency is now downstream-closed at the semantic boundary. Detailed reconciliation/source precedence, result-family typing, retention and physical persistence remain independently owned.

No Outcome hardening failed. **Outcome remains PASS WITH HARDENING, REOPEN = 0.**

Normative downstream references:

- `version.md`;
- `../checkpoints/version-material-equivalence-v0-validation.md`.
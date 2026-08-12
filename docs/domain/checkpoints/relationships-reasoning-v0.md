# Relationships / Reasoning Cluster v0 — Opening Checkpoint

**Status:** OPEN — no concept verdicts  
**Opened:** 2026-08-12  
**Validation standard:** [Domain Validation Methodology v3](../validation-methodology-v3.md)  
**Execution template:** [Validation Execution Template v3](../validation-execution-template-v3.md)  
**Workstream:** Core Domain Model v0  
**Branch:** `feature/domain-model`

## 1. Scope

This checkpoint opens Cluster 5, **Relationships / Reasoning**.

It does not accept a new primitive, choose a final review order, validate a candidate, alter Clusters 1–4, or begin logical/physical persistence design.

Its sole purpose is to preserve the mandatory starting conditions for the cluster:

- Clusters 1–4 are the current validated baseline;
- candidate terms are evidence-driven hypotheses, not a checklist;
- the next review order must be selected from dependency leverage and risk;
- every selected candidate must execute the full Methodology v3 pipeline before any verdict;
- from this cluster onward, the Adjacent Dependency Sweep is mandatory before every concept verdict.

## 2. Inherited baseline

```text
Intention & Execution v0        PASS
Time v0                         PASS
Observed Reality & Evidence v0  PASS
Data / Subjects v0              PASS WITH HARDENING
Deferred Dependency Closure     PASS
Cross-Cluster Validation v4     PASS WITH HARDENING

structural reopenings           0
unclassified material debt      0
```

Normative inherited sources:

1. [Domain Atlas README](../README.md);
2. [Domain & Product Language Map](../language-map.md);
3. [Validation Methodology v3](../validation-methodology-v3.md);
4. [Deferred Dependency Closure — Clusters 1–4 v0](deferred-dependency-closure-clusters-1-4-v0.md);
5. [Cross-Cluster Validation v4](cross-cluster-validation-v4.md);
6. [Multi-Actor Readiness v1](../multi-actor-readiness-v1.md);
7. [Core Domain Model workstream handoff](../../workstreams/domain-model.md).

The authoritative dependency register remains the Deferred Dependency Closure checkpoint. This cluster must not create a parallel generic watchlist.

## 3. Non-negotiable inherited invariants

```text
planned != actual
Schedule != Session
Schedule != Capacity Reservation
Occurrence identity != current timestamp/provider identifier
reported/asserted reality != established Actual
Actual != Session / Outcome / Observation / Confirmation / Evidence / Provenance
Observation != Quantity / universal RegisterEntry
Evidence != source information
Provenance != truth / Authority / Version / Audit
Confirmation != Authority / Acknowledgement / Acceptance / Verification

Person != Account != Actor
Subject != generic related_to
Actor != generic action edge
Resource != provider identity
Resource != Requirement / Allocation / Reservation / actual use
Asset != ownership / possession / stewardship / Resource role
visibility != authority
ownership != visibility
AI inference/proposal != established identity / Actual / Confirmation / allocation / Authority / disclosure permission
```

Relationships / Reasoning may reopen an inherited boundary only when stronger evidence exposes a material contradiction. Convenience, competitor vocabulary, table design, or apparent completeness are not reopening grounds.

## 4. Candidate space — not accepted concepts

The following names indicate demonstrated unresolved semantic pressure. None is pre-approved as a primitive, entity, relationship root, table, API, or workflow:

```text
Relationship
Dependency
Responsibility / Assignment / Claim / Hand-off
Stewardship / coordination burden
Contribution
Participation
GoalCriterion / Goal relationships
Evidence ↔ Criterion / evaluation relationship
Resource Requirement / Allocation / substitution
Authority
Visibility
Acknowledgement
Acceptance / Agreement
Verification
Decision
Version
AI Proposal
Principal / delegation / on-behalf-of
focus/context relations
```

## 5. Review-order decision rule

Before a first candidate is opened, compare candidate boundaries against the dependency register using all of:

1. number and severity of inherited dependencies affected;
2. leverage over existing accepted concepts;
3. likelihood of forcing premature assumptions about another unresolved candidate;
4. identity, history, authority, privacy and multi-actor risk;
5. ability to test the candidate without selecting a final SQL/API representation;
6. ability to preserve simple personal-first UX.

The selected first candidate must be justified in its own checkpoint. A likely starting area is not a decision:

```text
typed/directional/qualified relation semantics
Responsibility / Participation
Authority / Visibility
```

## 6. Mandatory candidate-validation protocol

For every candidate:

```text
Evidence + candidate formation
→ Core Semantic Validation Gate (CORE-01–CORE-13)
→ Multi-Actor Compatibility Gate (MA-01–MA-20, with explicit N/A rationale)
→ Cross-Concept Consistency Gate (XCON-01–XCON-06)
→ Adjacent Dependency Sweep
→ concept verdict
```

Applicable tests must be recorded in the candidate checkpoint. No candidate may receive a verdict with a material dependency left unnamed or unclassified.

Allowed concept verdicts:

```text
PASS
PASS WITH HARDENING
REOPEN
DEFERRED DEPENDENCY
```

Allowed dependency closure classes:

```text
RESOLVED
SAFE DEFERRED
REOPEN
```

A SAFE DEFERRED item must record why acceptance remains safe, its owner, exact reopening trigger, and tests to rerun.

## 7. Mandatory Cluster-5 pressure

The cluster must eventually test, where applicable:

- typed/directional relations versus semantic-free `related_to`;
- simple relation versus qualified relation with independent history/state/authority;
- Responsibility versus performer, Resource eligibility, participation and stewardship;
- open/claimable responsibility;
- hand-off request versus acceptance versus effective responsibility transfer;
- participation response versus Actual participation;
- Authority versus Visibility;
- canonical-change Authority versus asserted reality, Confirmation and Provenance;
- Account/Principal/delegation/on-behalf-of;
- shared fact versus actor-scoped overlay;
- selective disclosure and inference privacy;
- Evidence/Criterion/Decision semantics;
- Provenance versus Version/Decision/Audit;
- Milestone-attainment evaluation;
- Resource Requirement/Allocation/Reservation/history;
- Subject focus/context relations;
- AI proposal/action/authority boundaries;
- historical attribution after Account or relationship changes;
- deletion/revocation/retention implications.

This list is pressure coverage, not a required list of surviving primitives.

## 8. No-verdict state

No candidate has been validated in this checkpoint.

```text
concept verdicts issued          0
new primitives accepted          0
new primitives rejected          0
reopenings issued                0
new dependency closures issued   0
```

The next authorized work item is the read-only selection and formal opening of one candidate checkpoint under the protocol above.

## 9. Documentation propagation

No propagation is due at cluster opening.

- [x] Cluster opening recorded
- [x] Candidate space marked non-pre-approved
- [x] Inherited invariants recorded
- [x] Methodology v3 protocol recorded
- [x] No concept verdict implied
- [x] No Cluster 1–4 document modified
- [x] No logical/physical model started

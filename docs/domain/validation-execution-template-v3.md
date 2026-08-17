# Domain Validation Execution Template v3

**Status:** Mandatory checkpoint template for new Domain Atlas validation  
**Methodology:** `validation-methodology-v3.md`

Use this template for concept and cluster checkpoints. Remove sections only when explicitly `N/A` with rationale.

---

# 1. Scope

- Concept / cluster:
- Candidate version:
- Date:
- Reviewer/workstream:
- Adjacent concepts:
- Why this review exists:

# 2. Evidence reviewed

## Internal

- [ ] accepted Domain Atlas concepts
- [ ] relevant product docs
- [ ] feature-discovery scenarios
- [ ] multi-actor simulation/research where applicable
- [ ] architecture/ADR constraints
- [ ] prototype/product assumptions where relevant

## External

List targeted benchmark/research sources and classify each important finding:

| Source/pattern | Finding | Classification (BORROW/ADAPT/ALREADY STRONGER/ANTI-PATTERN/N/A) |
|---|---|---|

# 3. Candidate definition

> Canonical candidate definition here.

## Domain question answered

## Identity

## Independent/contextual existence

## Nearest boundaries

## Deliberate deferrals

---

# 4. Core Semantic Validation Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| CORE-01 Workflow inversion | | | | |
| CORE-02 Deep chronology | | | | |
| CORE-03 Reductio | | | | |
| CORE-04 Redundancy | | | | |
| CORE-05 Traceability | | | | |
| CORE-06 Orphan/independence | | | | |
| CORE-07 External benchmark | | | | |
| CORE-08 Anti-pattern review | | | | |
| CORE-09 Correction/reconciliation/epistemic integrity | | | | |
| CORE-10 Scale/performance/history | | | | |
| CORE-11 Simple vs power user | | | | |
| CORE-12 Product value/complexity cost | | | | |
| CORE-13 Implementation pressure | | | | |

## Core-gate failures/hardenings

---

# 5. Multi-Actor Compatibility Gate

| Test ID | Applicable? | Evidence/scenario | Result | Finding / hardening / deferral |
|---|---|---|---|---|
| MA-01 Identity/account independence | | | | |
| MA-02 Shared fact/actor overlay | | | | |
| MA-03 Responsibility/assignment/claim | | | | |
| MA-04 Stewardship/mental load | | | | |
| MA-05 Common ground/state separation | | | | |
| MA-06 Authority/canonical change | | | | |
| MA-07 Selective disclosure | | | | |
| MA-08 Inference privacy | | | | |
| MA-09 Partial adoption/external participant | | | | |
| MA-10 Assisted participation/provenance | | | | |
| MA-11 Relationship lifecycle/revocation | | | | |
| MA-12 Conflict/adversarial relationship | | | | |
| MA-13 Unequal power | | | | |
| MA-14 Multi-resource/capacity | | | | |
| MA-15 Coordination-burden distribution | | | | |
| MA-16 Formality/progressive disclosure | | | | |
| MA-17 AI authority/multi-party context | | | | |
| MA-18 Specialist-system boundary | | | | |
| MA-19 Multi-actor primitive redundancy | | | | |
| MA-20 Actor-scoped reality attribution | | | | |

## Multi-actor failures/hardenings

---

# 6. Cross-Concept Consistency Gate

| Test ID | Applicable? | Result | Notes |
|---|---|---|---|
| XCON-01 Identity compatibility | | | |
| XCON-02 Ownership/authority compatibility | | | |
| XCON-03 Planned/current/actual/history compatibility | | | |
| XCON-04 Relationship compatibility | | | |
| XCON-05 Multi-actor readiness compatibility | | | |
| XCON-06 Language-map compatibility | | | |

---

# 7. Adjacent Dependency Sweep

Mandatory before concept acceptance once the methodology transition rule applies. During the Data / Subjects transition cluster, record dependencies now and execute the full closure pass across clusters 1–4 after the cluster gate.

For every material neighboring question classify the closure treatment exactly as `RESOLVED`, `SAFE DEFERRED`, or `REOPEN`.

| Dependency / boundary | Why it matters | Closure class | Current resolution / why safe to defer | Owner / future concept or stage | Exact reopening trigger | Tests to rerun |
|---|---|---|---|---|---|---|

Rules:

- `RESOLVED` must point to the invariant/hardening that closes the issue now.
- `SAFE DEFERRED` must explain why current acceptance remains valid and identify an executable future trigger.
- `REOPEN` blocks acceptance until the affected concept/boundary is redesigned and retested.
- `TBD`, `review later`, or an unnamed future dependency is not a valid closure class.

---

# 8. Adversarial scenario log

Record the hardest scenarios, especially failures or near-failures.

| Scenario | What was stressed | Result | Model change required? |
|---|---|---|---|

---

# 9. Reopening / dependency register

| Finding | Severity | Closure class | Current treatment | Owner / future stage | Reopening trigger |
|---|---|---|---|---|---|

Severity: CRITICAL / STRUCTURAL / HARDENING / DEFERRED DEPENDENCY / PRODUCT-UX.  
Closure class for material dependency findings: RESOLVED / SAFE DEFERRED / REOPEN.

---

# 10. Concept verdict

Choose exactly one:

- [ ] PASS
- [ ] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

## Rationale

## Hardenings incorporated before acceptance

## Dependency-sweep summary

- RESOLVED:
- SAFE DEFERRED:
- REOPEN:

## Mandatory future re-tests

---

# 11. Cluster-only integration section

Use when this checkpoint validates a complete cluster.

| Test ID | Applicable? | Evidence/scenario | Result | Finding |
|---|---|---|---|---|
| CL-01 Representative reconstruction | | | | |
| CL-02 Deep integrated chronology | | | | |
| CL-03 Cross-concept redundancy | | | | |
| CL-04 Top-down traceability | | | | |
| CL-05 Bottom-up reconstruction | | | | |
| CL-06 Lateral propagation | | | | |
| CL-07 History/correction integrity | | | | |
| CL-08 Scale/product complexity | | | | |

## Cluster Multi-Actor Stress

Record at minimum applicable cases for shared state, reassignment/hand-off, external participant, privacy, conflicting evidence, revocation, unequal authority, shared resource, AI and actor-scoped Actual attribution.

| Scenario | Concepts exercised | Result | Finding |
|---|---|---|---|

## Cluster dependency closure summary

| Dependency | Closure class | Owner/trigger | Effect on cluster verdict |
|---|---|---|---|

## Cluster verdict

- [ ] PASS
- [ ] PASS WITH HARDENING
- [ ] REOPEN
- [ ] DEFERRED DEPENDENCY

---

# 12. Regression corpus additions

Add only scenarios that expose a new identity, history, authority, privacy, reconciliation, scale or UX boundary.

| Scenario | New boundary covered | Reuse trigger |
|---|---|---|

---

# 13. Documentation propagation

Before closing:

- [ ] concept document updated
- [ ] language map updated if terminology changed
- [ ] cluster checkpoint updated if applicable
- [ ] workstream handoff updated
- [ ] Adjacent Dependency Sweep completed or explicitly scheduled by the Data / Subjects transition rule
- [ ] every material deferral has owner + reopening trigger
- [ ] no unclassified dependency limbo remains at the applicable closure point
- [ ] no old conflicting canonical wording left unqualified

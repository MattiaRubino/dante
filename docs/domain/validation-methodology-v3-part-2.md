<!-- LIFEOS-CANONICAL-CONTINUATION document="validation-methodology-v3.md" follows="validation-methodology-v3.md" -->
> **Canonical continuation of the single logical Domain Validation Methodology v3 document.** This physical continuation amends execution/closure discipline only; it does not create a new methodology version.

# 2026-08-16 — Product-need admission and deferral-closure hardening

## Why this amendment exists

Validation Methodology v3 already required:

- `V3-GP-01 — LifeOS semantics first`;
- `V3-GP-03 — Representation alone is insufficient`;
- `EV-01..04` including product evidence, real workflows, external benchmark and candidate minimality;
- `CORE-01` real-world workflow inversion;
- `CORE-07` external cross-domain benchmark;
- `CORE-11` simple-user/power-user pressure;
- `CORE-12` product value / complexity cost;
- `CORE-13` implementation pressure without premature schema.

The methodological defect exposed during Relationships / Reasoning was **not missing product-value tests**. It was an overly permissive use of `SAFE DEFERRED`: semantically possible future questions could remain in the candidate pool even when no current LifeOS need had been demonstrated.

This amendment makes the already-existing LifeOS/product tests an explicit **candidate-admission and termination gate**.

---

# V3-GP-10 — Demonstrated LifeOS need before semantic carry-forward

A semantic question must not remain an active kernel candidate merely because:

```text
it exists in reality
another application models it
an external standard defines it
it could be useful someday
it is theoretically distinguishable
```

Before a candidate/dependency may survive into future semantic work, the review must establish a concrete current LifeOS reason through the existing evidence/product gates.

Mandatory question:

> **What current LifeOS capability, ordinary workflow, information-preservation requirement, structural invariant, or accepted North-Star behavior becomes false, lossy, materially harder, or impossible if this semantic is not represented in the current kernel?**

If no satisfactory answer exists, the item does **not** become `SAFE DEFERRED` merely because it is plausible.

External prevalence is supporting evidence only:

```text
competitors have it
!= LifeOS needs it

competitors do not have it
!= LifeOS does not need it
```

LifeOS may accept a semantic absent from competitors when the North Star / real workflows require it, and may reject a common industry semantic when it adds no current LifeOS value.

---

# Candidate admission / termination classification

After `EV-01..04`, `CORE-01`, `CORE-03/04`, `CORE-07`, `CORE-11`, `CORE-12` and applicable MA/XCON evidence, every discovered semantic candidate/dependency must first receive one **need disposition**:

## REQUIRED BY CURRENT LIFEOS

There is demonstrated current LifeOS product/kernel need and the accepted model cannot truthfully/completely cover it.

Treatment:

```text
→ active semantic work
→ resolve before applicable cluster closure
```

## ALREADY COVERED / COMPOSABLE

Accepted semantics already represent the required reality naturally and without material information loss.

Treatment:

```text
→ RESOLVED
→ no new concept/family
```

## REDUNDANT / OVERMODELED

The candidate adds labels, provider structure, convenience, or theoretical granularity without distinct necessary LifeOS semantics.

Treatment:

```text
→ REJECTED / RESOLVED
→ remove from active candidate pool
```

## NOT REQUIRED BY CURRENT LIFEOS KERNEL

The semantic may exist in reality or specialist systems, but no current ordinary LifeOS workflow/North-Star requirement needs it in the general kernel.

Treatment:

```text
→ RESOLVED OUT OF CURRENT KERNEL
→ no active semantic debt
→ may be reconsidered only from materially new product evidence
```

Examples may include specialist legal, forensic, institutional or provider-specific semantics when LifeOS currently only coordinates around them rather than owning them.

## REQUIRED BUT OWNED BY A LATER STAGE

The need is demonstrated, but the unresolved question belongs deliberately to a later project stage such as logical persistence, physical schema, API/runtime enforcement or another explicitly sequenced implementation layer.

Treatment:

```text
→ STAGE-DEFERRED
→ owner + exact stage trigger + tests required
→ not a semantic-kernel candidate treadmill item
```

This is the normal treatment for questions like exact SQL/API representation after semantic boundaries are already closed.

---

# SAFE DEFERRED — narrowed meaning

`SAFE DEFERRED` is no longer a valid label for “possibly useful later”.

A semantic dependency may be `SAFE DEFERRED` at **concept-level only** when all of the following are true:

1. a real current LifeOS need is demonstrated;
2. the current concept can still be accepted without guessing the unresolved neighboring semantics;
3. a specific owning semantic review is already part of the current cluster/explicitly sequenced domain work;
4. the exact reopen trigger is executable;
5. the relevant tests are named;
6. deferral does not turn the item into an indefinite candidate backlog.

If condition 1 fails, classify the item as `NOT REQUIRED BY CURRENT LIFEOS KERNEL`, `REDUNDANT/OVERMODELED`, or `ALREADY COVERED` instead.

If condition 2 fails, classification is `REOPEN`.

If the unresolved question is implementation-stage rather than semantic, classify it `STAGE-DEFERRED`, not `SAFE DEFERRED`.

---

# Cluster-final closure rule

A semantic cluster may not receive final `PASS` / `CLOSED` while it retains unresolved **semantic** `SAFE DEFERRED` items inside the scope of that cluster.

Before final cluster closure, every historical/current semantic deferral must be re-evaluated under the need-disposition gate and converted to one of:

```text
REQUIRED BY CURRENT LIFEOS
→ resolve now before closure

ALREADY COVERED / COMPOSABLE
→ RESOLVED

REDUNDANT / OVERMODELED
→ REJECTED / RESOLVED

NOT REQUIRED BY CURRENT LIFEOS KERNEL
→ RESOLVED OUT OF CURRENT KERNEL

REQUIRED BUT OWNED BY LATER NON-SEMANTIC STAGE
→ STAGE-DEFERRED
```

Final semantic-cluster closure requires:

```text
SEMANTIC SAFE DEFERRED = 0
SEMANTIC UNCLASSIFIED  = 0
SEMANTIC UNRESOLVED    = 0
STRUCTURAL REOPEN      = 0
```

`STAGE-DEFERRED` items may remain because they are not unresolved semantic decisions; they are explicit downstream implementation obligations whose semantic boundaries are already closed.

Historical checkpoint wording is preserved for audit. A later closure checkpoint must record the final disposition instead of deleting or rewriting earlier `SAFE DEFERRED` history.

---

# Candidate-space / re-score discipline

A fresh candidate-space re-score remains mandatory after accepted semantic milestones **only while the cluster still contains demonstrated REQUIRED current-LifeOS semantic gaps**.

Do not score every historical deferral as an active candidate.

Candidate pool admission requires:

```text
current LifeOS need demonstrated
AND
not already covered/composable
AND
not rejected/overmodeled
AND
not out-of-current-kernel
AND
not merely stage-deferred
```

When a cluster approaches closure, switch from candidate ranking to an **exhaustive final closure audit** of all remaining/historical deferrals. The purpose is to reach final disposition, not to generate another endless ranking.

If that audit identifies a real REQUIRED blocker, resolve that blocker and rerun the closure audit. Otherwise close the cluster.

---

# Product / benchmark interpretation hardening

For every material candidate, the checkpoint must state explicitly:

```text
LIFEOS USE
- which current LifeOS workflow/capability uses this semantic?
- what becomes wrong/lossy without it?

EXTERNAL EVIDENCE
- which comparable/specialist products model the problem?
- why do they model it that way?
- how do products without it solve the same workflow?
- what is BORROW / ADAPT / ALREADY STRONGER / ANTI-PATTERN / NOT APPLICABLE?

MINIMALITY
- is a new kernel semantic required?
- can accepted concepts compose naturally instead?
- is this specialist/product/UI vocabulary rather than kernel truth?
```

The benchmark is not a popularity vote. The LifeOS-use section is mandatory even when external evidence is strong.

---

# Relationship to existing v3 rules

This amendment **narrows and clarifies** the following earlier wording without deleting history:

```text
V3-GP-09
No unclassified dependency limbo
```

still applies, but “classified” now includes a final need disposition; `SAFE DEFERRED` is not the default escape hatch.

Earlier `CORE-04` output `DEFERRED` must be refined before acceptance into the need disposition and then the applicable closure treatment.

Earlier section 12 wording that a cluster PASS could retain `SAFE DEFERRED` semantic dependencies is superseded for final semantic-cluster closure by this amendment.

Earlier section 16.7 “Deferrals are executable obligations” remains valid only for genuinely required semantic/stage obligations after the need gate; it does not authorize speculative backlog.

---

# Mandatory result vocabulary from this amendment onward

For semantic candidate/dependency disposition use:

```text
REQUIRED NOW
ALREADY COVERED / COMPOSABLE
REJECTED / OVERMODELED
NOT REQUIRED BY CURRENT LIFEOS KERNEL
STAGE-DEFERRED
REOPEN
```

`SAFE DEFERRED` may appear only as a temporary concept-level dependency treatment satisfying the narrowed criteria above; it must be eliminated/resolved before final semantic cluster closure.

---

# Immediate applicability

This amendment applies immediately to the active Relationships / Reasoning v0 workstream.

The next action is **not another fresh candidate promotion**. It is an exhaustive final Cluster 5 closure audit that:

1. inventories every accepted concept and historical/current deferred item;
2. reruns the existing v3 LifeOS-use/product/benchmark/minimality/adversarial gates where needed;
3. assigns a final disposition to every semantic item;
4. identifies only genuinely REQUIRED current-LifeOS blockers;
5. reaches zero semantic deferred/unresolved/unclassified before cluster closure.

Canonical operational companion: `validation-execution-template-v3-part-2.md`.

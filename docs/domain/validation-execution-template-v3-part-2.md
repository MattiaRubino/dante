<!-- LIFEOS-CANONICAL-CONTINUATION document="validation-execution-template-v3.md" follows="validation-execution-template-v3.md" -->
> **Canonical continuation of the single logical Domain Validation Execution Template v3.** This physical continuation amends the mandatory execution template to enforce the product-need/deferral-closure hardening in `validation-methodology-v3-part-2.md`.

# 2026-08-16 — Mandatory product-need admission / closure additions

Use the original template plus the following mandatory additions. These sections supersede any older interpretation that treated `SAFE DEFERRED` as a generic future-work bucket.

---

# A. Candidate admission / LifeOS-use gate

Complete **before** a discovered semantic candidate/dependency may enter or remain in the active candidate pool.

## A1 — Current LifeOS use

- Concrete current LifeOS workflow/capability:
- North-Star/product evidence:
- What becomes false, lossy, materially harder or impossible without this semantic?
- Is this ordinary LifeOS behavior or a specialist/domain-extension concern?

## A2 — Existing-model coverage

- Can accepted concepts already represent the workflow naturally?
- If composable, what exact composition covers it?
- Would a new concept only improve labeling/query convenience rather than semantic truth?

## A3 — External benchmark

| Product/standard/system | How it handles the problem | Why | LifeOS classification |
|---|---|---|---|

Allowed classification:

```text
BORROW
ADAPT
ALREADY STRONGER
ANTI-PATTERN
NOT APPLICABLE
```

Explicitly answer:

```text
Do products without this concept solve the same workflow acceptably?
Does LifeOS need it for a reason independent of competitor prevalence?
```

## A4 — Need disposition

Choose exactly one:

- [ ] REQUIRED BY CURRENT LIFEOS
- [ ] ALREADY COVERED / COMPOSABLE
- [ ] REDUNDANT / OVERMODELED
- [ ] NOT REQUIRED BY CURRENT LIFEOS KERNEL
- [ ] REQUIRED BUT OWNED BY A LATER STAGE
- [ ] REOPEN

Rationale:

A candidate may enter the active semantic queue only when `REQUIRED BY CURRENT LIFEOS` is selected and the question is not already covered.

---

# B. Adjacent Dependency Sweep — amended classification

The original ADS table remains useful, but **perform Need Disposition first**.

For each material dependency use:

| Dependency / boundary | LifeOS need disposition | Why | Semantic closure treatment | Owner/stage | Exact trigger | Tests |
|---|---|---|---|---|---|---|

Need disposition must be one of:

```text
REQUIRED BY CURRENT LIFEOS
ALREADY COVERED / COMPOSABLE
REDUNDANT / OVERMODELED
NOT REQUIRED BY CURRENT LIFEOS KERNEL
REQUIRED BUT OWNED BY A LATER STAGE
REOPEN
```

Semantic closure treatment:

```text
RESOLVED
SAFE DEFERRED   # concept-level only; narrowed criteria apply
STAGE-DEFERRED
REOPEN
```

Rules:

- `ALREADY COVERED / COMPOSABLE` → `RESOLVED`.
- `REDUNDANT / OVERMODELED` → `RESOLVED — REJECTED`.
- `NOT REQUIRED BY CURRENT LIFEOS KERNEL` → `RESOLVED — OUT OF CURRENT KERNEL`.
- `REQUIRED BUT OWNED BY A LATER STAGE` → `STAGE-DEFERRED` with exact stage trigger/tests.
- `REQUIRED BY CURRENT LIFEOS` must be resolved now unless the narrowed concept-level `SAFE DEFERRED` criteria are all satisfied.
- `REOPEN` blocks acceptance.
- “could be useful later”, competitor prevalence, standard availability or theoretical distinguishability are not valid reasons for `SAFE DEFERRED`.

---

# C. Concept verdict additions

Before concept acceptance record:

```text
CURRENT LIFEOS NEED DEMONSTRATED   YES / NO / N/A-with-reason
ALREADY COVERED                   YES / NO
NEW SEMANTIC REQUIRED             YES / NO
OUT-OF-KERNEL ITEMS               <count/list>
STAGE-DEFERRED ITEMS              <count/list>
TEMPORARY SAFE DEFERRED           <count/list>
REOPEN                            <count/list>
```

A concept-level `SAFE DEFERRED` item must include the six criteria from `validation-methodology-v3-part-2.md` and cannot be promoted automatically after the concept closes.

---

# D. Cluster-final exhaustive closure audit

Use this section before any final semantic cluster `PASS/CLOSED`.

## D1 — Full inventory

Inventory all:

- historical candidate rankings;
- historical/current `SAFE DEFERRED` items;
- unresolved specialist boundaries;
- items discovered by accepted concepts;
- product/North-Star pressures;
- relevant external benchmark patterns;
- candidate families never yet formally selected.

Do not limit the audit to the latest ranking.

## D2 — Final disposition table

| Historical/current item | Current LifeOS need | Existing coverage | Final disposition | Evidence/tests | Remaining action |
|---|---|---|---|---|---|

Allowed final disposition:

```text
REQUIRED NOW
ALREADY COVERED / COMPOSABLE
REJECTED / OVERMODELED
NOT REQUIRED BY CURRENT LIFEOS KERNEL
STAGE-DEFERRED
REOPEN
```

`SAFE DEFERRED` is **not** a final semantic-cluster disposition.

## D3 — Blocker rule

If any row is `REQUIRED NOW` and not already resolved:

```text
CLUSTER CANNOT CLOSE
→ resolve exactly that real blocker
→ rerun impacted v3 tests
→ rerun final closure audit
```

Do not create a new broad candidate treadmill.

## D4 — Final semantic closure counts

Required before `PASS/CLOSED`:

```text
REQUIRED NOW unresolved = 0
SEMANTIC SAFE DEFERRED  = 0
SEMANTIC UNCLASSIFIED   = 0
SEMANTIC UNRESOLVED     = 0
STRUCTURAL REOPEN       = 0
```

Record separately:

```text
STAGE-DEFERRED = <count>
```

Stage-deferred items do not block semantic cluster closure only when their semantic boundary is already resolved and the later-stage owner/trigger/tests are explicit.

---

# E. Documentation propagation additions

Before closing a concept/cluster:

- [ ] LifeOS-use/product-need evidence recorded;
- [ ] external benchmark used as evidence, not authority;
- [ ] every discovered candidate has a need disposition;
- [ ] speculative “maybe later” items are not left as `SAFE DEFERRED`;
- [ ] historical `SAFE DEFERRED` items have final disposition at cluster closure;
- [ ] stage-deferred items are separated from semantic debt;
- [ ] final semantic cluster closure counts are zero as required;
- [ ] candidate ranking is not continued when final closure audit finds no REQUIRED blocker.

Canonical methodology: `validation-methodology-v3.md` + `validation-methodology-v3-part-2.md` as one logical document.

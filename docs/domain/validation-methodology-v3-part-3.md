<!-- LIFEOS-CANONICAL-CONTINUATION document="validation-methodology-v3.md" follows="validation-methodology-v3-part-2.md" -->
> **Canonical continuation of Domain Validation Methodology v3.** Earlier methodology remains preserved; this continuation adds mandatory whole-domain closure controls discovered during the final LifeOS regression.

# 2026-08-16 — Whole-Domain closure hardening

## Why this amendment exists

The original WD-01..07 gate is necessary but not sufficient for final semantic closure. A model can be internally coherent and still miss a real LifeOS capability because the test corpus was shaped by the concepts already present.

Final closure therefore requires three additional controls:

```text
WD-08 Whole-Domain Inverse Reconstruction / Necessity
WD-09 Simulation / Coverage / Missing-Concept Discovery
WD-10 External Product / Competitor Benchmark
```

These tests are mandatory for final Whole-Domain closure and for any later major semantic rebaseline.

---

# WD-08 — Whole-Domain Inverse Reconstruction / Necessity

Purpose:

> Test the complete model from the represented reality backward, rather than only from concepts forward.

For every accepted native referent, value semantics, capability, relation family or contextual profile, ask:

1. If this semantic owner is removed, can the same real-world state still be represented truthfully without abusing another concept?
2. Does removal collapse two realities that must remain distinguishable?
3. Does removal lose stable identity, actor scope, history, correction, provenance, planned/current/actual separation or material state?
4. Does preserving the information after removal require a semantic-free generic relation/property or synthetic workflow object?
5. Can a final/current record be traced backward to the materially relevant intention, source, actor, version and historical state where consequence requires it?
6. Does the concept survive because of real semantic independence rather than UI convenience, cardinality, query frequency or implementation shape?

Also run the inverse merge test:

> Can two different accepted concepts be merged without making at least one representative chronology or cross-cluster scenario false or ambiguous?

Pass condition:

```text
accepted owner removable without material loss   0
false merge accepted                             0
unclassified inverse pressure                    0
```

A failure reopens only the affected owner/boundary, not the entire model automatically.

---

# WD-09 — Simulation / Coverage / Missing-Concept Discovery

Purpose:

> Determine whether LifeOS can naturally represent the realities it is intended to support, including realities not used to design the current vocabulary.

WD-09 must include four layers:

### A. Historical simulation replay

Re-run the original feature-discovery and multi-actor scenarios that materially influenced the Domain Model.

### B. Current product replay

Re-run current accepted North Star / V1 workflows. Historical product documents do not override later product decisions.

### C. Adversarial cross-cluster simulation

Generate new scenarios designed specifically to combine boundaries and discover omissions, for example:

- expectation changes followed by different Actual;
- provider state conflicting with LifeOS current understanding;
- private cause producing a shareable consequence;
- actor/account transitions;
- correction after a consequential Decision;
- multi-currency or material-version history;
- group/collective states with dissent;
- external/accountless participants;
- simple and specialist-domain pressure in the same workflow.

### D. Missing-concept discovery

Do not only ask whether the known model can encode the known test set.

Ask:

> What ordinary or strategically important LifeOS reality would the product reasonably need to understand but is absent from the simulation corpus?

For every discovered capability X:

```text
LifeOS should support X?
  NO  → NOT REQUIRED / specialist / product-only as applicable
  YES → current model represents X naturally?
          YES → ALREADY COVERED / COMPOSABLE
          NO  → POTENTIAL GAP
                → Evidence + product-need gate
                → full V3 review only if it survives
```

A simulation failure is not by itself permission to create a primitive.

Pass condition:

```text
current required reality not naturally representable 0
unclassified simulation pressure                    0
```

---

# WD-10 — External Product / Competitor Benchmark

Purpose:

> Use mature products and adjacent specialist systems to expose real problem pressure, missing capabilities and known anti-patterns without allowing competitor schemas to dictate LifeOS ontology.

Mandatory evidence circles:

1. direct/broad personal planning, productivity, knowledge and coordination products;
2. adjacent specialist products relevant to important LifeOS domains, such as calendar/scheduling, health, travel, finance, family, CRM/contact, document/content, inventory/asset and automation systems.

For each external capability/pattern:

```text
external product has X
        ↓
does current LifeOS actually need the underlying capability?
        ↓
NO  → classified out of current kernel
YES → current model handles it naturally?
        ↓
YES → covered/composable
NO  → create product-independent LifeOS simulation
        ↓
     potential gap only if the simulation + product-need gate survive
```

Mandatory anti-pattern mining includes checking whether LifeOS accidentally reproduces patterns such as:

```text
task = calendar event
time placement = occurrence identity
person = account
creator = owner
sharing = authority
sharing = universal visibility
latest write wins universally
document = blob
place = free-text string only
money = ordinary unit quantity
all relationships = generic edge
all user-specific truth = untyped JSON/property
provider object = canonical LifeOS identity
```

Canonical rules:

```text
competitor presence != primitive justification
competitor absence != rejection evidence
standard/provider schema != ontology authority
market prevalence != semantic truth
```

Use current primary/official documentation where material and practical. Record product/version/date sensitivity where the benchmark may change.

Pass condition:

```text
externally exposed required LifeOS gap 0
unclassified external pressure         0
```

---

# Final Whole-Domain closure target

Final semantic closure now requires:

```text
WD-01..10
PASS / PASS WITH HARDENING

REQUIRED NOW unresolved  0
SEMANTIC SAFE DEFERRED   0
SEMANTIC UNCLASSIFIED    0
SEMANTIC UNRESOLVED      0
STRUCTURAL REOPEN        0
```

A separate later-stage readiness finding may still block logical/physical implementation without reopening semantics. Such findings must be explicitly classified and owned rather than hidden inside semantic debt.

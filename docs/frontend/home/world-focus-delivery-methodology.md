# DANTE — World Focus Delivery Methodology v0

**Status:** CURRENT WORKSTREAM METHOD  
**Date:** 2026-09-01  
**Branch:** `feature/home-react`  
**Applies to:** World Focus B0 foundation and every subsequent internal mini-vertical until the pre-backend freeze and later full-vertical handoff.

---

# 1. Purpose

World Focus must be built as a sequence of small, production-depth verticals rather than one broad implementation pass.

The method exists to prevent two opposite failures:

1. **premature architecture** — selecting libraries, abstractions, schemas or UI patterns before the real block proves they are needed;
2. **local optimization** — implementing a visually successful block that later forces rewrites because Domain, database, Intelligence, multi-actor, performance, accessibility or future evolution were ignored.

The governing principle is:

> **Freeze durable invariants early. Re-evaluate concrete implementation choices at the moment the evidence exists.**

Future compatibility does not mean implementing every hypothetical future feature now. It means preserving explicit ownership and extension boundaries so future capabilities can be added without reopening the core architecture.

---

# 2. Workstream shape

```text
WORLD FOCUS PLATFORM CONTRACT
        ↓
B0 — FOUNDATION
        ↓
internal mini-verticals
        ↓
contrasting complete Worlds
        ↓
production hardening
        ↓
pre-backend freeze
        ↓
full vertical / backend handoff
```

Every block, including B0, is independently reviewed, implemented, tested and accepted before the next block changes its frozen behavior.

---

# 3. Mandatory block lifecycle

Every block follows this order.

```text
1. Authority re-read
2. Concrete requirements
3. Scenario/simulation pressure
4. Failure-mode analysis
5. Future/evolution analysis
6. Current external product research
7. Current technology research
8. Architecture alternatives
9. Explicit decision + rejected alternatives
10. UX / information / interaction architecture
11. Responsive architecture
12. Accessibility architecture
13. Security / privacy / disclosure architecture
14. Performance architecture
15. State / async / concurrency architecture
16. Testing / observability / rollout architecture
17. Code/package ownership map
18. Smallest complete production-depth implementation
19. Automated gates
20. Real-browser/manual review
21. Fix/polish
22. Explicit acceptance
23. Freeze/update contracts
24. Next block
```

Do not jump directly from a product idea to implementation.

---

# 4. Authority re-read rule

Before each block, re-read the **specific** accepted DANTE authorities that block can affect. Do not rely only on summaries or memory.

Depending on scope these may include:

- Product Identity / North Star;
- feature-discovery simulations;
- multi-actor/collaboration simulations;
- adaptive-intelligence direction;
- Domain Atlas / current Domain authority;
- Logical Model;
- Physical Model;
- current Database source of record / Alembic history where persistence consequences matter;
- frontend production-readiness contracts;
- Access/Auth/AppShell contracts where boundaries are touched;
- Home structural/geometry/frozen behavior contracts;
- World Focus Platform Contract;
- current Intelligence Platform architecture when AI/capabilities/effects are touched.

A frontend convenience is not allowed to redefine accepted Domain or database semantics.

---

# 5. Research rule

External research is required when the block depends on changing technology, browser capabilities, current product patterns, current library quality or emerging alternatives.

Research must distinguish:

```text
mature production pattern
promising but emerging technology
experimental technology
product-specific implementation that should not be copied
```

The goal is not to copy another product. It is to discover mature invariants, failure modes and implementation lessons.

Potential comparison sources include, only when relevant:

- Notion;
- Linear;
- Grafana;
- Home Assistant;
- Apple platform interaction/widget patterns;
- Microsoft Copilot surfaces;
- Anthropic/other AI artifact patterns;
- browser/platform specifications;
- official React/TanStack/TypeScript/tooling documentation;
- W3C/WCAG;
- OWASP;
- web.dev/browser-performance guidance.

Research findings must be converted into DANTE-specific decisions or explicit non-adoptions.

---

# 6. Technology-selection rule

Do not choose a technology because it is:

- newer;
- popular;
- labeled enterprise;
- fashionable in the React ecosystem;
- used by a large company;
- theoretically more abstract/extensible.

Choose it only if it materially improves DANTE on evidence such as:

```text
correctness
maintainability
runtime performance
bundle cost
accessibility
security
observability/testability
future evolution
team/repository consistency
browser support
migration/replacement cost
```

Prefer native platform/framework capabilities when they solve the problem cleanly.

Every added dependency must have a concrete owner and a concrete problem it solves.

Do not add infrastructure “for later” when a narrow extension boundary is sufficient.

---

# 7. Architecture review format

Every non-trivial architectural choice should record:

```text
Problem
Constraints
Required invariants
Options considered
Current evidence
Decision
Why this decision
Rejected alternatives
Risks
Future trigger for re-evaluation
Tests/guards protecting the decision
```

A rejected option can become valid later if the documented trigger occurs.

This prevents historical decisions from turning into unexplained dogma.

---

# 8. Future-proofing rule

Every block must consider at least:

- future real backend/API;
- canonical Domain evolution;
- cross-device persistence where relevant;
- offline/sync where relevant;
- multi-actor/disclosure where relevant;
- provider failure/staleness;
- long-running/durable Intelligence work where relevant;
- saved configuration migration;
- feature rollout/disable/kill-switch behavior;
- new unknown Worlds;
- new module/specialist families;
- localization/timezone/unit pressure;
- larger real datasets than fixtures;
- mobile/narrow layouts even if current product scope is web-first;
- accessibility and assistive technology;
- browser/platform evolution.

Future-proofing must preserve boundaries, not pre-build speculative systems.

---

# 9. Mini-vertical definition

A mini-vertical is not merely a component.

A block is complete only when its relevant full depth is addressed, for example:

```text
product semantics
contracts/types
state ownership
async/races
UI behavior
responsive
accessibility
security/privacy
performance
errors/degraded states
tests
observability seams
future integration boundary
```

If a block is visual only while its lifecycle/data/error/a11y behavior remains undefined, it is not complete.

---

# 10. Production-depth rule

“Production quality” does not mean maximum abstraction.

It means the simplest architecture that truthfully handles the required operational reality.

Required qualities include where applicable:

- strict typing;
- runtime validation at untrusted boundaries;
- deterministic state/fixtures;
- stable identity;
- cancellation/race protection;
- error isolation;
- truthful loading/empty/partial/stale/error/unavailable states;
- accessibility by construction;
- bounded data/rendering;
- leak/resource cleanup;
- safe rich-content rendering;
- explicit persistence scope;
- explicit concurrency semantics for future durable writes;
- clear source of truth;
- testable contracts;
- no hidden fake-backend success.

---

# 11. Performance method

Performance decisions are evidence-based.

For each block determine:

```text
critical path
bundle/code cost
data/payload pressure
render/re-render ownership
layout/paint pressure
interaction latency
long-task risk
memory/resource lifetime
large-data behavior
```

Do not freeze arbitrary numeric product budgets before representative implementation/profile data exists.

Once measured and accepted, meaningful budgets become regression gates.

Performance work may not silently alter frozen product behavior.

---

# 12. Accessibility method

Accessibility is designed during the block, not added during final hardening.

Target remains WCAG 2.2 AA unless explicitly superseded.

Each interactive block reviews:

- keyboard behavior;
- focus ownership/restoration;
- semantic roles/names/states;
- reduced motion;
- zoom/text pressure;
- drag alternatives;
- pointer/touch targets;
- non-color communication;
- screen-reader/read-order semantics;
- chart/data alternatives when visual-only output is insufficient.

Automated checks complement, not replace, manual critical-path review.

---

# 13. Security/privacy/disclosure method

Each block asks:

```text
what data crosses the browser boundary?
what is untrusted?
what is sensitive?
what is merely hidden vs actually authorized?
can aggregates/explanations leak concealed facts?
what is logged/telemetried?
what may persist locally?
what requires authoritative revalidation?
```

No frontend affordance is treated as authorization.

No AI/provider content is treated as trusted executable UI.

---

# 14. Testing method

Tests protect observable semantics and architecture invariants, not incidental implementation.

Applicable layers:

```text
contract/static
unit
component
integration
browser/E2E
visual regression
accessibility
performance/resource cleanup
future backend contract tests
```

Failure/race injection is required where the block has async behavior.

No gate is reported green unless actually executed.

---

# 15. Freeze rule

A block can freeze only after:

```text
architecture review complete
implementation complete
relevant automated gates green
real-browser/manual product review complete
known regressions resolved
explicit user acceptance
contracts/docs updated
```

After freeze:

- refactors may change implementation but not accepted behavior;
- bug/performance fixes must preserve the contract;
- a deliberate behavior/architecture change requires explicit reopening before production writes;
- tests are not weakened merely to accommodate accidental drift.

---

# 16. Block B0 special role

B0 establishes the shared production foundation used by every later World Focus mini-vertical.

B0 must establish enough infrastructure that later blocks do not recreate:

```text
feature/package ownership
typed foundational contracts
state/source-of-truth rules
application/projection boundary
request generation/cancellation foundation
module host/registry extension seam
composition ownership seam
interaction-surface ownership seam
error isolation
runtime-validation strategy
localization/time/unit primitives
safe content/link policy
feature availability/evolution seam
observability seam
test fixture/harness foundations
accessibility/performance measurement foundations
```

B0 must **not** prematurely implement:

- final World Lens behavior;
- all module families;
- final adaptive ranking;
- final AI interaction UX;
- final customization UX;
- real backend endpoints;
- real LLM/provider calls;
- speculative DB tables;
- final visual skin/VFX.

B0 is successful when those later mini-verticals can be implemented independently without reopening foundational ownership.

---

# 17. Current planned block sequence

The sequence is a working decomposition and may be refined before each block if boundaries become clearer.

```text
B0  Platform Foundation
B1  World Context / Session / Lens
B2  Data & Projection
B3  Module Platform
B4  Stable Composition
B5  Adaptive
B6  Universal module mini-verticals
B7  Peek / Insight / Explore
B8  DANTE Intelligence integration
B9  Personalization / Insight promotion
B10 Specialist mini-verticals when justified
B11 Contrasting complete Worlds
B12 Final production hardening / pre-backend freeze
```

No later block is authorized to bypass the Platform Contract or this methodology because implementing the shortcut is locally easier.

---

# 18. Working mantra

```text
research the real problem
-> preserve accepted DANTE semantics
-> choose the narrowest correct owner
-> implement the smallest complete production-depth slice
-> prove it under pressure
-> freeze it
-> move forward
```

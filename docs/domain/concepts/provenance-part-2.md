<!-- LIFEOS-CANONICAL-CONTINUATION document="provenance.md" follows="provenance.md" -->
> **Canonical continuation of the single logical Provenance document.** This physical file extends the same logical document; it does not create a new Provenance concept or document identity.

# 2026-08-16 — Contribution versus Provenance

Contribution v0 resolves the boundary between lineage of records/material versions and actor-scoped materially meaningful contribution to a realized context.

```text
Provenance
= bounded lineage of a domain record / material version

Contribution
= materially meaningful actual input/work attributable to an Actor
  within a bounded realization/result/output context
```

Therefore:

```text
Provenance != Contribution
record creator != Contributor automatically
record editor != Contributor automatically
source lineage != Contribution automatically
Contribution != Provenance event
```

Provenance may provide Evidence supporting a Contribution assertion, but it does not choose or manufacture the semantic relation.

Examples:

```text
Anna edited the stored document
→ provenance fact

Anna materially supplied analysis used in the realized output
→ Contribution, if contextually established
```

The two may coincide but neither implies the other universally.

Contribution correction must preserve relevant provenance and consequential historical attribution rather than rewriting lineage to fit the latest interpretation.

## Result

```text
PROVENANCE v0
verdict unchanged
PASS WITH HARDENING
REOPEN 0

Provenance ↔ Contribution
RESOLVED
```

Normative downstream references:

- `contribution.md`;
- `../checkpoints/contribution-v0-validation.md`.

<!-- LIFEOS-CANONICAL-CONTINUATION document="reconciliation.md" follows="reconciliation.md" -->
> **Canonical continuation of `reconciliation.md`.** The accepted Reconciliation / Source Precedence v0 specification remains preserved. This amendment records Resource Requirement / Allocation integration only.

# 2026-08-15 — Resource Allocation conflict/correction boundary

Resource Requirement / Allocation v0 confirms that competing or stale planning states remain inputs to Reconciliation, not reasons for silent overwrite.

Representative cases:

```text
LifeOS current Allocation = none
external provider claim = still active
```

or:

```text
earlier recorded Allocation = Room A
later reliable evidence = Room B was actually selected
```

The model may preserve competing assertions/current interpretations and reconcile under a bounded basis.

Canonical rules:

```text
Allocation != Reconciliation
Reconciliation != current Allocation owner
provider state != universal truth
latest Allocation assertion != winner automatically
```

Reconciliation may correct, supersede, select, defer, escalate or leave the conflict unresolved according to applicable policy/Authority/Evidence/Provenance. The Resource Allocation family owns the resulting current planning state.

Correction must preserve material earlier assertion/provenance rather than pretending the corrected Allocation was always known.

No last-write-wins, newest-source-wins, provider-wins, user-wins or AI-confidence-wins rule is introduced.

Reconciliation / Source Precedence v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative downstream reference: `../checkpoints/resource-requirement-allocation-v0-validation.md`.
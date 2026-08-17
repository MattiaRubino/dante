<!-- LIFEOS-CANONICAL-CONTINUATION document="resource.md" follows="resource-part-3.md" -->
> **Canonical continuation of the single logical Resource document.** Earlier Resource semantics remain preserved; this physical continuation records Place integration only.

# 2026-08-16 — Place integration

Place v0 resolves the previously deferred native semantics behind room/place Resource use.

```text
Place
= native spatial referent

Resource
= contextual planning/execution role
```

Therefore:

```text
Place != Resource
Place may play Resource role
```

Examples:

```text
Place Room 3
capacity 20
→ Resource candidate for Workshop
```

```text
Place Studio
→ Resource candidate for Photo Session
```

The Place remains independently meaningful before/after any Resource Requirement, Allocation or Capacity Claim.

Resource eligibility may depend on Place properties/context such as capacity, accessibility, distance, policy or time-dependent Availability, but eligibility does not redefine Place identity.

Do not create synthetic Resource identity merely because a Place is bookable.

```text
venue != Resource automatically
Place allocation != Place identity
Place visibility != Resource-source visibility universally
```

Resource v0 remains **PASS WITH HARDENING, REOPEN = 0**.

Normative reference: `../checkpoints/place-v0-validation.md`.

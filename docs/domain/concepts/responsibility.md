<!-- LIFEOS-CANONICAL-SPLIT document="responsibility.md" part="1" total="3" -->
> **Canonical document split — Part 1 of 3.** Parts 1–3 together form one authoritative document; this is a physical split only, not a summary/reference hierarchy. The payload preserves the full pre-compaction baseline first and later downstream amendments in sequence; later explicit amendments override stale status/deferral wording without deleting the earlier rationale. Navigation: **Part 1** · [Part 2](responsibility-part-2.md) · [Part 3](responsibility-part-3.md)

<!-- LIFEOS-CANONICAL-PAYLOAD -->
# Responsibility v0

**Status:** Current accepted baseline  
**Accepted:** 2026-08-12  
**Meaning of accepted:** best current decision; reopenable with stronger evidence  
**Validation standard:** Domain Validation Methodology v3  
**Workstream:** Core Domain Model v0 — Relationships / Reasoning

## Canonical definition

> **Responsibility is the contextual semantic relation through which an eligible Actor bears the obligation/accountability to ensure that a bounded commitment is appropriately handled within a defined scope and context. Responsibility is independent of who requested the commitment, who is expected to perform it, who actually performs it, who coordinates it, who has Authority over it, and who may view it.**

Responsibility answers the bounded question:

> **Who is accountable for ensuring this commitment is appropriately handled in this context?**

It does not answer, by itself:

- who requested the commitment;
- who is operationally eligible to perform it;
- who is expected/planned to perform it;
- who actually performed it;
- who coordinates/reminds/monitors it;
- who may assign or transfer it;
- who has canonical-change Authority;
- who may view the commitment or relationship;
- whether a proposed transfer has been accepted;
- whether the underlying Activity/Event/commitment actually occurred.

Responsibility is therefore a **specific semantic relation family**, not a universal entity/root and not a synonym for `assignee`.

---

# 1. Why Responsibility exists

LifeOS already needs to preserve the identity of a commitment while the people around it change.

Representative case:

```text
Activity
Pick up prescription

requested_by
Maria

responsible
Anna

expected_performer
Luca

actual_performer
Marco
```

All of these may be true simultaneously.

Without distinct Responsibility semantics, the model tends toward weak alternatives:

1. one `assigned_to` field that mixes accountability and expected execution;
2. current Account/User implicitly treated as responsible;
3. actual performer overwriting planned/responsible actor;
4. transfer request treated as immediate transfer;
5. Resource eligibility treated as obligation;
6. ownership or Authority treated as automatic responsibility;
7. assignment treated as proof that coordination burden transferred;
8. `NULL assignee` used ambiguously for both unknown and intentionally open work.

The semantic need is real even though a universal Responsibility entity is not required for every simple case.

---

# 2. Responsibility is contextual, not native identity

Responsibility does not create a second identity for the responsible Actor or target.

```text
Person Anna
        ↓ responsible-for
Activity A17
```

Anna retains Person identity and Actor semantics.

The Activity retains Activity identity.

Ordinary reassignment or transfer changes the relationship, not the underlying Activity or Person identity.

Canonical rule:

> **Responsibility attaches accountability to an existing bounded commitment/context; it does not define the identity of the target or the holder.**

A simple case may be expressible as a direct specific relation. A richer case may require a qualified Responsibility context when the relationship itself has material state/history/scope.

---

# 3. Responsibility versus requester

Requester answers approximately:

> Who asked for this commitment/action?

Responsibility answers:

> Who must ensure it is appropriately handled?

These may coincide but are not equivalent.

```text
Manager requests report
Analyst responsible
```

```text
Parent requests pickup
Sibling responsible
```

Therefore:

```text
requester != responsible Actor
```

Requesting work does not automatically establish Responsibility unless the governing product/policy semantics explicitly do so.

---

# 4. Responsibility versus expected performer

Expected performer answers:

> Who is intended/planned to execute the work?

Responsibility answers:

> Who must ensure the commitment is appropriately handled?

Example:

```text
Manager responsible
Analyst expected performer
```

The responsible Actor may delegate execution while retaining accountability.

Therefore:

```text
Responsibility != expected performer
```

A simple personal task may collapse these roles in UI, but the kernel must not equate them universally.

---

# 5. Responsibility versus actual performer

Actual performer answers:

> Who actually executed the work?

Responsibility answers:

> Who bore accountability for ensuring it was handled?

Example:

```text
Responsible
Anna

Expected performer
Luca

Actual performer
Marco
```

Possible because Luca was unavailable and Marco substituted.

Therefore:

```text
Responsibility != actual performer
expected performer != actual performer
```

Actual execution must not rewrite historical Responsibility to make the eventual performer appear responsible all along.

---

# 6. Responsibility versus Actor

Actor is the contextual agency category/capability of the referent/system.

Responsibility is one specific semantic relationship that an eligible Actor may bear.

```text
Actor != Responsibility
```

The specific-role precedence rule remains:

```text
responsible_for
performed_by
recorded_by
confirmed_by
requested_by
```

are stronger than a generic `actor` edge when those meanings are known.

Responsibility does not turn Actor into an entity/root.

---

# 7. Responsibility versus Resource

Resource answers:

> What could satisfy this execution need?

Responsibility answers:

> Who is accountable for ensuring the commitment is handled?

A Person may be Resource-eligible without being responsible.

A responsible Actor may be unavailable or lack the capability to perform the work personally.

Therefore:

```text
Resource eligibility != obligation/accountability
Responsibility != Resource
```

This boundary prevents candidate selection and responsibility assignment from collapsing into one planner field.

---

# 8. Responsibility versus Authority

Responsibility does not grant the right to assign, override, disclose, approve, delete, or establish canonical state.

```text
responsible Actor
!= Authority holder
```

Likewise, an Authority holder may reassign a commitment without becoming responsible for it.

Example:

```text
Manager
has Authority to reassign

Employee
currently responsible
```

Canonical rule:

> **Responsibility never manufactures Authority by itself.**

Authority v0 now closes this boundary: effective assignment/claim/hand-off depends on whatever bounded Authority/policy/Acceptance basis applies, while Responsibility itself remains accountability semantics.

---

# 9. Responsibility versus Visibility

Being responsible does not automatically grant access to every related private fact, source, participant, Observation, Provenance record, or reason for unavailability.

Likewise, being able to view a commitment does not establish Responsibility.

```text
Responsibility != Visibility
```

Visibility v0 now closes this boundary. A product/policy may grant a responsibility holder some minimum bounded projection needed to act, but:

```text
Responsibility
!= Visibility
!= Authority to re-disclose
```

The relationship itself may also be more sensitive than either endpoint.

---

# 10. Responsibility versus ownership / possession / custody

Ownership, possession, custody and responsibility answer different questions.

Example:

```text
Asset laptop
owner = Company
holder = Mattia
maintenance responsibility = IT
repair coordinator = Anna
actual repair performer = Technician
```

No relation is inferred automatically from another.

Therefore:

```text
owner != responsible Actor
holder != responsible Actor
custodian != responsible Actor
```

---

# 11. Responsibility versus coordination Stewardship

Coordination Stewardship covers the distinct burden of anticipating, remembering, monitoring, reminding, coordinating, and repairing the process around a commitment.

Example:

```text
Child
responsible for taking recycling out

Parent
remembers deadline
monitors completion
reminds child
repairs failure
```

The parent may carry coordination burden without being the current Responsibility holder for execution.

Therefore:

```text
Responsibility != coordination Stewardship
Assignment != Stewardship transfer
```

The semantic distinction is accepted. A standalone Stewardship primitive is **not** accepted yet.

Stewardship remains SAFE DEFERRED until concrete LifeOS workflows prove that it must be explicitly assigned/transferred/queried as independent domain state rather than represented through actions, provenance, product state or another smaller model.

---

# 12. Explicitly open / unassigned versus unknown

This is a canonical epistemic distinction.

```text
UNKNOWN
!=
EXPLICITLY OPEN / UNASSIGNED
```

Examples:

```text
Activity
Take recycling out

responsibility intentionally open
someone eligible may claim
```

is not equivalent to:

```text
Activity imported from external system
responsible Actor unknown
```

Therefore a future logical representation must not use one ambiguous `NULL responsible_id` to mean both conditions without another semantic discriminator.

Canonical rule:

> **Absence of a known current holder is not evidence that the commitment is intentionally open, and intentional openness is not missing information.**

---

# 13. Assignment

`Assignment` is not accepted as a standalone universal kernel primitive.

Assignment is an operation/process through which an Actor is nominated or established for a **specific named role**.

Examples:

```text
assign Responsibility to Anna
```

```text
assign expected performer to Luca
```

```text
assign reviewer to Marco
```

The noun `Assignment` alone is semantically incomplete because it does not identify which role is being changed.

Canonical rule:

> **Every material assignment must identify the semantic role being assigned.**

Whether assignment immediately makes the role effective depends on the governing Authority, policy and acceptance semantics.

Therefore neither rule is universal:

```text
Assignment always requires Acceptance
```

nor:

```text
Assignment always makes Responsibility effective immediately
```

---

# 14. Claim

`Claim` is not accepted as a standalone universal kernel primitive.

A Claim is a self-initiated attempt/action by an Actor to acquire a specific role.

Example:

```text
open household chore
Luca: "I'll take it"
```

In a low-consequence household policy, Claim may also constitute acceptance and immediately establish Responsibility.

In a formal workflow, Claim may only nominate the Actor pending approval/acceptance.

Canonical rule:

> **Claim expresses self-initiated role acquisition intent/action; whether it establishes the role is policy-dependent.**

`Claim` must therefore name the role being claimed rather than becoming a generic relationship object.

---


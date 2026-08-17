<!-- LIFEOS-CANONICAL-CONTINUATION document="decision-and-assumption-register-v1.md" follows="decision-and-assumption-register-v1-part-5.md" -->
> **Canonical continuation of the Logical Model Decision and Assumption Register v1.** Earlier decisions/assumptions remain active unless explicitly superseded. This continuation records Slice E.

# Slice E — Decision Register

## DEC-E001 — Retain typed native provider identity; reject Resource identity root

**Decision:** Resource remains a contextual role over existing ReferenceAddress types.

**Accepted because:** Person, Asset and Place retain independent identity/lifecycle; a Resource wrapper would duplicate identity and reconciliation.

**Rejected alternatives:** universal Resource root; provider retyping into Resource.

**Reopen trigger:** a concrete workflow proves that Resource itself has independent identity/history not attributable to provider/requirement/allocation/claim semantics.

**Current status:** RETAIN.

## DEC-E002 — Resource Requirement is consequence-sensitive materialization

**Decision:** use LR-05 specification semantics by default; materialize LR-02 + ScopedRecordRef only when consequence/history/governance requires it.

**Rejected alternative:** mandatory Requirement entity/table for every simple resource use.

**Reopen trigger:** compact representation cannot preserve required history/reverse mapping in ordinary cases.

**Current status:** RETAIN.

## DEC-E003 — Candidate Set is derived by default

**Decision:** Candidate Set is LR-08 projection/read model.

**Rejected alternative:** candidate rows as canonical source truth.

**Reopen trigger:** a workflow requires durable candidate-set identity independent of the Requirement/evaluation that generated it.

**Current status:** RETAIN.

## DEC-E004 — Allocation remains separate from Claim and Actual use

**Decision:** Resource Allocation is LR-03 qualified association, escalating to material LR-02 where required.

**Rejected alternatives:** Allocation=Reservation; Allocation=Actual use; Allocation=Possession.

**Reopen trigger:** none from implementation convenience; requires contrary semantic evidence.

**Current status:** RETAIN.

## DEC-E005 — Effective Availability / Free Capacity are derived

**Decision:** baseline/rules/overrides/claims are source semantics; effective free intervals/capacity are LR-08 by default.

**Rejected alternative:** giant persisted canonical free-slot ledger.

**Reopen trigger:** only if a concrete owner establishes independently authoritative free-slot facts that cannot be reconstructed from source state.

**Current status:** RETAIN.

## DEC-E006 — Capacity is contextual and multidimensional-capable

**Decision:** no universal free/busy flag or single percentage. Use typed value dimensions + compatibility/policy + bounded material state.

**Rejected alternative:** universal Capacity scalar.

**Reopen trigger:** none absent stronger domain evidence.

**Current status:** RETAIN + HARDEN.

## DEC-E007 — Capacity Claim remains schedulable-capacity semantics

**Decision:** use qualified LR-03/LR-02 claim semantics for schedulable capacity; do not create universal Reservation root.

**Rejected alternative:** one semantic Reservation entity for calendar capacity, inventory stock, money and arbitrary resources.

**Reopen trigger:** specialist inventory/other domains independently prove a stable shared semantic owner above both families.

**Current status:** RETAIN.

## DEC-E008 — Quantity and MonetaryAmount remain distinct LR-04 families

**Decision:** physical scalar infrastructure may be shared; semantic families remain separate.

**Rejected alternative:** universal number+unit wrapper treating currency as ordinary unit conversion.

**Reopen trigger:** none from storage convenience.

**Current status:** RETAIN.

## DEC-E009 — Solver/AI is replaceable computation, not source truth

**Decision:** solver/AI produces candidate feasibility/ranking/proposals until domain-owned transitions become effective.

**Rejected alternative:** persist optimizer variables/solution as canonical Allocation state.

**Reopen trigger:** none unless product semantics explicitly promote a solver-owned fact through an accepted Authority/policy contract.

**Current status:** RETAIN.

## DEC-E010 — Specialist inventory/finance remain LR-13 boundaries

**Decision:** stock/movement/lot/serial and financial-account/transaction/ledger semantics remain specialist extensions rather than general Resource kernel.

**Rejected alternative:** ERP or financial ledger as LifeOS universal resource model.

**Reopen trigger:** cross-domain evidence establishes an actually shared semantic invariant, not merely shared storage mechanics.

**Current status:** RETAIN.

# Slice E — Assumption Register

## ASM-E001 — Native provider identity types remain sufficient for current general Resource use

**Evidence:** accepted Domain owners + Slice A ReferenceAddress + E falsification.

**Stability:** HIGH.

**If false:** Resource addressing strategy must be revisited; may require new bounded owner, not automatic universal root.

**Refresh trigger:** new provider family with independent persistent identity not covered by existing/specialist owner.

## ASM-E002 — Candidate universes can remain derived/cacheable

**Evidence:** solver/scheduler benchmarks and current product scenarios.

**Stability:** MEDIUM-HIGH.

**If false:** introduce material candidate snapshots only for workflows where historical candidate-set identity is consequential.

**Refresh trigger:** audit/explanation requirement depends on exact candidate universe at a past decision and cannot be reconstructed from captured inputs/state.

## ASM-E003 — Free capacity can be reconstructed from source rules/state for current scope

**Evidence:** Availability Domain model; free/busy benchmark patterns.

**Stability:** MEDIUM-HIGH.

**If false:** materialize authoritative availability facts under the correct owner without turning derived cache into source truth universally.

**Refresh trigger:** provider or product introduces authoritative availability commitments not reconstructible from local source state.

## ASM-E004 — Capacity dimensions remain bounded/context-specific

**Evidence:** human attention, rooms, cloud resources, count capacity and compatibility tests.

**Stability:** MEDIUM.

**If false:** add reviewed capacity-dimension vocabulary/definitions; do not default to a universal percentage.

**Refresh trigger:** repeated cross-domain need for shared capacity dimension definitions/versioning.

## ASM-E005 — Schedulable Capacity Claim and stock reservation do not yet justify one semantic owner

**Evidence:** Domain explicitly keeps inventory hold deferred; ERP benchmark shows distinct stock semantics.

**Stability:** MEDIUM.

**If false:** reevaluate shared claim abstraction during specialist inventory review.

**Refresh trigger:** inventory implementation proves identical lifecycle, identity, history, governance and reverse mapping across both claim families.

## ASM-E006 — Quantity/MonetaryAmount can share scalar physical machinery safely

**Evidence:** accepted semantic separation; mature datatype/payment systems.

**Stability:** HIGH for shared machinery, HIGH for semantic distinction.

**If false:** split physical implementation further; semantic distinction remains.

**Refresh trigger:** precision/currency/unit requirements expose unsafe shared physical assumptions.

## ASM-E007 — Solver engine will remain replaceable

**Evidence:** multiple viable optimization families (constraint programming, MIP, heuristics, AI/hybrid).

**Stability:** HIGH.

**If false:** implementation may optimize around a selected engine but canonical state must remain independently reconstructible.

**Refresh trigger:** solver-specific state becomes required for user-visible/history semantics rather than execution mechanics.

## ASM-E008 — Specialist inventory/finance can remain bounded without blocking general LifeOS

**Evidence:** current kernel scenarios; Domain specialist boundaries.

**Stability:** MEDIUM-HIGH.

**If false:** open a specialist logical slice/extension; do not overload general Resource semantics.

**Refresh trigger:** V1 product scope requires full stock/ledger operations as first-class functionality.

# Technology reconsideration record

Slice E explicitly reopened previously attractive mechanisms:

```text
ReferenceAddress                         RETAIN
MaterialStateRef                         RETAIN
Layered typed logical model              RETAIN + HARDEN
Universal Resource root                  REJECT
Universal Reservation root               REJECT
Universal Capacity ledger as whole model REJECT
Constraint solver as canonical model     REJECT
Owner-specific physical storage          RETAIN as physical ingredient
bounded capacity/claim engine             RETAIN as technical mechanism
ERP/inventory subsystem                  RETAIN as LR-13 specialist mechanism
```

No technology is retained merely because it was selected in an earlier slice.
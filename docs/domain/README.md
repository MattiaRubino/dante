# DANTE Domain Atlas

**Status:** CURRENT / AUTHORITATIVE ENTRY POINT  
**Domain verdict:** CLOSED for the current accepted DANTE/LifeOS kernel  
**Latest semantic closure:** 2026-08-17  
**Documentation lifecycle:** current truth here; detailed concept specifications remain in `concepts/`; validation chronology remains evidence in `checkpoints/`, `history/` and the historical continuation files.

## 1. Current truth

The Domain Model is semantically closed for the currently accepted kernel. The final Whole-Domain review found no required missing kernel owner and no structural reopen:

```text
NEW REQUIRED KERNEL GAP      0
REQUIRED NOW unresolved      0
SEMANTIC SAFE DEFERRED       0
SEMANTIC UNCLASSIFIED        0
SEMANTIC UNRESOLVED          0
STRUCTURAL REOPEN            0
```

The dedicated Domain closure was activated by the final remote-QA chain recorded in:

- [`checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](checkpoints/whole-domain-final-regression-v0-validation-part-7.md)

At Domain closure, WD-03 and WD-05 correctly remained downstream proof obligations. They were subsequently discharged by the completed Logical Model remote-QA closure:

- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md)

Therefore the current carried-forward state is:

```text
WD-01 PASS
WD-02 PASS
WD-03 PASS
WD-04 PASS
WD-05 PASS
WD-06 PASS
WD-07 PASS
WD-08 PASS
WD-09 PASS
WD-10 PASS

DOMAIN MODEL
CLOSED

LOGICAL MODEL
CLOSED
```

Later logical, physical and PostgreSQL work did not reopen the accepted Domain Model.

## 2. What is authoritative

Use the repository in this order when determining current Domain truth:

1. this README for current Domain status and navigation;
2. accepted concept specifications under [`concepts/`](concepts/);
3. [`validation-methodology-v3.md`](validation-methodology-v3.md) and [`validation-execution-template-v3.md`](validation-execution-template-v3.md) for the accepted validation method;
4. the final Whole-Domain closure record and other validation checkpoints for evidence of why the model was accepted;
5. downstream Logical Model closure evidence where it explicitly clears Domain carry-forward obligations such as WD-03 and WD-05.

Historical continuation files do not override newer current truth merely because they contain a later chronological note.

## 3. Core modeling rules that remain current

The accepted model follows these durable rules:

```text
accepted = current best justified decision, not immutable truth
specific truthful semantics > generic catch-all abstraction
native identity != contextual role
planned/intended state != Actual reality
Observation != Actual
Evidence != Provenance
Authority != Visibility
Responsibility != Participation
Ownership != Possession
provider identity != canonical DANTE identity
product/UI terminology != automatic ontology
```

The following generic shortcuts remain rejected as kernel truth:

```text
universal Entity / Thing root
universal Relationship / generic edge
universal Subject root
universal Actor root
universal Resource root
universal User root
universal ManagedObject root
untyped property-bag/EAV semantics as canonical truth
```

Specific qualified relation families are allowed when the relation itself has material lifecycle, history, authority, provenance, privacy, actor-scoped state or other domain invariants.

## 4. Accepted specialist boundary

Specialist semantics are not flattened into the general kernel merely to simplify storage or APIs.

In particular:

```text
rich financial Transaction / inventory Movement
!= Observation
```

They are not required as universal general-kernel roots under the current scope, but future specialist capability must preserve their own lifecycle and history when DANTE becomes responsible for those semantics.

## 5. Current concept specifications

Detailed accepted semantics live under [`concepts/`](concepts/). Those files are the durable concept-level reference and may themselves have physical continuation parts where older tool limits required them.

The Domain Model includes the accepted identity, intention/execution, time, observed-reality/evidence, governance/relationship, value/resource and history/reconciliation families validated through the Whole-Domain closure. Later repairs that survived the final need gates include **Living Referent** and **Possibility**.

Do not infer a new primitive from a product label alone. Terms such as `Life Area`, `Project`, `Program`, `Someday`, `Maybe`, `Preference`, `Value`, `Risk`, `Issue`, `Transaction` or `Movement` require the semantics of the actual use case before they can justify a kernel owner.

## 6. Validation and evidence

Primary closure evidence:

- [`checkpoints/whole-domain-final-regression-v0-validation-part-6.md`](checkpoints/whole-domain-final-regression-v0-validation-part-6.md) — fresh integrated WD-01..10 rerun;
- [`checkpoints/whole-domain-final-regression-v0-validation-part-7.md`](checkpoints/whole-domain-final-regression-v0-validation-part-7.md) — dedicated final closure/remote-QA activation record;
- [`checkpoints/whole-domain-audit-v0-part-8.md`](checkpoints/whole-domain-audit-v0-part-8.md) — final Whole-Domain audit propagation;
- [`language-map-part-22.md`](language-map-part-22.md) — final language/disposition propagation from the Domain closure;
- [`checkpoints/deferred-dependency-closure-clusters-1-4-v0-part-17.md`](checkpoints/deferred-dependency-closure-clusters-1-4-v0-part-17.md) — final dependency disposition propagation;
- [`multi-actor-readiness-v1-part-19.md`](multi-actor-readiness-v1-part-19.md) — final multi-actor propagation;
- [`../logical-model/checkpoints/whole-logical-v1-remote-qa.md`](../logical-model/checkpoints/whole-logical-v1-remote-qa.md) — downstream WD-03/WD-05 discharge and Logical Model closure.

These are evidence/closure records. They explain and prove the accepted result; they are not a chronological reading requirement for understanding the present.

## 7. Historical continuation classification

The files:

```text
README-part-2.md ... README-part-20.md
```

are now **HISTORICAL / EVIDENCE ONLY**. They preserve the evolution from earlier in-progress states through repairs and closure, but this README supersedes them as the current Domain Atlas status/index.

Likewise, chronological `*-part-N.md` files elsewhere in `docs/domain/` must be treated according to their owning logical document:

- concept/reference continuations may contain durable specification payload and remain part of that logical specification until explicitly compacted losslessly;
- checkpoint/validation continuations are evidence/history unless a newer current document explicitly names them as a current contract;
- chronology alone never makes a continuation a higher authority than a later consolidated current source.

No continuation should be deleted merely because it is old; deletion/compaction requires the documentation knowledge-coverage gate.

## 8. Reopening rule

Domain closure is not a claim that the model can never change.

Reopen only when new accepted product scope, real scenarios, specialist ownership, implementation pressure, privacy/safety requirements or stronger evidence expose a material contradiction or a genuinely missing semantic owner.

A reopen must be explicit, bounded and regression-tested. Convenience, table shape, provider terminology, UI naming or generic abstraction preference are not sufficient reasons.

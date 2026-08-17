<!-- LIFEOS-CANONICAL-CONTINUATION document="test-corpus-v1.md" follows="test-corpus-v1-part-5.md" -->
> **Canonical continuation of the single Logical Model Test Corpus v1 document.** Earlier corpus families remain preserved. This continuation adds Slice E scenarios only.

# Slice E corpus — Resources / Values / Capacity

## E-IDENTITY-01 — Native provider keeps native identity

A Sony A7 IV used for a photo shoot remains the same Asset before, during and after Resource-role use.

Expected:

```text
Asset identity retained
no Resource wrapper identity
```

## E-IDENTITY-02 — Person as Resource does not become Resource identity

A Person is selected as interpreter.

Expected:

```text
Person identity retained
Resource role contextual only
Allocation does not imply Agreement / Consent / Participation / Responsibility
```

## E-REQ-01 — Requirement without candidate

A photo shoot requires a weather-sealed full-frame camera; no current candidate satisfies it.

Expected:

```text
Requirement remains valid
Candidate Set empty
no fake Allocation
```

## E-REQ-02 — Candidate set changes without Requirement revision

One rental provider becomes unavailable while the Requirement is unchanged.

Expected:

```text
Candidate projection changes
Requirement material state unchanged
```

## E-ALLOC-01 — Allocation without Claim

Camera A17 is planned for tomorrow, but no schedulable capacity reservation exists.

Expected:

```text
Allocation exists
Capacity Claim absent
```

## E-ALLOC-02 — Claim before concrete Allocation

A pool of three equivalent rooms has one slot held; a specific room is bound later.

Expected:

```text
pool capacity claim representable
concrete Allocation may be later
```

## E-ALLOC-03 — Actual use differs from plan

Camera A17 was allocated; Rental B was actually used after A17 failed.

Expected:

```text
historical Allocation A17 retained
Actual use Rental B retained
no rewrite
```

## E-ALLOC-04 — Actual use without prior Allocation

A user spontaneously uses a taxi without any prior planned Resource Allocation.

Expected:

```text
Actual use representable
no retrospective Allocation fabricated
```

## E-POSSESSION-01 — Allocation and Possession diverge

Camera allocated to Sara for tomorrow is physically held by Luca today.

Expected:

```text
Allocation -> Sara/context
Possession -> Luca/current holding
no contradiction
```

## E-AVAIL-01 — Derived free capacity

Baseline Mon-Fri 09:00-18:00; Tuesday 09:00-13:00 unavailable; Tuesday 15:00-16:00 claim.

Expected effective projection:

```text
13:00-15:00 free compatible capacity
16:00-18:00 free compatible capacity
```

Expected canonical sources:

```text
baseline rule
material override
claim
```

No canonical slot grid required.

## E-AVAIL-02 — Provider free/busy is evidence

External provider says busy 10:00-11:00.

Expected:

```text
provider assertion/provenance retained
LifeOS interpretation governed separately
provider busy != automatic universal LifeOS claim
```

## E-CAP-01 — Scheduled all-day item is non-blocking

Birthday scheduled all day.

Expected:

```text
Schedule present
no automatic 24h capacity consumption
```

## E-CAP-02 — Compatible overlap

Walk and English listening overlap.

Expected:

```text
both schedules/actuals representable
no universal conflict from overlap alone
```

## E-CAP-03 — Incompatible overlap

Driving overlaps deep coding.

Expected:

```text
truthful records remain representable
capacity conflict derived
```

## E-CAP-04 — Count capacity

Three equivalent rooms; two concurrent claims.

Expected:

```text
remaining capacity exists
binary free/busy insufficient
```

## E-CAP-05 — Human capacity is not one percentage

Illness reduces available windows and admissible workload categories without a trusted scalar percentage.

Expected:

```text
multidimensional/contextual capacity representable
no fabricated precision
```

## E-HISTORY-01 — Temporary limitation and historical explanation

T0 normal baseline. T1 fracture/illness reduces effective capacity. T2 planner creates lighter schedule. T3 condition resolves. T4 normal capacity returns.

Queries:

- what is applicable now?
- why was T2 plan lighter?

Expected:

```text
current applicability from current material state
historical T2 explanation from state/provenance applicable then
resolved limitation not treated as currently active
```

## E-PRIVACY-01 — Free/busy without private reason

A private medical condition reduces capacity.

Expected shared projection:

```text
unavailable / insufficient compatible capacity
```

Forbidden disclosure:

```text
medical source reason unless separately visible
```

## E-FUNGIBLE-01 — Bulk supply

Maintenance requires 500 ml oil.

Expected:

```text
Quantity/supply semantics
no 500 or 1 synthetic Asset identities merely for quantity
```

## E-FUNGIBLE-02 — Serialized asset

Specific camera body with serial number is tracked across repair, possession and use.

Expected:

```text
stable Asset NativeRef
not collapsed into generic stock quantity
```

## E-INVENTORY-01 — Stock reservation specialist boundary

On-hand quantity, reserved quantity and forecasted quantity differ.

Expected:

```text
specialist stock semantics remain distinct
stock hold != schedulable Capacity Claim automatically
```

## E-QTY-01 — Quantity normalization

Source says `5.00 km`; normalized computation uses `5000 m`.

Expected:

```text
source representation preserved where material
normalized value may support computation
no fabricated source rewrite
```

## E-QTY-02 — Same unit does not authorize arbitrary aggregation

Two values share the same unit but represent semantically different quantities.

Expected:

```text
unit compatibility alone insufficient for aggregation
owner/context decides
```

## E-MONEY-01 — FX basis required

Hotel quote 300 USD; planning estimate is derived in EUR.

Expected:

```text
source 300 USD retained
converted MonetaryAmount carries attributable basis when consequential
```

## E-MONEY-02 — Historical FX survives rate changes

Later FX rate differs.

Expected:

```text
historical estimate remains reconstructible
current rate does not rewrite old decision basis
```

## E-SOLVER-01 — Solver candidate is not canonical Allocation

Optimization ranks A17 first.

Expected:

```text
candidate/ranking projection only
no effective Allocation without applicable domain transition/Authority
```

## E-SCALE-01 — Large candidate universe

10,000 possible providers exist.

Expected:

```text
no requirement for 10,000 canonical candidate rows
query/derived/cache strategy allowed
```

## E-SCALE-02 — Long availability horizon

Years of recurring availability exist.

Expected:

```text
rules/overrides remain source
free-slot expansion may be bounded/materialized operationally
no infinite canonical slot ledger
```

## E-COUNTERFACTUAL MATRIX

Mandatory distinct pairs:

```text
owned / available
possessed / allocated
candidate / selected
allocated / capacity held
capacity held / actual use
Schedule / capacity consumption
free interval / enough compatible capacity
fungible quantity / individually tracked Asset
Quantity conversion / FX conversion
current Availability / historical Availability
solver candidate / authorized Allocation
```

## E-MUTATION MATRIX

Reject implementations that introduce:

```text
universal Resource root
Resource wrapper identity
canonical Candidate Set by default
Allocation == Claim
Allocation == Actual use
Schedule == Claim
stock reservation == Capacity Claim universally
free-slot grid as source truth
one universal Capacity percentage
Quantity == MonetaryAmount
FX == unit conversion
solver output == canonical state
provider reservation ID == LifeOS identity
```

All Slice E tests become part of the permanent whole-logical regression corpus.
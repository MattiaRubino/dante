# DANTE AI — Search / Intelligence Boundary Amendment — 2026-09

- **Status:** CURRENT / BINDING IMPLEMENTATION AMENDMENT
- **Branch:** `feature/ai-implementation`
- **Established:** 2026-09-04
- **Scope:** implementation sequencing and activation dependency only
- **Reopens Product/Domain/Logical/Physical/DB:** NO
- **Database/Alembic change:** NONE

This amendment corrects an implementation-sequencing ambiguity that survived into the final AI implementation baseline and current roadmap.

The accepted architectural invariant remains:

```text
GLOBAL SEARCH != INTELLIGENCE
```

Earlier implementation-facing text grouped:

```text
GLOBAL SEARCH subset
+ READ-ONLY ASK DANTE
```

under one `initial technical vertical` and then described I3/C3 Search readiness as a mandatory convergence prerequisite before I6 Ask. That grouping is **not binding after this amendment**. It over-couples two separate product/application capabilities and can be misread as making Global Search the data path or product surface for DANTE Intelligence.

Git history preserves the earlier wording as architecture chronology. This amendment supersedes that wording for current implementation and activation decisions.

---

## 1. Correct capability boundary

```text
GLOBAL SEARCH
= independent cross-cutting discovery/navigation capability
= deterministic/no-model capable
= owns Search contracts, eligibility, family registry and Search-specific projections
= may be consumed by Intelligence only through its public application surface
= is not Ask DANTE
= is not the Intelligence UI
= is not a mandatory LLM workload

INTELLIGENCE / ASK DANTE
= independent intelligence/orchestration capability
= may answer through deterministic owning-capability query seams
= may use Retrieval/Context + qualified ModelAccess when cognition is required
= may use Search discovery only when the selected information need actually requires Search
= does not own Search persistence/query implementation
```

Search remains forbidden from importing Intelligence. Intelligence remains forbidden from reaching Search private persistence adapters or owning generic cross-capability SQL.

---

## 2. Search is optional per Ask information need

A valid Ask path may be entirely independent of Global Search:

```text
HTTP Ask
→ WorkContract
→ ContextPlan / InformationNeed
→ SemanticQueryGateway
→ owning capability public typed query seam
→ deterministic/model-assisted reasoning as needed
→ Verification
→ Publication
→ AskResult
```

A different Ask may legitimately require discovery:

```text
HTTP Ask
→ InformationNeed
→ Search public surface
→ eligible Search family/families
→ validated ContextFragments
→ reasoning / verification / publication
```

Therefore:

```text
ASK MAY USE SEARCH
!=
ASK REQUIRES SEARCH GENERALLY
```

and:

```text
SEARCH READINESS
!=
GLOBAL PREREQUISITE FOR INTELLIGENCE READINESS
```

---

## 3. Correct execution lanes

Search lane:

```text
I1 Search contracts/eligibility/registry/shell       CLOSED / PASS
I3/C3 first real Search family + bounded PG adapter  DEFERRED / OWNER-SEAM TRIGGERED
Search HTTP / protected activation                    AUTH + FAMILY PROOF TRIGGERED
```

Intelligence/provider lane:

```text
I2 Intelligence pure contracts                       CLOSED / PASS
C6 control/safety/publication contracts              CLOSED / PASS
C7 route-config                                      CLOSED / PASS
C8 provider candidate admission                      CLOSED
C9 provider adapter/live compatibility               OPEN / PRE-LIVE READY
C10 direct DANTE qualification                       AFTER C9 LIVE
C11 qualification/promotion decision                 AFTER C10 + APPLICABLE EVIDENCE
I6 read-only Ask DANTE integration                    REAL INTELLIGENCE VERTICAL + ACTIVATION GATES
```

I3/C3 remains valid Search work. It is not cancelled, renumbered or folded into Intelligence.

---

## 4. I6 readiness after this amendment

I6 read-only Ask requires the **actual source/query path needed by the selected Intelligence vertical**, not Global Search by default.

Minimum applicable readiness:

```text
real product/application owner
real source data semantics
owning public typed query/read seam or explicitly accepted projection
safe display/result semantics
current/history semantics where material
Auth/AuthZ/Visibility/Consent/disclosure integration as applicable
source/provenance/basis/currentness behavior
verification + publication behavior
qualified model route when a model is actually used
applicable direct proofs
```

If the selected Ask vertical requires cross-capability discovery, Search becomes a real dependency for that vertical and the required I3/Search family must be integration-ready before activation.

If the selected Ask vertical can be served by an owning capability typed query seam, I3/Search does not become an artificial prerequisite.

---

## 5. First Intelligence vertical is product-selected, not Search-implied

After this amendment there is **no binding architectural choice that the first Intelligence product vertical must be `Global Search subset + read-only Ask DANTE`**.

The first real Intelligence vertical must instead be selected from an actual application capability with truthful owner/data/query semantics. It should be bounded enough to prove the Intelligence path without inventing fake application semantics.

The selection is an implementation/product decision and must identify at least:

```text
user-visible product capability
owning module/domain boundary
read/query operation(s)
real data/projection/display semantics
permission/currentness/provenance requirements
what is deterministic vs model-assisted
expected answer/publication contract
```

The first vertical may be read-only to keep consequence/effect scope bounded, but `read-only` is a safety/implementation envelope, not a requirement that the capability be Search.

---

## 6. C9/C10 relationship to a product vertical

C9 live compatibility remains independent of an application vertical because it validates provider protocol/material compatibility using synthetic/public/minimized data.

C10 direct DANTE qualification evaluates the material DANTE model-access composition against DANTE-owned workloads/eval families. It may begin from controlled DANTE evaluation fixtures after C9, but any claim of production suitability for a concrete user-facing Intelligence vertical must include that vertical's applicable workload/data/security/currentness evidence before promotion/activation.

Therefore:

```text
C9 LIVE
DOES NOT REQUIRE PRODUCT VERTICAL

C10 BASE MODEL/ROUTE EVAL
CAN BEGIN WITHOUT USER-VISIBLE VERTICAL

I6 REAL PRODUCT INTEGRATION / ACTIVATION
REQUIRES A REAL INTELLIGENCE VERTICAL
```

---

## 7. Superseded implementation wording

For current execution, this amendment supersedes any earlier statement whose effect is one of the following:

```text
"Global Search subset + read-only Ask DANTE" is one mandatory first AI vertical
I3/C3 Search must always converge before I6 Ask
Global Search is the default/required data path for Ask DANTE
Search readiness is a global prerequisite for provider/model qualification
```

It does **not** supersede:

```text
GLOBAL SEARCH != INTELLIGENCE
Search/Intelligence ownership boundaries
Search protected non-interference requirements
SemanticQueryGateway owning-seam requirements
ModelAccess/provider qualification gates
Auth/AuthZ/disclosure/currentness/publication requirements
Search as an optional Intelligence acquisition route
```

---

## 8. Current implementation consequence

No production code, database schema, migration, provider adapter or existing closed checkpoint is invalidated by this correction.

Current state remains:

```text
I0-I2            CLOSED / PASS
I3/C3 Search     DEFERRED / OWNER-SEAM TRIGGERED
C6-C8            CLOSED
C9               OPEN / PRE-LIVE READY
C9 P4 live       NOT RUN
```

The next provider checkpoint remains C9 P4 live compatibility. In parallel, the project may select a real Intelligence product vertical without requiring that vertical to be Global Search.

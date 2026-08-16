<!-- LIFEOS-CANONICAL-CONTINUATION document="multi-actor-readiness-v1.md" follows="multi-actor-readiness-v1-part-12.md" -->
> **Canonical continuation of the single logical Multi-Actor Readiness v1 document.** Earlier readiness analysis remains preserved; this continuation records Place / Location integration only.

# 2026-08-16 — Place / Location multi-actor integration

Place identity remains independent from actor/account context.

```text
Place != Account-owned object
Place != Person
Place != Authority / Visibility
```

One persistent Place may participate in shared and private contexts without duplication.

Examples:

```text
Shared Event venue -> Place Office
Private Person Home -> Place Home
Private travel origin -> Place Home
Shared Resource site -> Place Room 3
```

Visibility can differ for:

- Place identity/name;
- exact address/coordinates;
- Home/work association;
- Event venue relation;
- Asset located-at relation;
- route/travel-origin detail;
- supporting provider/reconciliation Evidence.

Seeing one endpoint or a derived free/busy/travel consequence does not grant visibility of all spatial source data.

Provider/AI reconciliation may propose Place identity but does not silently establish or disclose it.

```text
MA-01..20
PASS / PASS WITH HARDENING

MULTI-ACTOR GATE
PASS WITH HARDENING

PLACE semantic reopen
0
```

Normative reference: `checkpoints/place-v0-validation.md`.

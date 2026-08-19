# DANTE — Home B1 Context Rail v1

**Status:** ACCEPTED  
**Date:** 2026-08-19  
**Scope:** replace the old side Appunti/Review composition with a coherent contextual rail without altering the rest of Home.

## Decision

Use one integrated contextual rail with two complementary functions:

```text
Capture      user -> DANTE
Resolution   DANTE -> user
```

### Capture

Low-friction natural capture without forcing classification first. Current prototype includes composer, voice/attachment affordances, submit, recent trace and `Registro completo`.

### Resolution

Only matters that benefit from meaningful user input: confirmation, correction, small choice or escalation to deeper inspection.

Not a notifications center, recommendation feed, reminder list or metrics surface.

## Visual integration

- preserve the existing rail location next to the timeline;
- one outer surface rather than two independent cards;
- restrained hierarchy subordinate to timeline;
- rail stretches with the timeline column;
- no additional floating controls;
- timeline expansion retains the existing behavior of taking the rail's space.

## Iteration history

### Preview v1

Concept functionally present but too compressed/mixed and ended early, creating unused lower space.

### Preview v2

Rail extended vertically and sections gained clearer separation.

### Preview v3 — accepted

Removed the ambiguous focus/expand chevrons entirely. Both functions remain simultaneously visible and predictable.

## Rejected

`balanced -> capture focus -> resolution focus` hidden mode machine.

Reason: unclear, unnecessary and often expanded empty space instead of useful information.

## Exact accepted output

```text
size
760281 bytes

SHA-256
a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
```

The deterministic source representation is the A2 retained complete baseline plus:

`prototypes/frontend/home/work/overrides/b1-context-rail-v1.patch`

Patch SHA-256:

`c89772f1301b3419b6a0a0843a8d5105d77a05ac73fea3b863ef5460a6db60c8`

## QA qualification

Static checks:

- 114 DOM IDs;
- zero duplicate IDs;
- 38 style blocks;
- 20 inline scripts;
- zero inline JS syntax failures;
- embedded day-ribbon PNG identity unchanged.

No new browser automation run is claimed for this checkpoint.

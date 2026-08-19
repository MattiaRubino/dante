# DANTE — Home Current Pre-Frontend Checkpoint

**Branch:** `prototype/frontend`  
**Status:** **APPROVED WORKING VISUAL/BEHAVIOR CHECKPOINT**  
**Current accepted build:** **B1 Context Rail v1**  
**Nature:** standalone HTML/CSS/JavaScript coded UX prototype; not production application code.

## Retained complete baseline

A2 complete baseline is deliberately preserved:

```text
path
prototypes/frontend/home/current/home.html

size
748625 bytes

SHA-256
986e7d22b4cb536c8a89eacf116bee3350dd0b8aafeb497df2f837fc9c1bf5df

Git blob
fd9788212fbbd1ee40e53271cc39cedd9275b341
```

## Current accepted B1 output

The current accepted Home is reconstructed from the retained complete baseline plus the accepted B1 override through `prototypes/frontend/home/work/build.py`.

```text
size
760281 bytes

SHA-256
a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0

result
DETERMINISTIC BUILD MATCH
```

The user visually reviewed and accepted the v3 preview corresponding to this exact byte identity.

## B1 functional delta

Accepted:

- one integrated context rail beside timeline;
- Capture = user -> DANTE low-friction unclassified capture;
- Resolution = DANTE -> user unresolved matters requiring meaningful user input;
- real button/segmented controls rather than text pretending to be actions;
- both functions visible together;
- rail stretches down with the timeline column;
- existing timeline expansion still yields/removes the rail.

Rejected during iteration:

- initial visually compressed/mixed composition;
- rail stopping early and leaving large unused lower space;
- ambiguous focus/expand chevrons.

## Non-regression / intentionally unchanged

B1 does not redesign:

- timeline semantics;
- calendar/day ribbon;
- timeline toolbar;
- Worlds/Stats;
- overall Home navigation;
- brand/skin;
- production frontend stack;
- backend/domain/logical/physical semantics.

## Current static evidence

```text
accepted output size            760281
accepted output SHA-256         a781fca7a1ca0f967f41a1b9cad8165c636da900f4bc497974b9d1a849d7a4b0
DOM IDs                         114
duplicate DOM IDs               0
style blocks                    38
inline scripts                  20
inline JS syntax failures       0
embedded day-ribbon PNG size    281038 bytes
embedded day-ribbon PNG SHA-256 9a273c238835dfd66b65544004d75e2adba03971add634a35e86d7fe10f0cc4d
```

Browser smoke was not independently rerun in this documentation/write scope. Visual acceptance is based on the user-reviewed B1 v3 standalone preview.

## Current authorities

Read before Home work:

- `docs/workstreams/frontend.md`
- `docs/frontend/ui-registry.md`
- `docs/frontend/home/contract.md`
- `docs/frontend/terminology.md`
- `docs/frontend/localization.md`
- `docs/frontend/design-tokens.md`
- this checkpoint
- `docs/frontend/research-index.md` when semantic research is needed.

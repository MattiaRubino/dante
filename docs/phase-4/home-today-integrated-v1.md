# Phase 4 — Home + Today Integrated v1

Status: **APPROVED WORKING BASELINE**

Branch: `prototype/phase-4-today-home`

## Purpose

This checkpoint preserves the approved integrated Home/Today prototype selected on 2026-08-13 as the working base for the next Phase 4 iteration.

It does **not** replace the historical Home Shell v11 and Today v21 authorities. Those checkpoints remain preserved for regression/history. This document records the newer integrated working baseline chosen after visual review.

## Artifact provenance

The approved artifact is derived from the user-supplied `preview_9.html`.

The only change made before approval was the visual placement of timeline gap/margin labels:

- previous: labels on the **right** of the timeline;
- approved: labels on the **left**, close to the time axis;
- gap calculation and semantics are unchanged.

Local approved filename during review:

`preview_10_margin_labels_left.html`

SHA-256 of restored HTML:

`66f1f8af4795aa579394ec07bc872798141907c6c216f5af0daed4f96e5c32b4`

Size: `252952` bytes.

## Explicit product/design constraints

1. **Do not add Home wing expansion.**
   - No left AI wing expansion.
   - No right contextual wing expansion.
   - Previous experiments that added this behavior are rejected and are not part of this baseline.

2. Preserve the Home shell contained in this artifact unless a later iteration explicitly changes it.

3. Preserve the integrated Today behavior contained in this artifact unless a later iteration explicitly changes it.

4. Timeline gap/margin labels belong on the **left** side.

5. Do not silently replace this artifact with earlier temporary previews from the conversation.

## Important integrated Today behavior present in this baseline

The artifact includes the integrated timeline/calendar work already present in the supplied base, including:

- 24-hour timeline and density mapping;
- overlap lanes and group separation behavior;
- visual group filtering and reorder behavior;
- subtask expansion and card reflow;
- drag/move, cross-day movement, cancel/Undo behavior;
- zoom and time editing;
- navigation into past and future days;
- week strip synchronized with the viewed day;
- distinct `today` and `viewing` states in the week strip;
- expandable calendar navigation through day/month/year levels;
- contextual `Ora` return-to-now control;
- click on empty timeline space clears card focus;
- environmental day route and current-time semantics;
- Appunti/Review side rail and timeline panel expansion already present in the supplied base.

This list is a handoff summary, not permission to simplify the implementation. The restorable artifact is the exact visual/behavioral reference.

## Validation at checkpoint

Before saving:

- diff against supplied `preview_9.html` confirmed only the intended `.tl-margin-label` CSS placement change;
- JavaScript syntax validation: **8/8 script blocks valid**;
- visual browser verification confirmed the margin labels on the left.

## Restore

The exact HTML is stored as gzip + base64 chunks under:

`prototypes/home/archive/integrated-v1/`

Run:

```bash
python prototypes/home/archive/integrated-v1/restore_integrated_v1.py
```

The restore script verifies the SHA-256 above.

## Handoff

This is the current approved working artifact. Do not continue from discarded conversation previews unless the user explicitly asks to recover one.

Next implementation/design direction is intentionally **pending user instruction**.

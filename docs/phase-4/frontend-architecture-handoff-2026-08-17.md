# LifeOS — Frontend Architecture Handoff — 2026-08-17

**Status:** operational handoff / current frontend continuation checkpoint  
**Branch:** `prototype/phase-4-today-home`  
**Supersedes for continuation:** `docs/phase-4/frontend-architecture-handoff-2026-08-16.md`  
**Current approved working artifact:** `docs/phase-4/home-vnext-adesso-main-stage-v1.md`

---

## 1. Current saved state

The current saved Home/Today reference is **Home vNext Adesso + Main Stage v1**, built directly on the approved v8 timeline-toolbar artifact.

Exact restorable artifact:

`lifeos_home_v8_world_stats_switch_contextual_v23_safe_mid_divider.html`

Archive: `prototypes/home/archive/home-vnext-adesso-main-stage-v1/` (`v23_fragment.html.gz.b64` + `restore_v23.py`)

- size: `344559` bytes
- SHA-256: `a45d1f2b5fab677d738306154a93697e497ffb2c8b2e36ddbba4f4289b42cc77`
- approved v8 is preserved as an exact `307487`-byte prefix
- v8 SHA-256: `473de755ebb48940b30847c90a0cfd3a315d179a9ddd04138a0af13e3862013f`

Do not continue from rejected intermediate Adesso / divider / surface-switch experiments. Use this checkpoint.

---

## 2. Current Home upper composition

### AI expanded

- modern AI chat remains at left;
- current moment / next, `In evidenza`, and `Per te` form an open editorial composition rather than obvious widget cards;
- `Ora` is dominant;
- `In evidenza` is long/low;
- `Per te` is dynamic contextual content with subtle carousel behavior;
- visual separators use restrained LifeOS purple/cyan accents.

### AI collapsed

- AI becomes the narrow rail;
- `Ora/Prossimo` and `Per te` remain stacked in the contextual left area;
- one long right-side separator groups the stack;
- one horizontal separator distinguishes the two stacked sections;
- no heavy cards/panels should reappear;
- `In evidenza` remains a long band above the main stage.

---

## 3. Worlds / Stats selector

- in Worlds mode the switch is visually associated with the active central World;
- in Stats mode it moves above the stats group so it does not overlap the central stats card;
- selector placement must not be implemented by moving the entire stage or causing vertical inversion during AI collapse/expand;
- Worlds/Stats remains prototype vocabulary, not accepted ontology.

---

## 4. Semantic distinction to preserve

```text
ORA / PROSSIMO
= current moment and immediate continuation

IN EVIDENZA
= materially relevant attention item

PER TE / DYNAMIC
= useful contextual suggestion/opportunity/discovery

MAIN STAGE
= carried-forward significant realities / contextual projection

TIMELINE
= temporal reality
```

`In evidenza` and dynamic recommendations are deliberately distinct.

---

## 5. Timeline remains protected

All v8 timeline-toolbar rules remain binding:

```text
[ month/year ▾ ] [ Ora ] [ previous | 7-day week | next ] [ legend icon ] [ expand icon ]
[ reset ○ ] [ group chips ... ]
[ timeline ]
```

The underlying mature Today behavior continues to be governed by `docs/phase-4/today-v21.md` and `tests/prototypes/today-v21-regression.py`.

---

## 6. QA state

Static checkpoint gate passed:

- no duplicate IDs;
- CSS parse clean;
- all inline scripts syntax-clean;
- all v8 inherited scripts hash-identical;
- no post-v8 Today/timeline CSS selectors or JS references;
- final v23 vs v20 correction is background-only and cannot alter layout geometry.

Full automated Chromium regression could not complete in the current tool runtime because Chromium blocks local navigation and hangs on the complete accumulated prototype. Do not misreport this as a browser PASS. The exact limitation and static evidence are archived in `qa-static.json`.

---

## 7. Immediate continuation

The upper Home state is checkpointed. Next:

1. leave the current upper geometry alone unless a concrete defect is identified;
2. define the two secondary/disappearing areas beside Today currently represented by `Appunti` and `Review` placeholders;
3. decide their content/attention contract before designing deeper interactions;
4. then move to popovers/inline expansions/deeper pages/workspaces/navigation.

Keep the documented architecture direction: stable semantics, adaptive presentation, no infinite dashboard, no ontology-driven UI.

# Prototypes

Coded prototypes are stored here until the production application structure is created.

Prototypes should be interactive and reusable where practical, but may use simulated data and omit production backend integration.

## Current Phase 4 integration baselines

### Home Shell v11

- Accepted outer Home shell/design checkpoint: [`../docs/phase-4/home-shell-v11.md`](../docs/phase-4/home-shell-v11.md)
- Exact restorable archive: [`home/archive/v11/`](home/archive/v11/)
- Regression/hash check: [`../tests/prototypes/home-shell-v11-regression.py`](../tests/prototypes/home-shell-v11-regression.py)

Restore with:

```bash
python prototypes/home/archive/v11/restore_v11.py
```

This shell freezes the accepted topbar, compact conversational AI, Worlds/Stats stage, contextual right rail and vertical Home spacing before integration of the full Today v21 timeline.

### Today timeline v21

The authoritative timeline behavior remains documented by:

- [`../docs/phase-4/frontend-master.md`](../docs/phase-4/frontend-master.md)
- [`../docs/phase-4/today-v21.md`](../docs/phase-4/today-v21.md)
- [`today/archive/v21/`](today/archive/v21/)
- [`../tests/prototypes/today-v21-regression.py`](../tests/prototypes/today-v21-regression.py)

The next Phase 4 task is to integrate this v21 timeline behavior into Home Shell v11 without losing capability.

## Historical milestone

### Home/Today v7

- UX documentation: [`../docs/ux/today-home-v7.md`](../docs/ux/today-home-v7.md)
- Exact prototype archive: [`today/archive/`](today/archive/)
- Restore instructions: [`today/archive/README.md`](today/archive/README.md)

Restore the standalone interactive HTML with:

```bash
python prototypes/today/archive/restore_prototype.py
```

The v7 milestone validates timeline density, event overlap, three levels of expansion, stable grouped columns, conditional horizontal scrolling, and progressive multi-day navigation.

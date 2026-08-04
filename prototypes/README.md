# Prototypes

Coded prototypes are stored here until the production application structure is created.

Prototypes should be interactive and reusable where practical, but may use simulated data and omit production backend integration.

## Available prototypes

### Home/Today v7

- UX documentation: [`../docs/ux/today-home-v7.md`](../docs/ux/today-home-v7.md)
- Exact prototype archive: [`today/archive/`](today/archive/)
- Restore instructions: [`today/archive/README.md`](today/archive/README.md)

Restore the standalone interactive HTML with:

```bash
python prototypes/today/archive/restore_prototype.py
```

The v7 milestone validates timeline density, event overlap, three levels of expansion, stable grouped columns, conditional horizontal scrolling, and progressive multi-day navigation.

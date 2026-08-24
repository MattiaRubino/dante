# DANTE — Frontend Design Tokens

**Status:** v0 semantic token authority for new/touched prototype UI.

Canonical prototype token file:

`prototypes/frontend/shared/theme/tokens.css`

## Why

Colors, radii, spacing, shadows and typography must be adjustable without searching arbitrary historical CSS blocks.

## Rule

- new/touched UI uses semantic tokens;
- do not add raw repeated colors/radii/shadows/spacing when a semantic token exists;
- if no token exists, define one deliberately here and in `tokens.css`;
- do not mass-rewrite untouched legacy CSS merely for cleanliness; migrate legacy values as their surface is touched and verify non-regression;
- tokens describe **role**, not a current visual color name.

Prefer:

```css
background: var(--dante-surface-contextual);
color: var(--dante-text-primary);
border-radius: var(--dante-radius-panel);
```

over:

```css
background: rgba(7,14,27,.92);
border-radius: 21px;
```

## Current token families

### Color / surface

- canvas and elevated surfaces
- primary/secondary/muted text
- subtle/active borders
- primary accent and accent-soft states
- semantic warning/error/success only when meaning requires them

### Shape

- control, card and panel radii

### Spacing

A compact scale used instead of unrelated one-off margins/paddings.

### Elevation

Panel and popover shadows.

### Typography

UI size/weight/line-height roles. Product headings and body copy should use roles rather than per-element arbitrary values.

## Brand/skin boundary

The eventual brand/skin pass may change token values substantially. It should not require structural rewrites if surfaces obey the token contract.

## Legacy status

The existing Home contains many historical raw values. They are **legacy**, not canonical. The B1 rail introduces the semantic mapping in documentation; future materialization of that module must consume these tokens without changing its approved appearance.

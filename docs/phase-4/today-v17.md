# LifeOS Home/Today v17

## Scope

Today v17 stabilizes three areas without touching the separate zoom-control bug:

1. stronger local timeline dilation in crowded periods;
2. finer drag precision;
3. stable cards, filters, and grouped expansion.

## Vertical density

The day now uses a non-linear local time mapper. It considers:

- simultaneous events;
- starts concentrated within the same 60-minute window;
- short events;
- global day density.

Crowded bands receive more pixels per minute, while empty bands remain more compact. The geometry is calculated from unfiltered events, so filtering does not shrink or change the day.

For the current demo day, the canvas grows from about 1260 px in v16 to about 1375 px in v17.

## Drag precision

- standard zoom: 5-minute snap;
- zoom >= 175%: 1-minute snap.

Minute-level precision changes placement only; the ruler does not render one label per minute.

## Cards and collisions

- duration-aware minimum heights for 5, 10, and 20-minute items;
- dedicated tiny-card visual state;
- overlapping events use strict non-intersecting compact lanes;
- compact lane order still follows the global group order;
- metadata is hidden only when width or height is genuinely insufficient.

## Filters and expansion

Filters affect visibility only. They no longer modify:

- global group count;
- expanded timeline target width;
- column geometry;
- day density;
- time mapping.

A single filtered group therefore remains in its global column and never expands into an arbitrary full-width card.

## Regression checks

- 22 cards render without JavaScript errors;
- no rectangle intersections in the dense current day;
- canvas height remains 1375.22 px before and after a single-group filter;
- expansion reaches progress 1.000 after filtering;
- filtered expanded cards remain approximately 202 px wide;
- normal drag produces five-minute increments;
- 190% zoom permits minute-level placement;
- `today-v17-regression.py` passes.

## Deferred

The separately reported zoom-control defect is not addressed in v17 and must be handled in the next isolated iteration.

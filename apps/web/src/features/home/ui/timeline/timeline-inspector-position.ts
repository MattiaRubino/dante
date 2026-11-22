/** Viewport-only position for a date-lane Inspector.
 *
 * A date bar can occupy the entire timeline width. Its right edge is not a
 * useful anchor, so use the actual click coordinate instead. Keyboard
 * activation falls back to the title-side of the bar.
 *
 * Keep this separate from the ordinary timed-card Inspector placement:
 * changing this geometry must not move existing timed card dialogs.
 */
export type TimelineInspectorClickPoint = Readonly<{
  clientX: number;
  clientY: number;
}>;

type Rect = Readonly<{
  left: number;
  top: number;
  right: number;
  bottom: number;
}>;

type Size = Readonly<{ width: number; height: number }>;

const EDGE = 12;
const GAP = 12;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

export function positionDateLaneInspector(
  anchor: Rect,
  viewport: Size,
  panel: Size,
  click?: TimelineInspectorClickPoint,
): Readonly<{ left: number; top: number }> {
  const maxLeft = Math.max(EDGE, viewport.width - panel.width - EDGE);
  const maxTop = Math.max(EDGE, viewport.height - panel.height - EDGE);
  const x = clamp(
    click?.clientX ?? anchor.left + Math.min(72, (anchor.right - anchor.left) / 2),
    EDGE,
    Math.max(EDGE, viewport.width - EDGE),
  );
  const y = clamp(
    click?.clientY ?? (anchor.top + anchor.bottom) / 2,
    EDGE,
    Math.max(EDGE, viewport.height - EDGE),
  );

  // Prefer right, flip left near the viewport edge, otherwise center around
  // the click while keeping every pixel of the panel within the viewport.
  const right = x + GAP;
  const left = x - panel.width - GAP;
  const desiredLeft =
    right + panel.width <= viewport.width - EDGE
      ? right
      : left >= EDGE
        ? left
        : x - panel.width / 2;

  // Below or above the clicked bar when there is room. Long Inspectors
  // instead remain alongside the clicked point without falling off screen.
  const below = anchor.bottom + GAP;
  const above = anchor.top - panel.height - GAP;
  const desiredTop =
    below + panel.height <= viewport.height - EDGE
      ? below
      : above >= EDGE
        ? above
        : y - 36;

  return Object.freeze({
    left: clamp(desiredLeft, EDGE, maxLeft),
    top: clamp(desiredTop, EDGE, maxTop),
  });
}

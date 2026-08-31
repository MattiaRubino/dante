export const WORLD_FOCUS_GEOMETRY_VERSION = 'wf-g3-candidate' as const;

const guideEllipses = Object.freeze({
  outer: Object.freeze({ rx: '52.25%', ry: '90%' }),
  origin: Object.freeze({ rx: '50%', ry: '87%' }),
  inner: Object.freeze({ rx: '47.75%', ry: '84%' }),
});

const layout = Object.freeze({
  workspaceInlineInset: 'clamp(136px, 14vw, 224px)',
  compactWorkspaceInlineInset: 'clamp(76px, 18vw, 112px)',
  workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
  compactWorkspaceBlockInset: '20px',
});

/**
 * WF-G3 candidate geometry authority.
 *
 * The World frame is three true concentric ellipses centered on the World Focus
 * surface. The canonical origin ellipse uses rx=50%, so it is mathematically
 * tangent to the left and right route edges at mid-height instead of
 * disappearing outside the viewport. Its taller ry produces the long corner
 * arcs approved during visual QA instead of a rigid circular silhouette.
 *
 * Ellipse semantics:
 * - outer: slightly larger than the route width, so the band extends outside;
 * - origin: canonical reference, tangent to both lateral route edges;
 * - inner: slightly smaller, so the inside edge remains visible.
 *
 * This remains a candidate until visual QA approves it. Once approved, bump to
 * a locked version and do not alter these values as visual polish.
 */
export const WORLD_FOCUS_GEOMETRY = Object.freeze({
  version: WORLD_FOCUS_GEOMETRY_VERSION,
  guideEllipses,
  layout,
});

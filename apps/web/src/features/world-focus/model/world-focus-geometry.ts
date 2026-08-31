export const WORLD_FOCUS_GEOMETRY_VERSION = 'wf-g2-candidate' as const;

const guideRadii = Object.freeze({
  outer: '69.5%',
  origin: '67.5%',
  inner: '65.5%',
});

const layout = Object.freeze({
  workspaceInlineInset: 'clamp(136px, 14vw, 224px)',
  compactWorkspaceInlineInset: 'clamp(76px, 18vw, 112px)',
  workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
  compactWorkspaceBlockInset: '20px',
});

/**
 * WF-G2 candidate geometry authority.
 *
 * The World frame is not made from left/right bezier rails. It is three true,
 * concentric circles centered on the World Focus surface. Their radii are set
 * close to the viewport half-diagonal, so clipping by the rectangular surface
 * exposes only four corner arcs instead of vertical side bulges.
 *
 * Circle semantics:
 * - outer: outer boundary of the reserved visual-frame band;
 * - origin: canonical visual origin/reference for future transitions/assets;
 * - inner: inner boundary of the reserved visual-frame band.
 *
 * This remains a candidate until visual QA approves it. Once approved, bump to
 * a locked version and do not alter these values as visual polish.
 */
export const WORLD_FOCUS_GEOMETRY = Object.freeze({
  version: WORLD_FOCUS_GEOMETRY_VERSION,
  guideRadii,
  layout,
});

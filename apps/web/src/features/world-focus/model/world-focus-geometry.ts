export const WORLD_FOCUS_GEOMETRY_VERSION = 'wf-g3' as const;

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
  compactTuningMaxPx: 720,
});

/**
 * WF-G3 is the frozen World Focus geometry authority.
 *
 * The World frame is three true concentric ellipses centered on the World
 * Focus route surface. The canonical origin ellipse uses rx=50%, so at
 * route mid-height it is mathematically tangent to the left and right route
 * edges. The larger outer ellipse extends beyond those edges; the smaller
 * inner ellipse remains inside them. Their taller ry values produce the
 * approved elongated corner-arc silhouette instead of a rigid circle.
 *
 * Ellipse semantics:
 * - outer: external boundary of the reserved visual-frame band;
 * - origin: canonical reference for future transitions/assets;
 * - inner: internal boundary of the reserved visual-frame band.
 *
 * Change control:
 * - these values are structural geometry, not visual-polish knobs;
 * - child modules, World skins and overlays must not duplicate or redefine
 *   them;
 * - changing them requires explicit product approval and a deliberate geometry
 *   version bump plus contract/test/documentation updates.
 */
export const WORLD_FOCUS_GEOMETRY = Object.freeze({
  version: WORLD_FOCUS_GEOMETRY_VERSION,
  guideEllipses,
  layout,
});

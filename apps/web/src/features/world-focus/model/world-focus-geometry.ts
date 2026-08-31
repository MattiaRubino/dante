export const WORLD_FOCUS_GEOMETRY_VERSION = 'wf-g1' as const;

const guidePaths = Object.freeze({
  outer: 'M8 -100 C154 180 154 820 8 1100',
  origin: 'M42 -100 C184 180 184 820 42 1100',
  inner: 'M76 -100 C214 180 214 820 76 1100',
});

const layout = Object.freeze({
  guideViewBox: '0 0 220 1000',
  railWidth: 'clamp(104px, 12vw, 192px)',
  compactRailWidth: 'clamp(56px, 16vw, 88px)',
  workspaceGap: 'clamp(16px, 2vw, 32px)',
  compactWorkspaceGap: '12px',
  workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
  compactWorkspaceBlockInset: '20px',
});

/**
 * WF-G1 is the approved World Focus geometry authority.
 *
 * Change control:
 * - do not alter these values as visual polish;
 * - do not duplicate them in projection/module CSS;
 * - changing them requires an explicit World Focus geometry approval and a
 *   deliberate version bump.
 *
 * The three guide lines mean:
 * - outer + inner: reserved visual-frame band boundaries;
 * - origin: canonical visual origin/reference for future transitions/assets.
 *
 * The workspace is rectangular application layout and is never clipped to the
 * visual-frame curves.
 */
export const WORLD_FOCUS_GEOMETRY = Object.freeze({
  version: WORLD_FOCUS_GEOMETRY_VERSION,
  guidePaths,
  layout,
});

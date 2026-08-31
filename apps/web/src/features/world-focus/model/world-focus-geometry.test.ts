import { describe, expect, it } from 'vitest';

import {
  WORLD_FOCUS_GEOMETRY,
  WORLD_FOCUS_GEOMETRY_VERSION,
} from './world-focus-geometry';

describe('World Focus WF-G3 frozen geometry contract', () => {
  it('keeps the approved concentric ellipse guides and workspace anchors explicit', () => {
    expect(WORLD_FOCUS_GEOMETRY_VERSION).toBe('wf-g3');
    expect(WORLD_FOCUS_GEOMETRY.version).toBe('wf-g3');
    expect(WORLD_FOCUS_GEOMETRY.guideEllipses).toEqual({
      outer: { rx: '52.25%', ry: '90%' },
      origin: { rx: '50%', ry: '87%' },
      inner: { rx: '47.75%', ry: '84%' },
    });
    expect(WORLD_FOCUS_GEOMETRY.layout).toEqual({
      workspaceInlineInset: 'clamp(136px, 14vw, 224px)',
      compactWorkspaceInlineInset: 'clamp(76px, 18vw, 112px)',
      workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
      compactWorkspaceBlockInset: '20px',
      compactTuningMaxPx: 720,
    });
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guideEllipses)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guideEllipses.outer)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guideEllipses.origin)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guideEllipses.inner)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.layout)).toBe(true);
  });
});

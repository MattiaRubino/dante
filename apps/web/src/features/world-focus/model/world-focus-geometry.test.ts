import { describe, expect, it } from 'vitest';

import {
  WORLD_FOCUS_GEOMETRY,
  WORLD_FOCUS_GEOMETRY_VERSION,
} from './world-focus-geometry';

describe('World Focus WF-G1 geometry contract', () => {
  it('keeps the approved geometry version and guide semantics locked', () => {
    expect(WORLD_FOCUS_GEOMETRY_VERSION).toBe('wf-g1');
    expect(WORLD_FOCUS_GEOMETRY.version).toBe('wf-g1');
    expect(WORLD_FOCUS_GEOMETRY.guidePaths).toEqual({
      outer: 'M8 -100 C154 180 154 820 8 1100',
      origin: 'M42 -100 C184 180 184 820 42 1100',
      inner: 'M76 -100 C214 180 214 820 76 1100',
    });
    expect(WORLD_FOCUS_GEOMETRY.layout).toEqual({
      guideViewBox: '0 0 220 1000',
      railWidth: 'clamp(104px, 12vw, 192px)',
      compactRailWidth: 'clamp(56px, 16vw, 88px)',
      workspaceGap: 'clamp(16px, 2vw, 32px)',
      compactWorkspaceGap: '12px',
      workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
      compactWorkspaceBlockInset: '20px',
    });
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guidePaths)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.layout)).toBe(true);
  });
});

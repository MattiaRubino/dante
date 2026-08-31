import { describe, expect, it } from 'vitest';

import {
  WORLD_FOCUS_GEOMETRY,
  WORLD_FOCUS_GEOMETRY_VERSION,
} from './world-focus-geometry';

describe('World Focus WF-G2 candidate geometry contract', () => {
  it('uses three true concentric-circle guides and keeps their geometry explicit', () => {
    expect(WORLD_FOCUS_GEOMETRY_VERSION).toBe('wf-g2-candidate');
    expect(WORLD_FOCUS_GEOMETRY.version).toBe('wf-g2-candidate');
    expect(WORLD_FOCUS_GEOMETRY.guideRadii).toEqual({
      outer: '69.5%',
      origin: '67.5%',
      inner: '65.5%',
    });
    expect(WORLD_FOCUS_GEOMETRY.layout).toEqual({
      workspaceInlineInset: 'clamp(136px, 14vw, 224px)',
      compactWorkspaceInlineInset: 'clamp(76px, 18vw, 112px)',
      workspaceBlockInset: 'clamp(32px, 5vh, 64px)',
      compactWorkspaceBlockInset: '20px',
    });
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.guideRadii)).toBe(true);
    expect(Object.isFrozen(WORLD_FOCUS_GEOMETRY.layout)).toBe(true);
  });
});

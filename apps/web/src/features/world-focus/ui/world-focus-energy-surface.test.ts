import { describe, expect, it, vi } from 'vitest';

import { canUseContinuousWorldFocusEnergy } from './world-focus-energy-surface';

function createContext(renderer: string) {
  const loseContext = vi.fn();
  const debugInfo = { UNMASKED_RENDERER_WEBGL: 0x9246 };
  const getExtension = vi.fn((name: string) => {
    if (name === 'WEBGL_debug_renderer_info') {
      return debugInfo;
    }
    if (name === 'WEBGL_lose_context') {
      return { loseContext };
    }
    return null;
  });
  const getParameter = vi.fn(() => renderer);

  const context = {
    RENDERER: 0x1f01,
    getExtension,
    getParameter,
  } as unknown as WebGL2RenderingContext;

  return { context, loseContext };
}

describe('World Focus energy capability', () => {
  it('rejects a missing or major-caveat WebGL2 context', () => {
    expect(canUseContinuousWorldFocusEnergy(() => null)).toBe(false);
  });

  it('rejects known software rasterizers and releases the probe context', () => {
    const { context, loseContext } = createContext(
      'ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)))',
    );

    expect(canUseContinuousWorldFocusEnergy(() => context)).toBe(false);
    expect(loseContext).toHaveBeenCalledTimes(1);
  });

  it('allows continuous rendering on a hardware renderer and releases the probe context', () => {
    const { context, loseContext } = createContext(
      'ANGLE (NVIDIA, NVIDIA GeForce RTX, OpenGL)',
    );

    expect(canUseContinuousWorldFocusEnergy(() => context)).toBe(true);
    expect(loseContext).toHaveBeenCalledTimes(1);
  });
});

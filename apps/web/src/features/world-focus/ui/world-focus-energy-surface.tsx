import { useState } from 'react';

import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusEnergyCanvas } from './world-focus-energy-canvas';

type WorldFocusEnergySurfaceProps = Readonly<{
  world: WorldFocusWorld;
}>;

type WebGlContextFactory = () => WebGL2RenderingContext | null;

type DebugRendererInfo = Readonly<{
  UNMASKED_RENDERER_WEBGL: number;
}>;

type LoseContextExtension = Readonly<{
  loseContext: () => void;
}>;

const SOFTWARE_RENDERER_PATTERN =
  /swiftshader|llvmpipe|softpipe|software rasterizer|mesa offscreen/i;

function createCapabilityProbeContext(): WebGL2RenderingContext | null {
  if (typeof document === 'undefined') {
    return null;
  }

  try {
    return document.createElement('canvas').getContext('webgl2', {
      alpha: true,
      antialias: false,
      depth: false,
      stencil: false,
      failIfMajorPerformanceCaveat: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: false,
    });
  } catch {
    return null;
  }
}

function readRendererIdentity(gl: WebGL2RenderingContext): string | null {
  try {
    const debugInfo = gl.getExtension(
      'WEBGL_debug_renderer_info',
    ) as DebugRendererInfo | null;
    const renderer = debugInfo
      ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)
      : gl.getParameter(gl.RENDERER);

    return typeof renderer === 'string' ? renderer : null;
  } catch {
    return null;
  }
}

function releaseProbeContext(gl: WebGL2RenderingContext) {
  try {
    const extension = gl.getExtension(
      'WEBGL_lose_context',
    ) as LoseContextExtension | null;
    extension?.loseContext();
  } catch {
    // Capability probing is advisory and must never affect page availability.
  }
}

/**
 * Continuous VFX is ornamental. It is allowed only when WebGL2 can be created
 * without a major performance caveat and the renderer is not a known software
 * rasterizer. The static CSS fallback preserves the World surface on constrained
 * or automation/headless environments without burning the main renderer thread.
 */
export function canUseContinuousWorldFocusEnergy(
  createContext: WebGlContextFactory = createCapabilityProbeContext,
): boolean {
  const gl = createContext();
  if (gl === null) {
    return false;
  }

  try {
    const renderer = readRendererIdentity(gl);
    return renderer === null || !SOFTWARE_RENDERER_PATTERN.test(renderer);
  } finally {
    releaseProbeContext(gl);
  }
}

function WorldFocusStaticEnergyFallback() {
  return (
    <div
      className="world-focus-energy-layer"
      data-world-focus-energy-renderer="fallback"
      data-world-focus-energy-motion="static"
      data-world-focus-vfx-coverage="peripheral-outside-workspace"
      data-world-focus-energy-degradation="performance-capability"
    >
      <div className="world-focus-energy-fallback" aria-hidden="true" />
      <canvas
        className="world-focus-energy-canvas"
        aria-hidden="true"
        data-world-focus-energy-inert
      />
    </div>
  );
}

export function WorldFocusEnergySurface({
  world,
}: WorldFocusEnergySurfaceProps) {
  const [continuousEnergy] = useState(() =>
    canUseContinuousWorldFocusEnergy(),
  );

  return continuousEnergy ? (
    <WorldFocusEnergyCanvas world={world} animated />
  ) : (
    <WorldFocusStaticEnergyFallback />
  );
}

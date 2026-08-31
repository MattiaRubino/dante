import { useEffect, useRef, useState } from 'react';

import type { WorldFocusEntrySnapshot } from '../model/world-focus-transition';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

const ENTRY_DURATION_MS = 1_080;
const MAX_DEVICE_PIXEL_RATIO = 1.5;

const VERTEX_SHADER = `#version 300 es
precision highp float;

void main() {
  vec2 position = vec2(
    gl_VertexID == 1 ? 3.0 : -1.0,
    gl_VertexID == 2 ? 3.0 : -1.0
  );
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const FRAGMENT_SHADER = `#version 300 es
precision highp float;

out vec4 outColor;

uniform vec2 uResolution;
uniform vec2 uOrigin;
uniform float uProgress;
uniform float uTime;
uniform vec3 uAccent;
uniform float uIntensity;
uniform float uDensity;
uniform float uMotion;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;

float hash21(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float valueNoise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);

  float a = hash21(i);
  float b = hash21(i + vec2(1.0, 0.0));
  float c = hash21(i + vec2(0.0, 1.0));
  float d = hash21(i + vec2(1.0, 1.0));

  return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  mat2 rotation = mat2(0.80, -0.60, 0.60, 0.80);

  for (int i = 0; i < 4; i++) {
    value += amplitude * valueNoise(p);
    p = rotation * p * 2.03 + 13.7;
    amplitude *= 0.5;
  }

  return value;
}

float easeOutCubic(float value) {
  float inverse = 1.0 - value;
  return 1.0 - inverse * inverse * inverse;
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  uv.y = 1.0 - uv.y;

  float progress = clamp(uProgress, 0.0, 1.0);
  float eased = easeOutCubic(progress);
  float aspect = uResolution.x / max(uResolution.y, 1.0);

  vec2 p = uv - uOrigin;
  p.x *= aspect;

  float radiusFromOrigin = max(length(p), 0.0001);
  float angle = atan(p.y, p.x);
  float radius = mix(0.018, 1.52, pow(eased, 0.72));

  float angularNoise = fbm(
    vec2(
      angle * 1.45 + uTime * 0.08 * uMotion,
      radiusFromOrigin * 8.0 - uTime * 0.45
    )
  );
  float fineNoise = fbm(p * (8.0 + uDensity * 5.0) - uTime * 0.18);
  float turbulence =
    (angularNoise - 0.5) * 0.075 + (fineNoise - 0.5) * 0.028;
  turbulence *= 0.55 + sin(progress * PI) * 0.75;

  float distortedRadius = radiusFromOrigin + turbulence;
  float edgeDistance = abs(distortedRadius - radius);
  float ringWidth = mix(0.012, 0.044, sin(progress * PI));
  float ring =
    1.0 - smoothstep(ringWidth, ringWidth * 2.6, edgeDistance);
  float innerRing =
    1.0 -
    smoothstep(
      ringWidth * 0.35,
      ringWidth * 1.15,
      abs(distortedRadius - radius * 0.965)
    );
  float inside =
    1.0 -
    smoothstep(radius - 0.035, radius + 0.018, distortedRadius);

  float polarY = log(radiusFromOrigin + 0.035);
  float radialBands = fract(
    polarY * (5.2 + uMotion * 0.7) -
      uTime * (1.45 + uMotion * 0.35)
  );
  float streakBand = pow(1.0 - abs(radialBands - 0.5) * 2.0, 11.0);

  float spokePhase = angle / TAU + 0.5;
  float spokeCell = floor(spokePhase * mix(68.0, 112.0, uDensity));
  float starSeed = hash21(vec2(spokeCell, floor(polarY * 22.0)));
  float starMask = smoothstep(0.84, 0.995, starSeed);
  float streaks = streakBand * starMask * inside;

  float vortex =
    0.5 +
    0.5 *
      sin(
        angle * (5.0 + uMotion) -
          polarY * 13.0 -
          uTime * (2.2 + uMotion * 0.5)
      );
  vortex = pow(vortex, 5.0) * inside;
  vortex *=
    1.0 -
    smoothstep(radius * 0.08, radius + 0.05, radiusFromOrigin);

  float activationFlash = exp(-pow((progress - 0.48) / 0.13, 2.0));
  float coreGlow = exp(-radiusFromOrigin * (3.0 + 1.8 * progress));

  vec3 cold = vec3(0.12, 0.58, 1.0);
  vec3 violet = vec3(0.46, 0.24, 1.0);
  vec3 energy = mix(violet, uAccent, 0.72);
  vec3 edgeColor = mix(cold, uAccent, 0.62);

  vec3 color = vec3(0.012, 0.025, 0.06) * inside;
  color += energy * inside * (0.18 + vortex * 0.34) * uIntensity;
  color += edgeColor * ring * (1.2 + activationFlash * 1.4);
  color += vec3(0.58, 0.83, 1.0) * innerRing * 0.72;
  color +=
    mix(uAccent, vec3(1.0), 0.48) *
    streaks *
    (0.85 + uDensity * 0.7);
  color += edgeColor * coreGlow * activationFlash * 0.62;

  float worldWash =
    inside * smoothstep(0.16, 0.72, progress) * 0.84;
  float effectFade = 1.0 - smoothstep(0.82, 1.0, progress);
  float alpha = max(worldWash, ring * 0.94 + innerRing * 0.54);
  alpha += streaks * 0.48 + coreGlow * activationFlash * 0.18;
  alpha = clamp(alpha * effectFade, 0.0, 0.97);

  outColor = vec4(color, alpha);
}
`;

type RendererMode = 'pending' | 'webgl2' | 'fallback';

type WorldFocusEntryEffectProps = Readonly<{
  entry: WorldFocusEntrySnapshot;
  world: WorldFocusWorld;
  onComplete: () => void;
}>;

type WebGlResources = Readonly<{
  program: WebGLProgram;
  vertexShader: WebGLShader;
  fragmentShader: WebGLShader;
  vertexArray: WebGLVertexArrayObject;
}>;

function clamp(value: number, minimum: number, maximum: number) {
  return Math.max(minimum, Math.min(maximum, value));
}

function parseHexColor(hex: string): readonly [number, number, number] {
  const normalized = hex.startsWith('#') ? hex.slice(1) : hex;
  if (!/^[0-9a-fA-F]{6}$/.test(normalized)) {
    return [0.54, 0.45, 1];
  }

  return [
    Number.parseInt(normalized.slice(0, 2), 16) / 255,
    Number.parseInt(normalized.slice(2, 4), 16) / 255,
    Number.parseInt(normalized.slice(4, 6), 16) / 255,
  ];
}

function compileShader(
  gl: WebGL2RenderingContext,
  type: number,
  source: string,
): WebGLShader {
  const shader = gl.createShader(type);
  if (shader === null) {
    throw new Error('Unable to allocate World Focus shader');
  }

  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const message = gl.getShaderInfoLog(shader) ?? 'Unknown shader error';
    gl.deleteShader(shader);
    throw new Error(message);
  }

  return shader;
}

function createProgram(gl: WebGL2RenderingContext): WebGlResources {
  const vertexShader = compileShader(gl, gl.VERTEX_SHADER, VERTEX_SHADER);
  const fragmentShader = compileShader(gl, gl.FRAGMENT_SHADER, FRAGMENT_SHADER);
  const program = gl.createProgram();
  const vertexArray = gl.createVertexArray();

  if (program === null || vertexArray === null) {
    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);
    throw new Error('Unable to allocate World Focus WebGL resources');
  }

  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const message = gl.getProgramInfoLog(program) ?? 'Unknown program link error';
    gl.deleteProgram(program);
    gl.deleteVertexArray(vertexArray);
    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);
    throw new Error(message);
  }

  return { program, vertexShader, fragmentShader, vertexArray };
}

function destroyProgram(
  gl: WebGL2RenderingContext,
  resources: WebGlResources,
) {
  gl.deleteVertexArray(resources.vertexArray);
  gl.deleteProgram(resources.program);
  gl.deleteShader(resources.vertexShader);
  gl.deleteShader(resources.fragmentShader);
}

function motionWeight(world: WorldFocusWorld) {
  switch (world.theme.motionCharacter) {
    case 'orbit':
      return 1.18;
    case 'drift':
      return 0.88;
    case 'steady':
      return 0.68;
    case 'pulse':
    default:
      return 1;
  }
}

export function WorldFocusEntryEffect({
  entry,
  world,
  onComplete,
}: WorldFocusEntryEffectProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const completionRef = useRef(onComplete);
  const [rendererMode, setRendererMode] = useState<RendererMode>('pending');

  useEffect(() => {
    completionRef.current = onComplete;
  }, [onComplete]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas === null) {
      return;
    }

    const completeWithFallback = () => {
      setRendererMode('fallback');
      const timeout = window.setTimeout(
        () => completionRef.current(),
        ENTRY_DURATION_MS,
      );
      return () => window.clearTimeout(timeout);
    };

    if (typeof window.WebGL2RenderingContext === 'undefined') {
      return completeWithFallback();
    }

    const gl = canvas.getContext('webgl2', {
      alpha: true,
      antialias: false,
      depth: false,
      failIfMajorPerformanceCaveat: true,
      powerPreference: 'high-performance',
      premultipliedAlpha: false,
      preserveDrawingBuffer: false,
      stencil: false,
    });

    if (gl === null) {
      return completeWithFallback();
    }

    let resources: WebGlResources;
    try {
      resources = createProgram(gl);
    } catch {
      gl.getExtension('WEBGL_lose_context')?.loseContext();
      return completeWithFallback();
    }

    setRendererMode('webgl2');

    const resolutionLocation = gl.getUniformLocation(
      resources.program,
      'uResolution',
    );
    const originLocation = gl.getUniformLocation(resources.program, 'uOrigin');
    const progressLocation = gl.getUniformLocation(
      resources.program,
      'uProgress',
    );
    const timeLocation = gl.getUniformLocation(resources.program, 'uTime');
    const accentLocation = gl.getUniformLocation(resources.program, 'uAccent');
    const intensityLocation = gl.getUniformLocation(
      resources.program,
      'uIntensity',
    );
    const densityLocation = gl.getUniformLocation(
      resources.program,
      'uDensity',
    );
    const motionLocation = gl.getUniformLocation(resources.program, 'uMotion');
    const accent = parseHexColor(world.accent);
    const startedAt = performance.now();
    let animationFrame = 0;

    gl.useProgram(resources.program);
    gl.bindVertexArray(resources.vertexArray);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.uniform3f(accentLocation, accent[0], accent[1], accent[2]);
    gl.uniform1f(intensityLocation, world.theme.ambientIntensity);
    gl.uniform1f(densityLocation, world.theme.particleDensity);
    gl.uniform1f(motionLocation, motionWeight(world));

    const resize = () => {
      const bounds = canvas.getBoundingClientRect();
      const dpr = Math.min(
        Math.max(window.devicePixelRatio || 1, 1),
        MAX_DEVICE_PIXEL_RATIO,
      );
      const width = Math.max(1, Math.round(bounds.width * dpr));
      const height = Math.max(1, Math.round(bounds.height * dpr));
      const originCenterX = entry.origin.left + entry.origin.width / 2;
      const originCenterY = entry.origin.top + entry.origin.height / 2;
      const originX = clamp(
        (originCenterX - bounds.left) / Math.max(bounds.width, 1),
        0,
        1,
      );
      const originY = clamp(
        (originCenterY - bounds.top) / Math.max(bounds.height, 1),
        0,
        1,
      );

      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, width, height);
      }

      gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
      gl.uniform2f(originLocation, originX, originY);
    };

    const render = (now: number) => {
      const progress = clamp((now - startedAt) / ENTRY_DURATION_MS, 0, 1);

      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.uniform1f(progressLocation, progress);
      gl.uniform1f(timeLocation, (now - startedAt) / 1_000);
      gl.drawArrays(gl.TRIANGLES, 0, 3);

      if (progress < 1) {
        animationFrame = window.requestAnimationFrame(render);
        return;
      }

      completionRef.current();
    };

    resize();
    window.addEventListener('resize', resize, { passive: true });
    animationFrame = window.requestAnimationFrame(render);

    return () => {
      window.removeEventListener('resize', resize);
      window.cancelAnimationFrame(animationFrame);
      destroyProgram(gl, resources);
      gl.getExtension('WEBGL_lose_context')?.loseContext();
    };
  }, [entry, world]);

  return (
    <canvas
      ref={canvasRef}
      className="world-focus-entry-effect"
      data-world-focus-entry-renderer={rendererMode}
      aria-hidden="true"
    />
  );
}

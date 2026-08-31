import { useEffect, useRef, useState } from 'react';

import type { WorldFocusEntrySnapshot } from '../model/world-focus-transition';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

const ENTRY_DURATION_MS = 1_240;
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
uniform vec2 uTarget;
uniform float uOriginRadius;
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

float easeInOutCubic(float value) {
  return value < 0.5
    ? 4.0 * value * value * value
    : 1.0 - pow(-2.0 * value + 2.0, 3.0) * 0.5;
}

float easeOutQuint(float value) {
  return 1.0 - pow(1.0 - value, 5.0);
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  uv.y = 1.0 - uv.y;

  float progress = clamp(uProgress, 0.0, 1.0);
  float focusProgress = smoothstep(0.0, 0.31, progress);
  float ignition = smoothstep(0.08, 0.34, progress);
  float opening = smoothstep(0.22, 0.84, progress);
  float breach = smoothstep(0.58, 0.96, progress);
  float fadeOut = 1.0 - smoothstep(0.88, 1.0, progress);

  vec2 center = mix(uOrigin, uTarget, easeInOutCubic(focusProgress));
  float aspect = uResolution.x / max(uResolution.y, 1.0);
  vec2 p = uv - center;
  p.x *= aspect;

  float distanceFromCenter = max(length(p), 0.0001);
  float angle = atan(p.y, p.x);

  float seedRadius = max(uOriginRadius, 0.018);
  float lockedRadius = mix(seedRadius, 0.185, easeOutQuint(focusProgress));
  float portalRadius = mix(lockedRadius, 1.34, pow(opening, 0.82));

  float angularNoise = fbm(
    vec2(
      angle * (1.55 + uMotion * 0.11) - uTime * (0.34 + uMotion * 0.08),
      distanceFromCenter * (8.5 + uDensity * 2.5) - uTime * 0.52
    )
  );
  float fineNoise = fbm(
    p * (9.0 + uDensity * 5.5) + vec2(uTime * 0.12, -uTime * 0.22)
  );
  float turbulence = (angularNoise - 0.5) * mix(0.012, 0.082, opening);
  turbulence += (fineNoise - 0.5) * mix(0.006, 0.035, ignition);

  float distortedRadius = distanceFromCenter + turbulence;
  float ringWidth = mix(0.009, 0.043, sin(opening * PI));
  float ringDistance = abs(distortedRadius - portalRadius);
  float outerRing = 1.0 - smoothstep(ringWidth, ringWidth * 2.35, ringDistance);
  float innerRing = 1.0 - smoothstep(
    ringWidth * 0.28,
    ringWidth * 1.08,
    abs(distortedRadius - portalRadius * 0.968)
  );

  float inside = 1.0 - smoothstep(
    portalRadius - ringWidth * 1.4,
    portalRadius + ringWidth * 0.4,
    distortedRadius
  );

  float normalizedRadius = distanceFromCenter / max(portalRadius, 0.001);
  float tunnelDepth = log(distanceFromCenter + 0.028);
  float spiralPhase =
    angle * (4.6 + uMotion * 0.7) -
    tunnelDepth * (13.5 + uMotion * 1.8) -
    uTime * (2.2 + uMotion * 0.52);
  float spiral = 0.5 + 0.5 * sin(spiralPhase);
  spiral = pow(spiral, 5.5) * inside;
  spiral *= 1.0 - smoothstep(0.13, 1.04, normalizedRadius);

  float secondarySpiral = 0.5 + 0.5 * sin(
    -angle * (7.0 + uDensity * 2.0) - tunnelDepth * 18.0 + uTime * 2.8
  );
  secondarySpiral = pow(secondarySpiral, 9.0) * inside * 0.46;

  float radialBand = fract(
    tunnelDepth * (5.4 + uMotion * 0.6) -
    uTime * (1.62 + uMotion * 0.24)
  );
  float streakShape = pow(1.0 - abs(radialBand - 0.5) * 2.0, 13.0);
  float spokePhase = angle / TAU + 0.5;
  float spokeCell = floor(spokePhase * mix(72.0, 126.0, uDensity));
  float streakSeed = hash21(vec2(spokeCell, floor(tunnelDepth * 24.0)));
  float streaks = streakShape * smoothstep(0.79, 0.995, streakSeed) * inside;
  streaks *= 1.0 - smoothstep(0.19, 1.08, normalizedRadius);

  float sparkCell = floor(spokePhase * mix(100.0, 170.0, uDensity));
  float sparkSeed = hash21(vec2(sparkCell, floor(distanceFromCenter * 86.0)));
  float sparks = smoothstep(0.91, 0.998, sparkSeed);
  sparks *= outerRing * (0.55 + uDensity * 0.7);

  float ignitionFlash = exp(-pow((progress - 0.27) / 0.105, 2.0));
  float breachFlash = exp(-pow((progress - 0.69) / 0.16, 2.0));
  float core = exp(-distanceFromCenter * mix(11.0, 2.8, opening));
  float aperture = smoothstep(0.36, 0.94, opening);

  vec3 cold = vec3(0.18, 0.55, 1.0);
  vec3 violet = vec3(0.48, 0.22, 1.0);
  vec3 hot = vec3(1.0, 0.49, 0.16);
  vec3 portalColor = mix(violet, uAccent, 0.68);
  vec3 edgeColor = mix(cold, uAccent, 0.58);
  vec3 hotEdge = mix(portalColor, hot, 0.24 + 0.18 * uMotion);

  vec3 color = vec3(0.005, 0.012, 0.032) * inside;
  color += portalColor * inside * (0.09 + spiral * 0.52) * uIntensity;
  color += edgeColor * secondarySpiral * (0.26 + uIntensity * 0.22);
  color += hotEdge * outerRing * (1.18 + ignitionFlash * 1.42);
  color += mix(vec3(0.72, 0.88, 1.0), uAccent, 0.28) * innerRing * 0.84;
  color += mix(uAccent, vec3(1.0), 0.56) * streaks * (0.72 + uDensity * 0.82);
  color += vec3(1.0, 0.82, 0.62) * sparks * 0.72;
  color += edgeColor * core * ignitionFlash * 0.78;
  color += mix(portalColor, vec3(1.0), 0.34) * breachFlash * inside * 0.18;

  float worldWash = inside * aperture * mix(0.28, 0.92, breach);
  float alpha = max(worldWash, outerRing * 0.96 + innerRing * 0.62);
  alpha += streaks * 0.46 + sparks * 0.34 + core * ignitionFlash * 0.24;
  alpha = clamp(alpha * fadeOut, 0.0, 0.985);

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
      desynchronized: true,
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
    const targetLocation = gl.getUniformLocation(resources.program, 'uTarget');
    const originRadiusLocation = gl.getUniformLocation(
      resources.program,
      'uOriginRadius',
    );
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
    let completed = false;

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
      const aspect = width / Math.max(height, 1);
      const originRadius =
        Math.max(
          (entry.origin.width / Math.max(bounds.width, 1)) * aspect,
          entry.origin.height / Math.max(bounds.height, 1),
        ) * 0.5;

      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, width, height);
      }

      gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
      gl.uniform2f(originLocation, originX, originY);
      gl.uniform2f(targetLocation, 0.5, 0.46);
      gl.uniform1f(originRadiusLocation, clamp(originRadius, 0.018, 0.16));
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

      if (!completed) {
        completed = true;
        completionRef.current();
      }
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

import { useEffect, useRef, useState } from 'react';

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

type WorldFocusEnergyCanvasProps = Readonly<{
  world: WorldFocusWorld;
  animated?: boolean;
}>;

type RendererStatus = 'pending' | 'webgl2' | 'fallback';
type MotionMode = 'animated' | 'reduced' | 'static';
type Rgb = readonly [number, number, number];
type WorkspaceRect = readonly [number, number, number, number];

const MAX_DEVICE_PIXEL_RATIO = 1.4;
const ENTRY_REVEAL_SECONDS = 1.65;
const PARTICLE_STRIDE_FLOATS = 9;
const TAU = Math.PI * 2;

const FULLSCREEN_VERTEX_SHADER = `#version 300 es
precision highp float;

const vec2 POSITIONS[3] = vec2[3](
  vec2(-1.0, -1.0),
  vec2(3.0, -1.0),
  vec2(-1.0, 3.0)
);

void main() {
  gl_Position = vec4(POSITIONS[gl_VertexID], 0.0, 1.0);
}
`;

const FIELD_FRAGMENT_SHADER = `#version 300 es
precision highp float;

out vec4 outColor;

uniform vec2 uResolution;
uniform vec3 uAccent;
uniform vec3 uViolet;
uniform vec3 uHot;
uniform float uIntensity;
uniform float uTime;
uniform float uSeed;
uniform float uReveal;
uniform vec2 uOriginRadius;
uniform vec4 uWorkspaceRect;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;

float hash21(vec2 point) {
  vec3 p3 = fract(vec3(point.xyx) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

float noise2(vec2 point) {
  vec2 cell = floor(point);
  vec2 local = fract(point);
  vec2 smoothLocal = local * local * (3.0 - 2.0 * local);

  float a = hash21(cell);
  float b = hash21(cell + vec2(1.0, 0.0));
  float c = hash21(cell + vec2(0.0, 1.0));
  float d = hash21(cell + vec2(1.0, 1.0));

  return mix(mix(a, b, smoothLocal.x), mix(c, d, smoothLocal.x), smoothLocal.y);
}

float fbm(vec2 point) {
  float value = 0.0;
  float amplitude = 0.52;
  mat2 transform = mat2(0.82, -0.57, 0.57, 0.82);

  for (int octave = 0; octave < 6; octave += 1) {
    value += amplitude * noise2(point);
    point = transform * point * 2.03 + vec2(13.7, 8.9);
    amplitude *= 0.49;
  }

  return value;
}

float ridgedFbm(vec2 point) {
  float value = 0.0;
  float amplitude = 0.58;
  mat2 transform = mat2(0.74, -0.67, 0.67, 0.74);

  for (int octave = 0; octave < 5; octave += 1) {
    float sampleValue = noise2(point);
    float ridge = 1.0 - abs(sampleValue * 2.0 - 1.0);
    value += ridge * ridge * amplitude;
    point = transform * point * 2.11 + vec2(21.3, 5.7);
    amplitude *= 0.47;
  }

  return value;
}

float roundedRectSdf(vec2 point, vec4 rect, float radius) {
  vec2 center = (rect.xy + rect.zw) * 0.5;
  vec2 halfSize = max((rect.zw - rect.xy) * 0.5, vec2(radius + 0.0001));
  vec2 q = abs(point - center) - (halfSize - vec2(radius));
  return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - radius;
}

float outsideWorkspace(vec2 uv) {
  float pixel = 1.0 / min(uResolution.x, uResolution.y);
  float radius = 24.0 * pixel;
  float distanceValue = roundedRectSdf(uv, uWorkspaceRect, radius);
  return smoothstep(-2.0 * pixel, 13.0 * pixel, distanceValue);
}

float sparseStar(vec2 uv, float seed) {
  vec2 gridUv = uv * vec2(96.0, 61.0);
  vec2 cell = floor(gridUv);
  vec2 local = fract(gridUv);
  float gate = step(0.972, hash21(cell + seed * 19.1));
  vec2 center = vec2(
    0.14 + hash21(cell + seed * 3.7) * 0.72,
    0.14 + hash21(cell + seed * 8.9 + 11.0) * 0.72
  );
  float distanceToPoint = length(local - center);
  return gate * pow(max(0.0, 1.0 - distanceToPoint * 8.0), 9.0);
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  float workspaceMask = outsideWorkspace(uv);
  if (workspaceMask < 0.001) {
    discard;
  }

  float aspect = uResolution.x / max(uResolution.y, 1.0);
  vec2 centered = (uv - vec2(0.5)) * vec2(aspect, 1.0);
  vec2 originPoint = (uv - vec2(0.5)) / uOriginRadius;
  float originMetric = length(originPoint);
  float angle = atan(originPoint.y, originPoint.x);
  float turn = fract((angle + PI * 0.5) / TAU);

  float guideDistance = abs(originMetric - 1.0);
  float guideField = exp(-guideDistance * 4.1);
  float atmosphereField = exp(-guideDistance * 1.15);

  vec2 broadWarp = vec2(
    fbm(centered * 2.1 + vec2(uSeed * 2.9, uTime * 0.035)),
    fbm(centered.yx * 2.35 + vec2(-uTime * 0.031, uSeed * 4.7))
  );

  vec2 flowDomain = vec2(
    angle * 1.25 + broadWarp.x * 2.4,
    originMetric * 3.8 + broadWarp.y * 2.1
  );
  float nebulaLarge = fbm(flowDomain * 1.45 + vec2(uSeed * 3.1, uTime * 0.055));
  float nebulaMedium = fbm(
    flowDomain * 3.4 +
    broadWarp * 4.2 +
    vec2(-uTime * 0.075, uSeed * 6.3)
  );

  vec2 filamentDomain = flowDomain * 7.8 + broadWarp * 8.4;
  float filamentNoise = ridgedFbm(
    filamentDomain + vec2(uTime * 0.13, -uSeed * 8.7)
  );
  float filament = smoothstep(0.64, 1.14, filamentNoise);
  filament *= smoothstep(0.25, 0.76, nebulaMedium + nebulaLarge * 0.42);

  float hairNoise = ridgedFbm(
    filamentDomain * 1.92 +
    vec2(-uTime * 0.21, uSeed * 13.1)
  );
  float hair = smoothstep(0.82, 1.22, hairNoise);
  hair *= smoothstep(0.35, 0.82, nebulaMedium);

  float cloudBody = smoothstep(
    0.25,
    0.83,
    nebulaLarge * 0.66 + nebulaMedium * 0.52
  );
  float cloudVoids = smoothstep(
    0.2,
    0.68,
    fbm(centered * 3.1 + broadWarp * 2.7 + vec2(uSeed * 9.0, -uTime * 0.04))
  );
  cloudBody *= mix(0.28, 1.0, cloudVoids);

  float star = sparseStar(uv, uSeed);
  float hotPocket = smoothstep(
    0.67,
    0.93,
    fbm(flowDomain * 4.7 + broadWarp * 3.6 + vec2(uSeed * 10.7, uTime * 0.09))
  );

  float revealMask = 1.0;
  float head = 0.0;
  if (uReveal < 0.999) {
    revealMask = smoothstep(turn - 0.035, turn + 0.018, uReveal);
    float headAngle = -PI * 0.5 + uReveal * TAU;
    vec2 headPoint = vec2(0.5) + vec2(
      cos(headAngle) * uOriginRadius.x,
      sin(headAngle) * uOriginRadius.y
    );
    head = exp(-length((uv - headPoint) * vec2(aspect, 1.0)) * 58.0);
  }

  float irregularEnvelope = clamp(
    0.09 +
    atmosphereField * 0.16 +
    guideField * 0.42 +
    cloudBody * 0.42 +
    filament * 0.34,
    0.0,
    1.0
  );

  float density = workspaceMask * revealMask * irregularEnvelope * clamp(
    0.11 +
    cloudBody * 0.54 +
    filament * 0.82 +
    hair * 0.46 +
    star * 1.3,
    0.0,
    1.0
  );
  density += workspaceMask * head * 0.8;

  float paletteNoise = fbm(
    flowDomain * 1.75 + broadWarp * 1.8 + vec2(uSeed * 4.1, 2.7)
  );
  vec3 color = mix(uViolet, uAccent, smoothstep(0.16, 0.84, paletteNoise));

  float warmSide = smoothstep(
    0.42,
    0.96,
    uv.x + (nebulaLarge - 0.5) * 0.22 + hotPocket * 0.08
  );
  color = mix(color, uHot, warmSide * (0.28 + hotPocket * 0.54));

  vec3 whiteHot = vec3(1.0, 0.965, 0.91);
  float whiteAmount = clamp(
    filament * 0.38 +
    hair * 0.28 +
    star * 1.0 +
    head * 0.9,
    0.0,
    0.86
  );
  color = mix(color, whiteHot, whiteAmount);

  float luminance =
    0.2 +
    cloudBody * 0.46 +
    filament * 0.9 +
    hair * 0.44 +
    star * 2.0 +
    head * 1.35;

  float alpha = density * clamp(0.64 + uIntensity * 0.44, 0.0, 1.18);
  alpha = clamp(alpha, 0.0, 0.94);
  vec3 rgb = color * luminance;

  outColor = vec4(rgb * alpha, alpha);
}
`;

const PARTICLE_VERTEX_SHADER = `#version 300 es
precision highp float;

in float aAngle;
in float aPhase;
in float aSpeed;
in float aRadial;
in float aSize;
in float aDrift;
in float aColorMix;
in float aSeed;
in float aDirection;

uniform vec2 uResolution;
uniform vec2 uOriginRadius;
uniform float uTime;
uniform float uReveal;
uniform float uPointScale;

out float vLife;
out float vColorMix;
out float vSeed;
out float vPointAngle;
out float vStretch;
out float vRevealGate;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;

void main() {
  float age = fract(aPhase + uTime * aSpeed);
  float turn = fract((aAngle + PI * 0.5) / TAU);
  float revealGate = uReveal >= 0.999
    ? 1.0
    : smoothstep(turn - 0.025, turn + 0.015, uReveal);

  float movingAngle = aAngle +
    aDirection * age * (0.07 + aDrift * 0.17);
  vec2 ellipsePoint = vec2(
    cos(movingAngle) * uOriginRadius.x,
    sin(movingAngle) * uOriginRadius.y
  );
  vec2 radial = normalize(ellipsePoint);
  vec2 tangent = normalize(vec2(
    -sin(movingAngle) * uOriginRadius.x,
    cos(movingAngle) * uOriginRadius.y
  )) * aDirection;

  float outward = aRadial +
    pow(age, 1.28) * (0.018 + aDrift * 0.095);
  float tangentTravel = age * (0.012 + aDrift * 0.072);
  float turbulence = sin(
    age * 11.0 + aSeed * 17.0 + movingAngle * 3.0
  );

  vec2 positionUv = vec2(0.5) +
    ellipsePoint +
    radial * (outward + turbulence * 0.007 * age) +
    tangent * tangentTravel;

  vec2 clip = positionUv * 2.0 - 1.0;
  gl_Position = vec4(clip, 0.0, 1.0);

  float lifeEnvelope = sin(PI * age);
  float stretch = 1.6 + aDrift * 2.9;
  gl_PointSize = max(
    1.0,
    aSize * uPointScale * stretch * (0.38 + lifeEnvelope * 0.74)
  );

  vec2 tangentPixels = vec2(
    tangent.x * uResolution.x,
    tangent.y * uResolution.y
  );
  vPointAngle = atan(tangentPixels.y, tangentPixels.x);
  vLife = lifeEnvelope;
  vColorMix = aColorMix;
  vSeed = aSeed;
  vStretch = stretch;
  vRevealGate = revealGate;
}
`;

const PARTICLE_FRAGMENT_SHADER = `#version 300 es
precision highp float;

out vec4 outColor;

uniform vec2 uResolution;
uniform vec4 uWorkspaceRect;
uniform vec3 uAccent;
uniform vec3 uViolet;
uniform vec3 uHot;

in float vLife;
in float vColorMix;
in float vSeed;
in float vPointAngle;
in float vStretch;
in float vRevealGate;

float roundedRectSdf(vec2 point, vec4 rect, float radius) {
  vec2 center = (rect.xy + rect.zw) * 0.5;
  vec2 halfSize = max((rect.zw - rect.xy) * 0.5, vec2(radius + 0.0001));
  vec2 q = abs(point - center) - (halfSize - vec2(radius));
  return length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - radius;
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  float pixel = 1.0 / min(uResolution.x, uResolution.y);
  if (roundedRectSdf(uv, uWorkspaceRect, 24.0 * pixel) < 8.0 * pixel) {
    discard;
  }

  vec2 point = gl_PointCoord - vec2(0.5);
  float cosine = cos(vPointAngle);
  float sine = sin(vPointAngle);
  vec2 rotated = mat2(cosine, sine, -sine, cosine) * point;
  vec2 stretched = vec2(rotated.x, rotated.y * vStretch);
  float distanceValue = length(stretched) * 2.0;

  float shape = 1.0 - smoothstep(0.22, 1.0, distanceValue);
  if (shape < 0.002 || vRevealGate < 0.002) {
    discard;
  }

  vec3 color = mix(uViolet, uAccent, vColorMix);
  color = mix(color, uHot, smoothstep(0.58, 0.98, vColorMix + vSeed * 0.22));
  vec3 whiteHot = vec3(1.0, 0.97, 0.92);
  color = mix(color, whiteHot, pow(shape, 3.0) * 0.66);

  float alpha = shape * vLife * vRevealGate * (0.2 + vSeed * 0.56);
  vec3 rgb = color * (0.48 + shape * 1.42 + vSeed * 0.35);
  outColor = vec4(rgb * alpha, alpha);
}
`;

function parsePercentage(value: string): number {
  return Number.parseFloat(value) / 100;
}

function parseHexColor(value: string): Rgb {
  const normalized = value.trim().replace('#', '');
  if (!/^[0-9a-fA-F]{6}$/.test(normalized)) {
    return [0.55, 0.45, 1.0];
  }

  return [
    Number.parseInt(normalized.slice(0, 2), 16) / 255,
    Number.parseInt(normalized.slice(2, 4), 16) / 255,
    Number.parseInt(normalized.slice(4, 6), 16) / 255,
  ];
}

function worldSeed(id: string): number {
  let hash = 2166136261;
  for (let index = 0; index < id.length; index += 1) {
    hash ^= id.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return (hash >>> 0) / 4294967295;
}

function mulberry32(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state += 0x6d2b79f5;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function particleCountForWidth(width: number): number {
  if (width >= 1400) {
    return 1900;
  }
  if (width >= 900) {
    return 1450;
  }
  if (width >= 721) {
    return 1050;
  }
  return 620;
}

function createParticleData(count: number, seed: number): Float32Array {
  const random = mulberry32(Math.floor(seed * 0xffffffff) ^ 0x9e3779b9);
  const data = new Float32Array(count * PARTICLE_STRIDE_FLOATS);

  for (let index = 0; index < count; index += 1) {
    const offset = index * PARTICLE_STRIDE_FLOATS;
    data[offset] = random() * TAU;
    data[offset + 1] = random();
    data[offset + 2] = 0.035 + random() * 0.072;
    data[offset + 3] = (random() - 0.5) * 0.026;
    data[offset + 4] = 1.0 + random() * 3.6;
    data[offset + 5] = 0.35 + random() * 1.05;
    data[offset + 6] = random();
    data[offset + 7] = random();
    data[offset + 8] = random() < 0.18 ? -1 : 1;
  }

  return data;
}

function compileShader(
  gl: WebGL2RenderingContext,
  type: number,
  source: string,
): WebGLShader | null {
  const shader = gl.createShader(type);
  if (shader === null) {
    return null;
  }

  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    gl.deleteShader(shader);
    return null;
  }

  return shader;
}

function createProgram(
  gl: WebGL2RenderingContext,
  vertexSource: string,
  fragmentSource: string,
): WebGLProgram | null {
  const vertexShader = compileShader(gl, gl.VERTEX_SHADER, vertexSource);
  const fragmentShader = compileShader(gl, gl.FRAGMENT_SHADER, fragmentSource);

  if (vertexShader === null || fragmentShader === null) {
    if (vertexShader !== null) {
      gl.deleteShader(vertexShader);
    }
    if (fragmentShader !== null) {
      gl.deleteShader(fragmentShader);
    }
    return null;
  }

  const program = gl.createProgram();
  if (program === null) {
    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);
    return null;
  }

  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    gl.deleteProgram(program);
    return null;
  }

  return program;
}

function requireUniform(
  gl: WebGL2RenderingContext,
  program: WebGLProgram,
  name: string,
): WebGLUniformLocation | null {
  return gl.getUniformLocation(program, name);
}

function clamp01(value: number): number {
  return Math.min(1, Math.max(0, value));
}

function measureWorkspace(canvas: HTMLCanvasElement): WorkspaceRect {
  const canvasRect = canvas.getBoundingClientRect();
  const shell = canvas.closest('.world-focus-shell');
  const workspace = shell?.querySelector<HTMLElement>(
    '[data-world-focus-region="workspace"]',
  );

  if (
    workspace === null ||
    workspace === undefined ||
    canvasRect.width <= 0 ||
    canvasRect.height <= 0
  ) {
    return [0.14, 0.07, 0.86, 0.93];
  }

  const workspaceRect = workspace.getBoundingClientRect();
  const x0 = clamp01((workspaceRect.left - canvasRect.left) / canvasRect.width);
  const x1 = clamp01((workspaceRect.right - canvasRect.left) / canvasRect.width);
  const top = clamp01((workspaceRect.top - canvasRect.top) / canvasRect.height);
  const bottom = clamp01((workspaceRect.bottom - canvasRect.top) / canvasRect.height);

  return [x0, 1 - bottom, x1, 1 - top];
}

export function WorldFocusEnergyCanvas({
  world,
  animated = true,
}: WorldFocusEnergyCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [rendererStatus, setRendererStatus] =
    useState<RendererStatus>('pending');
  const [motionMode, setMotionMode] = useState<MotionMode>(
    animated ? 'animated' : 'static',
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas === null) {
      return;
    }

    const gl = canvas.getContext('webgl2', {
      alpha: true,
      antialias: false,
      depth: false,
      stencil: false,
      desynchronized: true,
      failIfMajorPerformanceCaveat: false,
      powerPreference: 'high-performance',
      premultipliedAlpha: true,
      preserveDrawingBuffer: false,
    });

    if (gl === null) {
      setRendererStatus('fallback');
      return;
    }

    const fieldProgram = createProgram(
      gl,
      FULLSCREEN_VERTEX_SHADER,
      FIELD_FRAGMENT_SHADER,
    );
    const particleProgram = createProgram(
      gl,
      PARTICLE_VERTEX_SHADER,
      PARTICLE_FRAGMENT_SHADER,
    );

    if (fieldProgram === null || particleProgram === null) {
      if (fieldProgram !== null) {
        gl.deleteProgram(fieldProgram);
      }
      if (particleProgram !== null) {
        gl.deleteProgram(particleProgram);
      }
      setRendererStatus('fallback');
      return;
    }

    const fieldVertexArray = gl.createVertexArray();
    const particleVertexArray = gl.createVertexArray();
    const particleBuffer = gl.createBuffer();

    if (
      fieldVertexArray === null ||
      particleVertexArray === null ||
      particleBuffer === null
    ) {
      if (fieldVertexArray !== null) {
        gl.deleteVertexArray(fieldVertexArray);
      }
      if (particleVertexArray !== null) {
        gl.deleteVertexArray(particleVertexArray);
      }
      if (particleBuffer !== null) {
        gl.deleteBuffer(particleBuffer);
      }
      gl.deleteProgram(fieldProgram);
      gl.deleteProgram(particleProgram);
      setRendererStatus('fallback');
      return;
    }

    const fieldUniforms = {
      resolution: requireUniform(gl, fieldProgram, 'uResolution'),
      accent: requireUniform(gl, fieldProgram, 'uAccent'),
      violet: requireUniform(gl, fieldProgram, 'uViolet'),
      hot: requireUniform(gl, fieldProgram, 'uHot'),
      intensity: requireUniform(gl, fieldProgram, 'uIntensity'),
      time: requireUniform(gl, fieldProgram, 'uTime'),
      seed: requireUniform(gl, fieldProgram, 'uSeed'),
      reveal: requireUniform(gl, fieldProgram, 'uReveal'),
      originRadius: requireUniform(gl, fieldProgram, 'uOriginRadius'),
      workspaceRect: requireUniform(gl, fieldProgram, 'uWorkspaceRect'),
    };
    const particleUniforms = {
      resolution: requireUniform(gl, particleProgram, 'uResolution'),
      originRadius: requireUniform(gl, particleProgram, 'uOriginRadius'),
      time: requireUniform(gl, particleProgram, 'uTime'),
      reveal: requireUniform(gl, particleProgram, 'uReveal'),
      pointScale: requireUniform(gl, particleProgram, 'uPointScale'),
      workspaceRect: requireUniform(gl, particleProgram, 'uWorkspaceRect'),
      accent: requireUniform(gl, particleProgram, 'uAccent'),
      violet: requireUniform(gl, particleProgram, 'uViolet'),
      hot: requireUniform(gl, particleProgram, 'uHot'),
    };

    const accent = parseHexColor(world.accent);
    const violet = parseHexColor('#7049ff');
    const hot = parseHexColor('#ff8b36');
    const seed = worldSeed(world.id);
    const originRadius = WORLD_FOCUS_GEOMETRY.guideEllipses.origin;
    const originRadiusX = parsePercentage(originRadius.rx);
    const originRadiusY = parsePercentage(originRadius.ry);

    let particleCount = 0;
    let workspaceRect: WorkspaceRect = [0.14, 0.07, 0.86, 0.93];
    let devicePixelRatio = 1;
    let animationFrame = 0;
    let resizeObserver: ResizeObserver | null = null;
    let motionQuery: MediaQueryList | null = null;
    let disposed = false;
    let animationEnabled = false;
    let startTime = performance.now();

    const configureParticles = (cssWidth: number) => {
      const nextCount = particleCountForWidth(cssWidth);
      if (nextCount === particleCount) {
        return;
      }

      particleCount = nextCount;
      const particleData = createParticleData(particleCount, seed);
      gl.bindVertexArray(particleVertexArray);
      gl.bindBuffer(gl.ARRAY_BUFFER, particleBuffer);
      gl.bufferData(gl.ARRAY_BUFFER, particleData, gl.STATIC_DRAW);

      const attributeNames = [
        'aAngle',
        'aPhase',
        'aSpeed',
        'aRadial',
        'aSize',
        'aDrift',
        'aColorMix',
        'aSeed',
        'aDirection',
      ];
      const stride = PARTICLE_STRIDE_FLOATS * Float32Array.BYTES_PER_ELEMENT;

      attributeNames.forEach((name, index) => {
        const location = gl.getAttribLocation(particleProgram, name);
        if (location < 0) {
          return;
        }
        gl.enableVertexAttribArray(location);
        gl.vertexAttribPointer(
          location,
          1,
          gl.FLOAT,
          false,
          stride,
          index * Float32Array.BYTES_PER_ELEMENT,
        );
      });
    };

    const updateLayout = () => {
      const rect = canvas.getBoundingClientRect();
      devicePixelRatio = Math.min(
        window.devicePixelRatio || 1,
        MAX_DEVICE_PIXEL_RATIO,
      );
      const width = Math.max(1, Math.round(rect.width * devicePixelRatio));
      const height = Math.max(1, Math.round(rect.height * devicePixelRatio));

      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }

      workspaceRect = measureWorkspace(canvas);
      configureParticles(rect.width);
      gl.viewport(0, 0, width, height);
    };

    const setCommonFieldUniforms = (timeSeconds: number, reveal: number) => {
      if (fieldUniforms.resolution !== null) {
        gl.uniform2f(fieldUniforms.resolution, canvas.width, canvas.height);
      }
      if (fieldUniforms.accent !== null) {
        gl.uniform3f(fieldUniforms.accent, accent[0], accent[1], accent[2]);
      }
      if (fieldUniforms.violet !== null) {
        gl.uniform3f(fieldUniforms.violet, violet[0], violet[1], violet[2]);
      }
      if (fieldUniforms.hot !== null) {
        gl.uniform3f(fieldUniforms.hot, hot[0], hot[1], hot[2]);
      }
      if (fieldUniforms.intensity !== null) {
        gl.uniform1f(fieldUniforms.intensity, world.theme.ambientIntensity);
      }
      if (fieldUniforms.time !== null) {
        gl.uniform1f(fieldUniforms.time, timeSeconds);
      }
      if (fieldUniforms.seed !== null) {
        gl.uniform1f(fieldUniforms.seed, seed * 17.0 + 0.37);
      }
      if (fieldUniforms.reveal !== null) {
        gl.uniform1f(fieldUniforms.reveal, reveal);
      }
      if (fieldUniforms.originRadius !== null) {
        gl.uniform2f(
          fieldUniforms.originRadius,
          originRadiusX,
          originRadiusY,
        );
      }
      if (fieldUniforms.workspaceRect !== null) {
        gl.uniform4f(fieldUniforms.workspaceRect, ...workspaceRect);
      }
    };

    const setCommonParticleUniforms = (timeSeconds: number, reveal: number) => {
      if (particleUniforms.resolution !== null) {
        gl.uniform2f(particleUniforms.resolution, canvas.width, canvas.height);
      }
      if (particleUniforms.originRadius !== null) {
        gl.uniform2f(
          particleUniforms.originRadius,
          originRadiusX,
          originRadiusY,
        );
      }
      if (particleUniforms.time !== null) {
        gl.uniform1f(particleUniforms.time, timeSeconds);
      }
      if (particleUniforms.reveal !== null) {
        gl.uniform1f(particleUniforms.reveal, reveal);
      }
      if (particleUniforms.pointScale !== null) {
        gl.uniform1f(particleUniforms.pointScale, devicePixelRatio);
      }
      if (particleUniforms.workspaceRect !== null) {
        gl.uniform4f(particleUniforms.workspaceRect, ...workspaceRect);
      }
      if (particleUniforms.accent !== null) {
        gl.uniform3f(particleUniforms.accent, accent[0], accent[1], accent[2]);
      }
      if (particleUniforms.violet !== null) {
        gl.uniform3f(particleUniforms.violet, violet[0], violet[1], violet[2]);
      }
      if (particleUniforms.hot !== null) {
        gl.uniform3f(particleUniforms.hot, hot[0], hot[1], hot[2]);
      }
    };

    const draw = (timeSeconds: number, reveal: number) => {
      if (disposed || gl.isContextLost()) {
        return;
      }

      updateLayout();
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.disable(gl.DEPTH_TEST);
      gl.disable(gl.CULL_FACE);

      gl.disable(gl.BLEND);
      gl.useProgram(fieldProgram);
      gl.bindVertexArray(fieldVertexArray);
      setCommonFieldUniforms(timeSeconds, reveal);
      gl.drawArrays(gl.TRIANGLES, 0, 3);

      gl.enable(gl.BLEND);
      gl.blendEquation(gl.FUNC_ADD);
      gl.blendFunc(gl.ONE, gl.ONE);
      gl.useProgram(particleProgram);
      gl.bindVertexArray(particleVertexArray);
      setCommonParticleUniforms(timeSeconds, reveal);
      gl.drawArrays(gl.POINTS, 0, particleCount);
      gl.disable(gl.BLEND);
    };

    const drawSettledFrame = () => {
      window.cancelAnimationFrame(animationFrame);
      animationFrame = window.requestAnimationFrame(() => {
        draw(3.2 + seed * 4.0, 1);
      });
    };

    const renderLoop = (timestamp: number) => {
      if (!animationEnabled || document.visibilityState === 'hidden') {
        return;
      }

      const elapsedSeconds = Math.max(0, (timestamp - startTime) / 1000);
      const reveal = Math.min(1, elapsedSeconds / ENTRY_REVEAL_SECONDS);
      draw(elapsedSeconds * 0.72 + seed * 2.7, reveal);
      animationFrame = window.requestAnimationFrame(renderLoop);
    };

    const startAnimation = (restartReveal: boolean) => {
      window.cancelAnimationFrame(animationFrame);
      if (restartReveal) {
        startTime = performance.now();
      }
      animationFrame = window.requestAnimationFrame(renderLoop);
    };

    const syncMotionPreference = (restartReveal: boolean) => {
      const reduced = motionQuery?.matches === true;
      animationEnabled = animated && !reduced;
      setMotionMode(
        animationEnabled ? 'animated' : animated && reduced ? 'reduced' : 'static',
      );

      if (animationEnabled && document.visibilityState !== 'hidden') {
        startAnimation(restartReveal);
      } else {
        drawSettledFrame();
      }
    };

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'hidden') {
        window.cancelAnimationFrame(animationFrame);
        return;
      }

      if (animationEnabled) {
        startAnimation(false);
      } else {
        drawSettledFrame();
      }
    };

    const handleContextLost = (event: Event) => {
      event.preventDefault();
      window.cancelAnimationFrame(animationFrame);
      setRendererStatus('fallback');
    };

    const handleMotionChange = () => {
      syncMotionPreference(false);
    };

    gl.bindVertexArray(fieldVertexArray);
    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.CULL_FACE);
    updateLayout();

    const shell = canvas.closest('.world-focus-shell');
    const workspace = shell?.querySelector<Element>(
      '[data-world-focus-region="workspace"]',
    );
    resizeObserver = new ResizeObserver(() => {
      updateLayout();
      if (!animationEnabled) {
        drawSettledFrame();
      }
    });
    resizeObserver.observe(canvas);
    if (workspace !== null && workspace !== undefined) {
      resizeObserver.observe(workspace);
    }

    motionQuery =
      typeof window.matchMedia === 'function'
        ? window.matchMedia('(prefers-reduced-motion: reduce)')
        : null;
    motionQuery?.addEventListener('change', handleMotionChange);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    canvas.addEventListener('webglcontextlost', handleContextLost);

    setRendererStatus('webgl2');
    syncMotionPreference(true);

    return () => {
      disposed = true;
      window.cancelAnimationFrame(animationFrame);
      resizeObserver?.disconnect();
      motionQuery?.removeEventListener('change', handleMotionChange);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      canvas.removeEventListener('webglcontextlost', handleContextLost);
      gl.bindBuffer(gl.ARRAY_BUFFER, null);
      gl.bindVertexArray(null);
      gl.useProgram(null);
      gl.deleteBuffer(particleBuffer);
      gl.deleteVertexArray(fieldVertexArray);
      gl.deleteVertexArray(particleVertexArray);
      gl.deleteProgram(fieldProgram);
      gl.deleteProgram(particleProgram);
    };
  }, [animated, world]);

  return (
    <div
      className="world-focus-energy-layer"
      data-world-focus-energy-renderer={rendererStatus}
      data-world-focus-energy-motion={motionMode}
      data-world-focus-vfx-coverage="peripheral-outside-workspace"
    >
      <div className="world-focus-energy-fallback" aria-hidden="true" />
      <canvas
        ref={canvasRef}
        className="world-focus-energy-canvas"
        aria-hidden="true"
      />
    </div>
  );
}

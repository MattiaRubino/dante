import { useEffect, useRef, useState } from 'react';

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

type WorldFocusEnergyCanvasProps = Readonly<{
  world: WorldFocusWorld;
  animated?: boolean;
}>;

type RendererStatus = 'pending' | 'webgl2' | 'fallback';

type Rgb = readonly [number, number, number];

const MAX_DEVICE_PIXEL_RATIO = 1.6;

const VERTEX_SHADER_SOURCE = `#version 300 es
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

const FRAGMENT_SHADER_SOURCE = `#version 300 es
precision highp float;

out vec4 outColor;

uniform vec2 uResolution;
uniform vec3 uAccent;
uniform vec3 uViolet;
uniform vec3 uHot;
uniform float uIntensity;
uniform float uTime;
uniform float uSeed;
uniform vec2 uOuterRadius;
uniform vec2 uOriginRadius;
uniform vec2 uInnerRadius;

const float PI = 3.141592653589793;
const float TAU = 6.283185307179586;

float hash11(float value) {
  return fract(sin(value * 127.1 + 311.7) * 43758.5453123);
}

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
  mat2 rotation = mat2(0.82, -0.57, 0.57, 0.82);

  for (int octave = 0; octave < 5; octave += 1) {
    value += amplitude * noise2(point);
    point = rotation * point * 2.03 + vec2(17.1, 9.2);
    amplitude *= 0.49;
  }

  return value;
}

float ellipseMetric(vec2 uv, vec2 radius) {
  vec2 normalized = (uv - vec2(0.5)) / radius;
  return length(normalized);
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  float pixel = 2.2 / min(uResolution.x, uResolution.y);

  float outerMetric = ellipseMetric(uv, uOuterRadius);
  float innerMetric = ellipseMetric(uv, uInnerRadius);
  float insideOuter = 1.0 - smoothstep(1.0, 1.0 + pixel * 2.0, outerMetric);
  float outsideInner = smoothstep(1.0 - pixel * 2.0, 1.0, innerMetric);
  float band = insideOuter * outsideInner;

  if (band < 0.001) {
    discard;
  }

  vec2 originPoint = (uv - vec2(0.5)) / uOriginRadius;
  float radius = length(originPoint);
  float angle = atan(originPoint.y, originPoint.x);
  float radialDistance = abs(radius - 1.0);
  float normalizedAngle = (angle + PI) / TAU;

  vec2 warpDomain = vec2(angle * 2.15 + uSeed * 0.91, radius * 17.0 - uTime * 0.15);
  float warpA = fbm(warpDomain);
  float warpB = fbm(vec2(
    angle * 5.4 - warpA * 3.8 + uSeed * 1.7,
    radius * 38.0 + warpA * 5.2 + uTime * 0.22
  ));
  float microNoise = fbm(vec2(
    angle * 13.0 + warpB * 2.4,
    radius * 92.0 - warpA * 9.0 - uTime * 0.31
  ));

  float broadGlow = exp(-radialDistance * 22.0);
  float core = exp(-radialDistance * 82.0);

  float filamentA = pow(
    0.5 + 0.5 * sin(angle * 71.0 + radius * 54.0 + warpA * 11.0 + uTime * 0.7),
    7.0
  );
  float filamentB = pow(
    0.5 + 0.5 * sin(angle * 119.0 - radius * 37.0 + warpB * 15.0 - uTime * 0.9),
    12.0
  );
  float filamentC = pow(
    0.5 + 0.5 * sin(angle * 183.0 + radius * 91.0 + microNoise * 8.0 + uTime * 1.1),
    18.0
  );

  float densityBreakup = smoothstep(0.34, 0.82, warpB + microNoise * 0.38);
  float filamentField =
    filamentA * 0.48 +
    filamentB * 0.34 +
    filamentC * 0.22;
  filamentField *= mix(0.22, 1.0, densityBreakup);

  float sectorCount = 168.0;
  float sector = normalizedAngle * sectorCount;
  float sectorId = floor(sector);
  float localAngle = abs(fract(sector) - 0.5);
  float sparkGate = step(0.81, hash11(sectorId + floor(uSeed * 31.0)));
  float sparkOffset = (hash11(sectorId * 3.7 + uSeed * 13.0) - 0.5) * 0.07;
  float spark = exp(-localAngle * 88.0) *
    exp(-abs((radius - 1.0) - sparkOffset) * 165.0) *
    sparkGate;

  float shardGate = step(0.9, hash11(sectorId * 11.3 + uSeed * 7.0));
  float shard = exp(-localAngle * 34.0) *
    exp(-radialDistance * 42.0) *
    shardGate *
    (0.4 + 0.6 * microNoise);

  float energy =
    broadGlow * 0.24 +
    core * 0.92 +
    filamentField * (0.42 + broadGlow * 0.8) +
    spark * 1.5 +
    shard * 0.65;

  float colorWave = 0.5 + 0.5 * sin(angle * 1.17 + warpA * 3.1 + uSeed);
  vec3 baseColor = mix(uViolet, uAccent, colorWave);
  float hotMix = smoothstep(0.48, 0.92, warpB) *
    (0.32 + 0.68 * (0.5 + 0.5 * sin(angle * 1.83 - uSeed)));
  baseColor = mix(baseColor, uHot, hotMix * 0.82);

  vec3 whiteHot = vec3(1.0, 0.975, 0.925);
  float whiteAmount = clamp(core * 0.52 + spark * 0.92 + filamentC * core * 0.35, 0.0, 1.0);
  vec3 color = mix(baseColor, whiteHot, whiteAmount);

  float alpha = band * clamp(
    0.07 +
    broadGlow * 0.16 +
    densityBreakup * 0.14 +
    filamentField * 0.5 +
    core * 0.42 +
    spark * 0.92 +
    shard * 0.38,
    0.0,
    1.0
  );
  alpha *= clamp(0.62 + uIntensity * 0.54, 0.0, 1.35);

  float luminance =
    0.46 +
    energy * 1.16 +
    spark * 1.5 +
    filamentC * core * 0.7;
  vec3 rgb = color * luminance;

  // Premultiplied output gives clean transparent compositing around the band.
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

function createProgram(gl: WebGL2RenderingContext): WebGLProgram | null {
  const vertexShader = compileShader(gl, gl.VERTEX_SHADER, VERTEX_SHADER_SOURCE);
  const fragmentShader = compileShader(
    gl,
    gl.FRAGMENT_SHADER,
    FRAGMENT_SHADER_SOURCE,
  );

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

export function WorldFocusEnergyCanvas({
  world,
  animated = false,
}: WorldFocusEnergyCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [rendererStatus, setRendererStatus] =
    useState<RendererStatus>('pending');

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

    const program = createProgram(gl);
    if (program === null) {
      setRendererStatus('fallback');
      return;
    }

    const vertexArray = gl.createVertexArray();
    if (vertexArray === null) {
      gl.deleteProgram(program);
      setRendererStatus('fallback');
      return;
    }

    gl.bindVertexArray(vertexArray);
    gl.useProgram(program);
    gl.disable(gl.DEPTH_TEST);
    gl.disable(gl.CULL_FACE);
    gl.disable(gl.BLEND);
    gl.clearColor(0, 0, 0, 0);

    const resolutionLocation = requireUniform(gl, program, 'uResolution');
    const accentLocation = requireUniform(gl, program, 'uAccent');
    const violetLocation = requireUniform(gl, program, 'uViolet');
    const hotLocation = requireUniform(gl, program, 'uHot');
    const intensityLocation = requireUniform(gl, program, 'uIntensity');
    const timeLocation = requireUniform(gl, program, 'uTime');
    const seedLocation = requireUniform(gl, program, 'uSeed');
    const outerRadiusLocation = requireUniform(gl, program, 'uOuterRadius');
    const originRadiusLocation = requireUniform(gl, program, 'uOriginRadius');
    const innerRadiusLocation = requireUniform(gl, program, 'uInnerRadius');

    const accent = parseHexColor(world.accent);
    const violet = parseHexColor('#8757ff');
    const hot = parseHexColor('#ff8a38');
    const seed = worldSeed(world.id);
    const outerRadius = WORLD_FOCUS_GEOMETRY.guideEllipses.outer;
    const originRadius = WORLD_FOCUS_GEOMETRY.guideEllipses.origin;
    const innerRadius = WORLD_FOCUS_GEOMETRY.guideEllipses.inner;

    let animationFrame = 0;
    let observer: ResizeObserver | null = null;
    let disposed = false;

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const devicePixelRatio = Math.min(
        window.devicePixelRatio || 1,
        MAX_DEVICE_PIXEL_RATIO,
      );
      const width = Math.max(1, Math.round(rect.width * devicePixelRatio));
      const height = Math.max(1, Math.round(rect.height * devicePixelRatio));

      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }
      gl.viewport(0, 0, width, height);
    };

    const draw = (timeSeconds: number) => {
      if (disposed || gl.isContextLost()) {
        return;
      }

      resize();
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.useProgram(program);
      gl.bindVertexArray(vertexArray);

      if (resolutionLocation !== null) {
        gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
      }
      if (accentLocation !== null) {
        gl.uniform3f(accentLocation, accent[0], accent[1], accent[2]);
      }
      if (violetLocation !== null) {
        gl.uniform3f(violetLocation, violet[0], violet[1], violet[2]);
      }
      if (hotLocation !== null) {
        gl.uniform3f(hotLocation, hot[0], hot[1], hot[2]);
      }
      if (intensityLocation !== null) {
        gl.uniform1f(intensityLocation, world.theme.ambientIntensity);
      }
      if (timeLocation !== null) {
        gl.uniform1f(timeLocation, timeSeconds);
      }
      if (seedLocation !== null) {
        gl.uniform1f(seedLocation, seed * 17.0 + 0.37);
      }
      if (outerRadiusLocation !== null) {
        gl.uniform2f(
          outerRadiusLocation,
          parsePercentage(outerRadius.rx),
          parsePercentage(outerRadius.ry),
        );
      }
      if (originRadiusLocation !== null) {
        gl.uniform2f(
          originRadiusLocation,
          parsePercentage(originRadius.rx),
          parsePercentage(originRadius.ry),
        );
      }
      if (innerRadiusLocation !== null) {
        gl.uniform2f(
          innerRadiusLocation,
          parsePercentage(innerRadius.rx),
          parsePercentage(innerRadius.ry),
        );
      }

      gl.drawArrays(gl.TRIANGLES, 0, 3);
    };

    const renderLoop = (timestamp: number) => {
      draw(timestamp * 0.00032 + seed * 3.0);
      animationFrame = window.requestAnimationFrame(renderLoop);
    };

    const renderStaticFrame = () => {
      window.cancelAnimationFrame(animationFrame);
      animationFrame = window.requestAnimationFrame(() => {
        draw(1.15 + seed * 3.0);
      });
    };

    const handleContextLost = (event: Event) => {
      event.preventDefault();
      window.cancelAnimationFrame(animationFrame);
      setRendererStatus('fallback');
    };

    canvas.addEventListener('webglcontextlost', handleContextLost);
    observer = new ResizeObserver(() => {
      if (!animated) {
        renderStaticFrame();
      }
    });
    observer.observe(canvas);

    setRendererStatus('webgl2');
    if (animated) {
      animationFrame = window.requestAnimationFrame(renderLoop);
    } else {
      renderStaticFrame();
    }

    return () => {
      disposed = true;
      window.cancelAnimationFrame(animationFrame);
      observer?.disconnect();
      canvas.removeEventListener('webglcontextlost', handleContextLost);
      gl.bindVertexArray(null);
      gl.useProgram(null);
      gl.deleteVertexArray(vertexArray);
      gl.deleteProgram(program);
    };
  }, [animated, world]);

  return (
    <div
      className="world-focus-energy-layer"
      data-world-focus-energy-renderer={rendererStatus}
      data-world-focus-energy-motion={animated ? 'animated' : 'static'}
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

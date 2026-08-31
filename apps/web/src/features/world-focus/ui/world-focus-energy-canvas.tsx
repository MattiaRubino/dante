import { useEffect, useRef, useState } from 'react';

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

type WorldFocusEnergyCanvasProps = Readonly<{
  world: WorldFocusWorld;
  animated?: boolean;
}>;

type RendererStatus = 'pending' | 'webgl2' | 'fallback';

type Rgb = readonly [number, number, number];

const MAX_DEVICE_PIXEL_RATIO = 1.45;

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
  float amplitude = 0.5;
  mat2 transform = mat2(0.84, -0.54, 0.54, 0.84);

  for (int octave = 0; octave < 6; octave += 1) {
    value += amplitude * noise2(point);
    point = transform * point * 2.02 + vec2(11.7, 7.9);
    amplitude *= 0.5;
  }

  return value;
}

float ridgedFbm(vec2 point) {
  float value = 0.0;
  float amplitude = 0.56;
  mat2 transform = mat2(0.76, -0.65, 0.65, 0.76);

  for (int octave = 0; octave < 5; octave += 1) {
    float sampleValue = noise2(point);
    float ridge = 1.0 - abs(sampleValue * 2.0 - 1.0);
    value += ridge * ridge * amplitude;
    point = transform * point * 2.08 + vec2(19.1, 4.3);
    amplitude *= 0.48;
  }

  return value;
}

float ellipseMetric(vec2 uv, vec2 radius) {
  return length((uv - vec2(0.5)) / radius);
}

float starSpark(vec2 uv, float seed) {
  vec2 gridUv = uv * vec2(88.0, 58.0);
  vec2 cell = floor(gridUv);
  vec2 local = fract(gridUv);
  float gate = step(0.968, hash21(cell + seed * 13.7));
  vec2 center = vec2(
    0.18 + hash21(cell + seed * 5.1) * 0.64,
    0.18 + hash21(cell + seed * 9.3 + 17.0) * 0.64
  );
  float distanceToSpark = length(local - center);
  float point = pow(max(0.0, 1.0 - distanceToSpark * 8.5), 10.0);
  return gate * point;
}

void main() {
  vec2 uv = gl_FragCoord.xy / uResolution;
  float pixel = 2.0 / min(uResolution.x, uResolution.y);

  float outerMetric = ellipseMetric(uv, uOuterRadius);
  float innerMetric = ellipseMetric(uv, uInnerRadius);
  float insideOuter = 1.0 - smoothstep(1.0, 1.0 + pixel * 2.0, outerMetric);
  float outsideInner = smoothstep(1.0 - pixel * 2.0, 1.0, innerMetric);
  float hardBand = insideOuter * outsideInner;

  if (hardBand < 0.001) {
    discard;
  }

  float outerDepth = max(0.0, 1.0 - outerMetric);
  float innerDepth = max(0.0, innerMetric - 1.0);
  float bandDepth = max(outerDepth + innerDepth, 0.00001);
  float acrossBand = clamp(innerDepth / bandDepth, 0.0, 1.0);

  vec2 originPoint = (uv - vec2(0.5)) / uOriginRadius;
  float angle = atan(originPoint.y, originPoint.x);
  vec2 orbit = vec2(cos(angle), sin(angle));

  vec2 largeDomain = orbit * 2.7 + vec2(
    acrossBand * 1.45 + uSeed * 1.8,
    acrossBand * -1.1 + uTime * 0.035
  );
  float largeCloud = fbm(largeDomain);

  vec2 warp = vec2(
    fbm(orbit * 4.4 + vec2(acrossBand * 3.2, uSeed * 2.1 + uTime * 0.05)),
    fbm(orbit.yx * 4.9 + vec2(-acrossBand * 2.7, uSeed * 3.4 - uTime * 0.04))
  );

  vec2 mediumDomain = orbit * 6.8 +
    warp * 2.9 +
    vec2(acrossBand * 8.5, uSeed * 2.6 + uTime * 0.09);
  float mediumCloud = fbm(mediumDomain);

  vec2 filamentDomain = orbit * 13.0 +
    warp * 5.2 +
    vec2(acrossBand * 19.0 - uTime * 0.12, uSeed * 5.7);
  float filamentNoise = ridgedFbm(filamentDomain);
  float filament = smoothstep(0.62, 1.12, filamentNoise);
  filament *= smoothstep(0.22, 0.76, mediumCloud + largeCloud * 0.34);

  vec2 detailDomain = orbit * 24.0 +
    warp * 7.0 +
    vec2(acrossBand * 41.0, -uSeed * 7.3 + uTime * 0.17);
  float fineCloud = fbm(detailDomain);
  float fineRidge = ridgedFbm(detailDomain * 1.37 + vec2(8.0, 3.0));
  float hair = smoothstep(0.75, 1.18, fineRidge) * smoothstep(0.38, 0.78, fineCloud);

  float edgeWarp = (largeCloud - 0.5) * 0.22 + (mediumCloud - 0.5) * 0.08;
  float warpedAcross = clamp(acrossBand + edgeWarp, 0.0, 1.0);
  float edgeEnvelope = pow(max(0.0, sin(PI * warpedAcross)), 0.38);

  float voids = smoothstep(0.24, 0.58, fbm(
    orbit * 3.6 + warp * 1.4 + vec2(uSeed * 4.1, acrossBand * 5.0)
  ));
  float cloudBody = smoothstep(
    0.24,
    0.78,
    largeCloud * 0.58 + mediumCloud * 0.58 + fineCloud * 0.18
  );
  cloudBody *= mix(0.38, 1.0, voids);

  float spark = starSpark(uv, uSeed);
  float hotPocket = smoothstep(0.66, 0.92, fbm(
    orbit * 5.1 + warp * 2.2 + vec2(acrossBand * 7.2, uSeed * 8.0)
  ));

  float density = edgeEnvelope * clamp(
    0.08 +
    cloudBody * 0.62 +
    filament * 0.78 +
    hair * 0.42 +
    spark * 1.2,
    0.0,
    1.0
  );

  float paletteNoise = fbm(
    orbit * 2.35 + warp * 1.6 + vec2(uSeed * 3.0, acrossBand * 2.8)
  );
  vec3 color = mix(uViolet, uAccent, smoothstep(0.18, 0.82, paletteNoise));
  color = mix(color, uHot, hotPocket * (0.28 + 0.44 * mediumCloud));

  vec3 whiteHot = vec3(1.0, 0.965, 0.9);
  float whiteAmount = clamp(
    filament * 0.46 +
    hair * 0.34 +
    spark * 1.15 +
    smoothstep(0.82, 1.08, filamentNoise) * 0.24,
    0.0,
    0.9
  );
  color = mix(color, whiteHot, whiteAmount);

  float luminance =
    0.34 +
    cloudBody * 0.56 +
    filament * 1.0 +
    hair * 0.55 +
    spark * 2.2;

  float alpha = hardBand * density * clamp(0.72 + uIntensity * 0.42, 0.0, 1.25);
  alpha = clamp(alpha, 0.0, 1.0);

  vec3 rgb = color * luminance;
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
    const violet = parseHexColor('#6f4cff');
    const hot = parseHexColor('#ff9a42');
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

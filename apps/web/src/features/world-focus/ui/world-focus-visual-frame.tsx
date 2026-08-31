import { useMemo } from 'react';

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import { WORLD_FOCUS_REGION } from '../model/world-focus-structure';
import {
  WORLD_FOCUS_VISUAL_LAYER,
  WORLD_FOCUS_VISUAL_VERSION,
} from '../model/world-focus-visual';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import './world-focus-visual-frame.css';

type WorldFocusVisualFrameProps = Readonly<{
  world: WorldFocusWorld;
}>;

type CoronaParticle = Readonly<{
  x: number;
  y: number;
  radius: number;
  opacity: number;
  tone: 'accent' | 'hot' | 'white';
  streak: boolean;
}>;

type Point = Readonly<{ x: number; y: number }>;

const VIEWBOX_SIZE = 1000;
const VIEWBOX_CENTER = VIEWBOX_SIZE / 2;
const CORONA_MARKER_ANGLES = [0, 34, 146, 180, 214, 326] as const;

function percentToViewBox(value: string): number {
  return Number.parseFloat(value) * 10;
}

function hashSeed(value: string): number {
  let hash = 2166136261;
  for (let index = 0; index < value.length; index += 1) {
    hash ^= value.charCodeAt(index);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

function createRandom(seed: number) {
  let state = seed || 1;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

function pointOnEllipse(angleDegrees: number, rx: number, ry: number): Point {
  const angle = (angleDegrees * Math.PI) / 180;
  return {
    x: VIEWBOX_CENTER + rx * Math.cos(angle),
    y: VIEWBOX_CENTER + ry * Math.sin(angle),
  };
}

function buildParticles(
  world: WorldFocusWorld,
  originRx: number,
  originRy: number,
): readonly CoronaParticle[] {
  const random = createRandom(hashSeed(`world-focus:${world.id}`));
  const count = Math.round(54 + world.theme.particleDensity * 48);

  return Array.from({ length: count }, (_, index) => {
    const angle = random() * Math.PI * 2;
    const radialOffset = (random() - 0.5) * 38;
    const rx = originRx + radialOffset;
    const ry = originRy + radialOffset * 1.25;
    const toneRoll = random();

    return {
      x: VIEWBOX_CENTER + rx * Math.cos(angle),
      y: VIEWBOX_CENTER + ry * Math.sin(angle),
      radius: 0.75 + random() * 2.5,
      opacity: 0.28 + random() * 0.68,
      tone:
        toneRoll > 0.78 ? 'white' : toneRoll > 0.46 ? 'hot' : 'accent',
      streak: index % 7 === 0,
    };
  });
}

export function WorldFocusVisualFrame({ world }: WorldFocusVisualFrameProps) {
  const outerRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.outer.rx);
  const outerRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.outer.ry);
  const originRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.origin.rx);
  const originRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.origin.ry);
  const innerRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.inner.rx);
  const innerRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.inner.ry);
  const particles = useMemo(
    () => buildParticles(world, originRx, originRy),
    [originRx, originRy, world],
  );
  const idPrefix = `world-focus-corona-${world.id}`;
  const bandMaskId = `${idPrefix}-band-mask`;
  const spectrumId = `${idPrefix}-spectrum`;
  const flareId = `${idPrefix}-flare`;

  return (
    <div
      className="world-focus-visual-frame"
      data-world-focus-region={WORLD_FOCUS_REGION.visualFrame}
      data-world-focus-visual-version={WORLD_FOCUS_VISUAL_VERSION}
      data-world-focus-motion-character={world.theme.motionCharacter}
      data-world-focus-texture={world.theme.texture}
      aria-hidden="true"
    >
      <div
        className="world-focus-ambient-field"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.ambient}
      />

      <svg
        className="world-focus-corona-svg"
        viewBox={`0 0 ${VIEWBOX_SIZE} ${VIEWBOX_SIZE}`}
        preserveAspectRatio="none"
        focusable="false"
      >
        <defs>
          <mask
            id={bandMaskId}
            maskUnits="userSpaceOnUse"
            x="-100"
            y="-500"
            width="1200"
            height="2000"
          >
            <rect x="-100" y="-500" width="1200" height="2000" fill="black" />
            <ellipse
              cx={VIEWBOX_CENTER}
              cy={VIEWBOX_CENTER}
              rx={outerRx}
              ry={outerRy}
              fill="white"
            />
            <ellipse
              cx={VIEWBOX_CENTER}
              cy={VIEWBOX_CENTER}
              rx={innerRx}
              ry={innerRy}
              fill="black"
            />
          </mask>

          <linearGradient
            id={spectrumId}
            gradientUnits="userSpaceOnUse"
            x1="0"
            y1="180"
            x2={VIEWBOX_SIZE}
            y2="820"
          >
            <stop className="world-focus-corona-stop world-focus-corona-stop--violet" offset="0%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--accent" offset="30%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--white" offset="49%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--hot" offset="72%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--accent" offset="100%" />
          </linearGradient>

          <radialGradient id={flareId} cx="50%" cy="50%" r="68%">
            <stop className="world-focus-corona-stop world-focus-corona-stop--white" offset="0%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--accent" offset="42%" />
            <stop className="world-focus-corona-stop world-focus-corona-stop--transparent" offset="100%" />
          </radialGradient>
        </defs>

        <g
          className="world-focus-corona-field"
          data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaField}
          mask={`url(#${bandMaskId})`}
        >
          <rect
            className="world-focus-corona-band-fill"
            x="-100"
            y="-500"
            width="1200"
            height="2000"
            fill={`url(#${spectrumId})`}
          />
          <rect
            className="world-focus-corona-band-flare"
            x="-100"
            y="-500"
            width="1200"
            height="2000"
            fill={`url(#${flareId})`}
          />
        </g>

        <g
          className="world-focus-corona-energy"
          data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaEnergy}
          mask={`url(#${bandMaskId})`}
        >
          <ellipse
            className="world-focus-corona-halo world-focus-corona-halo--wide"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx}
            ry={originRy}
            fill="none"
            stroke={`url(#${spectrumId})`}
            pathLength={1000}
          />
          <ellipse
            className="world-focus-corona-halo world-focus-corona-halo--mid"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx}
            ry={originRy}
            fill="none"
            stroke={`url(#${spectrumId})`}
            pathLength={1000}
          />
          <ellipse
            className="world-focus-corona-core"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx}
            ry={originRy}
            fill="none"
            stroke={`url(#${spectrumId})`}
            pathLength={1000}
          />
          <ellipse
            className="world-focus-corona-thread world-focus-corona-thread--outer"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={outerRx - 7}
            ry={outerRy - 10}
            fill="none"
            stroke={`url(#${spectrumId})`}
            pathLength={1000}
          />
          <ellipse
            className="world-focus-corona-thread world-focus-corona-thread--inner"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={innerRx + 8}
            ry={innerRy + 10}
            fill="none"
            stroke={`url(#${spectrumId})`}
            pathLength={1000}
          />
        </g>

        <g
          className="world-focus-corona-geometry"
          data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaGeometry}
          mask={`url(#${bandMaskId})`}
        >
          <ellipse
            className="world-focus-corona-orbit world-focus-corona-orbit--a"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx + 11}
            ry={originRy + 14}
            fill="none"
            pathLength={1000}
          />
          <ellipse
            className="world-focus-corona-orbit world-focus-corona-orbit--b"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx - 11}
            ry={originRy - 14}
            fill="none"
            pathLength={1000}
          />

          {CORONA_MARKER_ANGLES.map((angle) => {
            const innerPoint = pointOnEllipse(angle, innerRx + 3, innerRy + 4);
            const outerPoint = pointOnEllipse(angle, outerRx - 3, outerRy - 4);
            const originPoint = pointOnEllipse(angle, originRx, originRy);

            return (
              <g key={angle} className="world-focus-corona-marker">
                <line
                  x1={innerPoint.x}
                  y1={innerPoint.y}
                  x2={outerPoint.x}
                  y2={outerPoint.y}
                />
                <rect
                  x={originPoint.x - 4.25}
                  y={originPoint.y - 4.25}
                  width="8.5"
                  height="8.5"
                  transform={`rotate(45 ${originPoint.x} ${originPoint.y})`}
                />
              </g>
            );
          })}
        </g>

        <g
          className="world-focus-corona-particles"
          data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaParticles}
          mask={`url(#${bandMaskId})`}
        >
          {particles.map((particle, index) => (
            <g key={`${particle.x}-${particle.y}-${index}`}>
              {particle.streak ? (
                <line
                  className="world-focus-corona-particle-streak"
                  x1={particle.x - 5}
                  y1={particle.y - 1.2}
                  x2={particle.x + 5}
                  y2={particle.y + 1.2}
                  data-particle-tone={particle.tone}
                  opacity={particle.opacity * 0.5}
                />
              ) : null}
              <circle
                className="world-focus-corona-particle"
                cx={particle.x}
                cy={particle.y}
                r={particle.radius}
                data-particle-tone={particle.tone}
                opacity={particle.opacity}
              />
            </g>
          ))}
        </g>
      </svg>
    </div>
  );
}

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import { WORLD_FOCUS_REGION } from '../model/world-focus-structure';
import {
  WORLD_FOCUS_VISUAL_LAYER,
  WORLD_FOCUS_VISUAL_VERSION,
} from '../model/world-focus-visual';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusEnergyCanvas } from './world-focus-energy-canvas';
import './world-focus-visual-frame.css';

type WorldFocusVisualFrameProps = Readonly<{
  world: WorldFocusWorld;
}>;

const VIEWBOX_SIZE = 1000;
const VIEWBOX_CENTER = VIEWBOX_SIZE / 2;

function percentToViewBox(value: string): number {
  return Number.parseFloat(value) * 10;
}

export function WorldFocusVisualFrame({ world }: WorldFocusVisualFrameProps) {
  const outerRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.outer.rx);
  const outerRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.outer.ry);
  const originRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.origin.rx);
  const originRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.origin.ry);
  const innerRx = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.inner.rx);
  const innerRy = percentToViewBox(WORLD_FOCUS_GEOMETRY.guideEllipses.inner.ry);
  const idPrefix = `world-focus-corona-${world.id}`;
  const fallbackMaskId = `${idPrefix}-fallback-mask`;
  const fallbackGradientId = `${idPrefix}-fallback-gradient`;
  const turbulenceId = `${idPrefix}-turbulence`;

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
        className="world-focus-corona-fallback-svg"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaFallback}
        viewBox={`0 0 ${VIEWBOX_SIZE} ${VIEWBOX_SIZE}`}
        preserveAspectRatio="none"
        focusable="false"
      >
        <defs>
          <mask
            id={fallbackMaskId}
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
            id={fallbackGradientId}
            gradientUnits="userSpaceOnUse"
            x1="80"
            y1="90"
            x2="920"
            y2="910"
          >
            <stop offset="0%" stopColor="var(--world-focus-violet)" />
            <stop offset="34%" stopColor="var(--world-focus-accent)" />
            <stop offset="55%" stopColor="rgba(255, 250, 242, 0.98)" />
            <stop offset="76%" stopColor="var(--world-focus-hot)" />
            <stop offset="100%" stopColor="var(--world-focus-accent)" />
          </linearGradient>

          <filter
            id={turbulenceId}
            x="-20%"
            y="-20%"
            width="140%"
            height="140%"
            colorInterpolationFilters="sRGB"
          >
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.008 0.055"
              numOctaves="4"
              seed="17"
              result="noise"
            />
            <feDisplacementMap
              in="SourceGraphic"
              in2="noise"
              scale="34"
              xChannelSelector="R"
              yChannelSelector="B"
            />
          </filter>
        </defs>

        <g mask={`url(#${fallbackMaskId})`} filter={`url(#${turbulenceId})`}>
          <ellipse
            className="world-focus-fallback-energy world-focus-fallback-energy--broad"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx}
            ry={originRy}
            fill="none"
            stroke={`url(#${fallbackGradientId})`}
          />
          <ellipse
            className="world-focus-fallback-energy world-focus-fallback-energy--core"
            cx={VIEWBOX_CENTER}
            cy={VIEWBOX_CENTER}
            rx={originRx}
            ry={originRy}
            fill="none"
            stroke={`url(#${fallbackGradientId})`}
          />
        </g>
      </svg>

      <div
        className="world-focus-corona-energy-renderer"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaEnergy}
      >
        <WorldFocusEnergyCanvas world={world} animated={false} />
      </div>

      <svg
        className="world-focus-corona-reference-overlay"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaReference}
        viewBox={`0 0 ${VIEWBOX_SIZE} ${VIEWBOX_SIZE}`}
        preserveAspectRatio="none"
        focusable="false"
      >
        <ellipse
          className="world-focus-corona-reference world-focus-corona-reference--outer"
          cx={VIEWBOX_CENTER}
          cy={VIEWBOX_CENTER}
          rx={outerRx}
          ry={outerRy}
          fill="none"
          pathLength={1000}
        />
        <ellipse
          className="world-focus-corona-reference world-focus-corona-reference--origin"
          cx={VIEWBOX_CENTER}
          cy={VIEWBOX_CENTER}
          rx={originRx}
          ry={originRy}
          fill="none"
          pathLength={1000}
        />
        <ellipse
          className="world-focus-corona-reference world-focus-corona-reference--inner"
          cx={VIEWBOX_CENTER}
          cy={VIEWBOX_CENTER}
          rx={innerRx}
          ry={innerRy}
          fill="none"
          pathLength={1000}
        />
      </svg>
    </div>
  );
}

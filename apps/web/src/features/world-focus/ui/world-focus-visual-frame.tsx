import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import { WORLD_FOCUS_REGION } from '../model/world-focus-structure';
import {
  WORLD_FOCUS_VISUAL_LAYER,
  WORLD_FOCUS_VISUAL_VERSION,
} from '../model/world-focus-visual';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusEnergySurface } from './world-focus-energy-surface';
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

  return (
    <div
      className="world-focus-visual-frame"
      data-world-focus-region={WORLD_FOCUS_REGION.visualFrame}
      data-world-focus-visual-version={WORLD_FOCUS_VISUAL_VERSION}
      data-world-focus-motion-character={world.theme.motionCharacter}
      data-world-focus-texture={world.theme.texture}
      data-world-focus-vfx-boundary="workspace-protected"
      aria-hidden="true"
    >
      <div
        className="world-focus-ambient-field"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.ambient}
      />

      <div
        className="world-focus-corona-energy-renderer"
        data-world-focus-visual-layer={WORLD_FOCUS_VISUAL_LAYER.coronaEnergy}
      >
        <WorldFocusEnergySurface world={world} />
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
        />
        <ellipse
          className="world-focus-corona-reference world-focus-corona-reference--origin"
          cx={VIEWBOX_CENTER}
          cy={VIEWBOX_CENTER}
          rx={originRx}
          ry={originRy}
          fill="none"
        />
        <ellipse
          className="world-focus-corona-reference world-focus-corona-reference--inner"
          cx={VIEWBOX_CENTER}
          cy={VIEWBOX_CENTER}
          rx={innerRx}
          ry={innerRy}
          fill="none"
        />
      </svg>
    </div>
  );
}

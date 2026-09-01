import { useTranslation } from 'react-i18next';

import type { WorldFocusSessionSnapshot } from '../application/world-focus-session';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import type { WorldFocusTimePreset } from '../model/world-focus-lens';

export type WorldFocusTimePresetChangeHandler = (
  preset: WorldFocusTimePreset,
) => void;

type WorldFocusContextProps = Readonly<{
  world: WorldFocusWorld;
  session: WorldFocusSessionSnapshot;
  disabled?: boolean;
  onTimePresetChange?: WorldFocusTimePresetChangeHandler;
}>;

export function WorldFocusContext({
  world,
  session,
  disabled = false,
  onTimePresetChange,
}: WorldFocusContextProps) {
  const { t } = useTranslation('common');
  const label = t(($) => $.common.worldFocus.worlds[world.id].label);
  const description = t(
    ($) => $.common.worldFocus.worlds[world.id].description,
  );
  const temporalLens = world.lens?.time;
  const selectedPreset = session.lens.time?.preset;

  const presetLabels: Record<WorldFocusTimePreset, string> = {
    '7d': t(($) => $.common.worldFocus.lens.presets.last7Days),
    '30d': t(($) => $.common.worldFocus.lens.presets.last30Days),
    '90d': t(($) => $.common.worldFocus.lens.presets.last90Days),
    '1y': t(($) => $.common.worldFocus.lens.presets.lastYear),
    all: t(($) => $.common.worldFocus.lens.presets.allTime),
  };

  return (
    <header
      className="world-focus-context"
      data-world-focus-context="true"
      data-world-focus-scope-key={session.scopeKey}
    >
      <div className="world-focus-context-copy">
        <p className="world-focus-context-kicker">
          {t(($) => $.common.worldFocus.kicker)}
        </p>
        <h1 className="world-focus-context-title">{label}</h1>
        <p className="world-focus-context-description">{description}</p>
      </div>

      {temporalLens === undefined || selectedPreset === undefined ? null : (
        <div
          className="world-focus-lens"
          aria-label={t(($) => $.common.worldFocus.lens.label)}
        >
          <div
            className="world-focus-lens-segments"
            role="group"
            aria-label={t(($) => $.common.worldFocus.lens.timeLabel)}
          >
            {temporalLens.presets.map((preset) => (
              <button
                key={preset}
                type="button"
                className="world-focus-lens-segment"
                aria-pressed={preset === selectedPreset}
                disabled={disabled}
                onClick={() => onTimePresetChange?.(preset)}
              >
                {presetLabels[preset]}
              </button>
            ))}
          </div>

          <label className="world-focus-lens-compact">
            <span className="world-focus-visually-hidden">
              {t(($) => $.common.worldFocus.lens.timeLabel)}
            </span>
            <select
              className="world-focus-lens-select"
              value={selectedPreset}
              disabled={disabled}
              onChange={(event) =>
                onTimePresetChange?.(event.target.value as WorldFocusTimePreset)
              }
            >
              {temporalLens.presets.map((preset) => (
                <option key={preset} value={preset}>
                  {presetLabels[preset]}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}
    </header>
  );
}

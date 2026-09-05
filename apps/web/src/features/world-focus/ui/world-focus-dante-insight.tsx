import { useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusSurfaceRendererProps } from './world-focus-surface-registry';
import { useWorldFocusDanteInsight } from './world-focus-dante-insight-context';

export {
  WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  WORLD_FOCUS_DANTE_INSIGHT_KIND,
} from './world-focus-dante-insight-context';

export function WorldFocusDanteInsight({
  isCurrentGeneration,
  onRequestClose,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const { insight } = useWorldFocusDanteInsight();
  const closeRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    queueMicrotask(() => closeRef.current?.focus({ preventScroll: true }));
  }, []);

  if (insight === null || !isCurrentGeneration) {
    return (
      <section
        className="world-focus-dante-insight world-focus-dante-insight-unavailable"
        data-world-focus-dante-surface="insight"
        role="dialog"
        aria-modal="false"
        aria-labelledby="world-focus-dante-insight-unavailable-title"
      >
        <header className="world-focus-dante-insight-header">
          <h2 id="world-focus-dante-insight-unavailable-title">
            {t(($) => $.common.worldFocus.dante.insight.title)}
          </h2>
          <button
            ref={closeRef}
            className="world-focus-dante-insight-close"
            type="button"
            aria-label={t(($) => $.common.worldFocus.dante.insight.close)}
            onClick={onRequestClose}
          >
            <span aria-hidden="true">×</span>
          </button>
        </header>
        <p className="world-focus-dante-insight-state" role="status">
          {t(($) => $.common.worldFocus.dante.insight.unavailable)}
        </p>
      </section>
    );
  }

  const referenceCount = 1 + insight.basisReferences.supporting.length;

  return (
    <section
      className="world-focus-dante-insight"
      data-world-focus-dante-surface="insight"
      data-world-focus-dante-insight-kind={insight.kind}
      role="dialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-insight-title"
    >
      <header className="world-focus-dante-insight-header">
        <div>
          <span className="world-focus-dante-insight-kicker">
            {t(($) => $.common.worldFocus.dante.insight.kicker)}
          </span>
          <h2 id="world-focus-dante-insight-title">{insight.title}</h2>
        </div>
        <button
          ref={closeRef}
          className="world-focus-dante-insight-close"
          type="button"
          aria-label={t(($) => $.common.worldFocus.dante.insight.close)}
          onClick={onRequestClose}
        >
          <span aria-hidden="true">×</span>
        </button>
      </header>

      <div className="world-focus-dante-insight-body">
        <p className="world-focus-dante-insight-kind">
          {t(($) => $.common.worldFocus.dante.insight.kinds[insight.kind])}
        </p>
        <p className="world-focus-dante-insight-summary">{insight.summary}</p>
        <p className="world-focus-dante-insight-basis">
          {t(($) => $.common.worldFocus.dante.insight.basis, {
            count: referenceCount,
          })}
        </p>
        <p className="world-focus-dante-insight-truth-note">
          {t(($) => $.common.worldFocus.dante.insight.truthNote)}
        </p>
      </div>
    </section>
  );
}

import { useCallback, useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { HOME_COSMOS_DATA_URL } from '../assets/home-cosmos';
import { AISurface } from './ai-surface/ai-surface';
import { CentralStage } from './central-stage/central-stage';
import { ContextRail } from './context-rail/context-rail';
import { DayContextStrip } from './orientation/day-context-strip';
import { Orientation } from './orientation/orientation';
import { TimelineSurface } from './timeline/timeline-surface';

type TimelineExpansionMetrics = Readonly<{
  railWidth: number;
  gap: number;
}>;

type HomeShellProps = Readonly<{
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
}>;

export function HomeShell({
  viewedDateIso,
  onViewedDateChange,
}: HomeShellProps) {
  const { t } = useTranslation('common');
  const [isAiCollapsed, setIsAiCollapsed] = useState(false);
  const [isTimelineExpanded, setIsTimelineExpanded] = useState(false);
  const [localViewedDateIso, setLocalViewedDateIso] = useState(viewedDateIso);
  const todayLayoutRef = useRef<HTMLElement | null>(null);
  const timelineExpansionMetricsRef = useRef<TimelineExpansionMetrics | null>(
    null,
  );

  useEffect(() => {
    setLocalViewedDateIso(viewedDateIso);
  }, [viewedDateIso]);

  const navigateViewedDate = useCallback(
    (isoDate: string | undefined) => {
      setLocalViewedDateIso(isoDate);
      onViewedDateChange?.(isoDate);
    },
    [onViewedDateChange],
  );

  const mirrorTimelineViewedDate = useCallback(
    (isoDate: string | undefined) => {
      setLocalViewedDateIso((current) =>
        current === isoDate ? current : isoDate,
      );
    },
    [],
  );

  const applyTimelineExpansionProgress = useCallback((progress: number) => {
    const layout = todayLayoutRef.current;
    if (!layout) {
      return;
    }

    const p = Math.max(0, Math.min(1, progress));
    if (!timelineExpansionMetricsRef.current) {
      const computed = getComputedStyle(layout);
      const railWidth = Number.parseFloat(
        computed.getPropertyValue('--home-today-rail-width'),
      );
      const gap = Number.parseFloat(computed.getPropertyValue('--home-today-gap'));
      timelineExpansionMetricsRef.current = {
        railWidth: Number.isFinite(railWidth) ? railWidth : 306,
        gap: Number.isFinite(gap) ? gap : 16,
      };
    }

    const metrics = timelineExpansionMetricsRef.current;
    const compactViewport = window.innerWidth <= 1120;
    const visible = compactViewport ? 0 : 1 - p;
    layout.style.setProperty(
      '--rail-width',
      `${compactViewport ? 0 : metrics.railWidth * visible}px`,
    );
    layout.style.setProperty(
      '--layout-gap',
      `${compactViewport ? 0 : metrics.gap * visible}px`,
    );
    layout.style.setProperty('--rail-opacity', String(visible));
    layout.style.setProperty('--rail-shift', `${18 * p}px`);

    if (!compactViewport && p > 0.001 && p < 0.999) {
      layout.dataset.timelineResizing = 'true';
    } else {
      delete layout.dataset.timelineResizing;
    }
  }, []);

  return (
    <div
      className="home-shell home-m1"
      data-home-region="shell"
      data-home-ai-state={isAiCollapsed ? 'collapsed' : 'expanded'}
      data-home-timeline-state={isTimelineExpanded ? 'expanded' : 'normal'}
      data-home-visual-source="b2-v27"
    >
      <div className="home-m1-backdrop" aria-hidden="true">
        <img src={HOME_COSMOS_DATA_URL} alt="" />
        <span />
      </div>

      <main
        className="home-main"
        aria-label={t(($) => $.common.home.shell.mainLabel)}
      >
        <section className="home-hero" data-home-layout="hero">
          <DayContextStrip
            viewedDateIso={localViewedDateIso}
            onViewedDateChange={navigateViewedDate}
          />

          <div className="home-hero-body">
            <AISurface
              collapsed={isAiCollapsed}
              onToggleCollapsed={() => setIsAiCollapsed((value) => !value)}
            />

            <div
              className="home-upper-workspace"
              data-home-layout="upper-workspace"
            >
              <Orientation />
              <CentralStage />
            </div>
          </div>
        </section>

        <section
          ref={todayLayoutRef}
          className="home-today-layout"
          data-home-layout="today"
          data-expanded={isTimelineExpanded ? 'true' : 'false'}
        >
          <TimelineSurface
            expanded={isTimelineExpanded}
            onExpandedChange={setIsTimelineExpanded}
            onExpansionProgress={applyTimelineExpansionProgress}
            viewedDateIso={localViewedDateIso}
            onViewedDateChange={mirrorTimelineViewedDate}
            onDateNavigation={navigateViewedDate}
          />
          <ContextRail />
        </section>
      </main>
    </div>
  );
}

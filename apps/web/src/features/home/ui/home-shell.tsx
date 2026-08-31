import {
  useCallback,
  useRef,
  useState,
  type MouseEvent as ReactMouseEvent,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import { HOME_COSMOS_DATA_URL } from '../assets/home-cosmos';
import type { HomeWorldOpenIntent } from '../model/home-world-focus';
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
  preferredName?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
  onOpenWorldFocus?: ((intent: HomeWorldOpenIntent) => void) | undefined;
}>;

type ViewedDateMirror = Readonly<{
  externalIso: string | undefined;
  localIso: string | undefined;
}>;

type WorldFocusPointerPress = {
  pointerId: number;
  startX: number;
  startY: number;
  element: HTMLElement;
};

const WORLD_FOCUS_CLICK_TRAVEL_THRESHOLD = 7;

function getActiveWorldButton(target: EventTarget | null) {
  if (!(target instanceof Element)) {
    return null;
  }

  return target.closest<HTMLElement>(
    '[data-world-logical][aria-current="true"]',
  );
}

export function HomeShell({
  viewedDateIso,
  preferredName,
  onViewedDateChange,
  onOpenWorldFocus,
}: HomeShellProps) {
  const { t } = useTranslation('common');
  const [isAiCollapsed, setIsAiCollapsed] = useState(false);
  const [isTimelineExpanded, setIsTimelineExpanded] = useState(false);
  const [viewedDateMirror, setViewedDateMirror] = useState<ViewedDateMirror>(
    () => ({
      externalIso: viewedDateIso,
      localIso: viewedDateIso,
    }),
  );
  const todayLayoutRef = useRef<HTMLElement | null>(null);
  const timelineExpansionMetricsRef = useRef<TimelineExpansionMetrics | null>(
    null,
  );
  const worldFocusPressRef = useRef<WorldFocusPointerPress | null>(null);

  const localViewedDateIso =
    viewedDateMirror.externalIso === viewedDateIso
      ? viewedDateMirror.localIso
      : viewedDateIso;

  const navigateViewedDate = useCallback(
    (isoDate: string | undefined) => {
      setViewedDateMirror({
        externalIso: viewedDateIso,
        localIso: isoDate,
      });
      onViewedDateChange?.(isoDate);
    },
    [onViewedDateChange, viewedDateIso],
  );

  const mirrorTimelineViewedDate = useCallback(
    (isoDate: string | undefined) => {
      setViewedDateMirror((current) => {
        const currentLocalIso =
          current.externalIso === viewedDateIso
            ? current.localIso
            : viewedDateIso;
        if (
          current.externalIso === viewedDateIso &&
          currentLocalIso === isoDate
        ) {
          return current;
        }
        return {
          externalIso: viewedDateIso,
          localIso: isoDate,
        };
      });
    },
    [viewedDateIso],
  );

  const emitWorldFocusIntent = useCallback(
    (element: HTMLElement) => {
      if (onOpenWorldFocus === undefined) {
        return;
      }

      const label = element.getAttribute('aria-label')?.trim();
      if (!label) {
        return;
      }

      const rect = element.getBoundingClientRect();
      onOpenWorldFocus({
        label,
        origin: {
          left: rect.left,
          top: rect.top,
          width: rect.width,
          height: rect.height,
        },
      });
    },
    [onOpenWorldFocus],
  );

  const handleWorldFocusPointerDownCapture = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      if (
        onOpenWorldFocus === undefined ||
        (event.pointerType === 'mouse' && event.button !== 0)
      ) {
        worldFocusPressRef.current = null;
        return;
      }

      const element = getActiveWorldButton(event.target);
      worldFocusPressRef.current =
        element === null
          ? null
          : {
              pointerId: event.pointerId,
              startX: event.clientX,
              startY: event.clientY,
              element,
            };
    },
    [onOpenWorldFocus],
  );

  const handleWorldFocusPointerUpCapture = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      const press = worldFocusPressRef.current;
      worldFocusPressRef.current = null;

      if (press === null || press.pointerId !== event.pointerId) {
        return;
      }

      const travel = Math.hypot(
        event.clientX - press.startX,
        event.clientY - press.startY,
      );

      if (
        travel <= WORLD_FOCUS_CLICK_TRAVEL_THRESHOLD &&
        press.element.isConnected &&
        press.element.getAttribute('aria-current') === 'true'
      ) {
        emitWorldFocusIntent(press.element);
      }
    },
    [emitWorldFocusIntent],
  );

  const handleWorldFocusPointerCancelCapture = useCallback(
    (event: ReactPointerEvent<HTMLDivElement>) => {
      if (worldFocusPressRef.current?.pointerId === event.pointerId) {
        worldFocusPressRef.current = null;
      }
    },
    [],
  );

  const handleWorldFocusClickCapture = useCallback(
    (event: ReactMouseEvent<HTMLDivElement>) => {
      if (event.detail !== 0) {
        return;
      }

      const element = getActiveWorldButton(event.target);
      if (element !== null) {
        emitWorldFocusIntent(element);
      }
    },
    [emitWorldFocusIntent],
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
      const gap = Number.parseFloat(
        computed.getPropertyValue('--home-today-gap'),
      );
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
    layout.style.setProperty(
      '--timeline-week-home-offset',
      `${compactViewport ? 0 : ((metrics.railWidth + metrics.gap) * visible) / 2}px`,
    );

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
          <DayContextStrip preferredName={preferredName} />

          <div className="home-hero-body">
            <AISurface
              collapsed={isAiCollapsed}
              onToggleCollapsed={() => setIsAiCollapsed((value) => !value)}
            />

            <div
              className="home-upper-workspace"
              data-home-layout="upper-workspace"
              onPointerDownCapture={handleWorldFocusPointerDownCapture}
              onPointerUpCapture={handleWorldFocusPointerUpCapture}
              onPointerCancelCapture={handleWorldFocusPointerCancelCapture}
              onClickCapture={handleWorldFocusClickCapture}
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

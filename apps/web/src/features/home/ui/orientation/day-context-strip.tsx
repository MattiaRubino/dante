import { Temporal } from '@dante/time';
import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { useTranslation } from 'react-i18next';
import dayRibbonBackdropUrl from 'virtual:dante-day-ribbon-backdrop';

import {
  createDayContextSnapshot,
  createPrototypeWeeklyForecast,
  getBrowserTimeZone,
  getDayGreetingPeriod,
  normalizePreferredName,
  type DailyWeatherForecast,
} from '../../model/day-context';
import {
  createDayRouteGeometry,
  DAY_ROUTE_HEIGHT,
  DAY_ROUTE_ROAD_Y,
  DAY_ROUTE_SCENE_BOTTOM_Y,
  pointOnDayRoute,
} from './day-route-geometry';
import { useMinuteClock } from './use-minute-clock';
import './day-context-strip.css';

type DayContextStripProps = Readonly<{
  viewedDateIso?: string | undefined;
  preferredName?: string | undefined;
}>;

type RouteStyle = CSSProperties & {
  '--day-route-x'?: string;
};

const DEFAULT_ROUTE_WIDTH = 900;
const WALKER_SCALE = 2;
const WALKER_FRAME_MS = 420;
const RIBBON_ANIMATION_MS = 7600;
const MASCOT_IDLE_AMPLITUDE = 1.6;
const MASCOT_IDLE_MS = 2100;
const WALKER_COLORS = {
  '1': '#335d28',
  '2': '#b7f05a',
  '3': '#17310c',
} as const;
const WALKER_FRAMES = [
  [
    '..1..1..',
    '.122221.',
    '12222221',
    '12322321',
    '12222221',
    '12233221',
    '.122221.',
    '..1..1..',
    '.11...11',
  ],
  [
    '..1..1..',
    '.122221.',
    '12222221',
    '12322321',
    '12222221',
    '12233221',
    '.122221.',
    '..1..1..',
    '..11.11.',
  ],
] as const;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function resolveLocale(language: string | undefined): string {
  return language?.toLowerCase().startsWith('en') ? 'en-US' : 'it-IT';
}

function capitalize(value: string, locale: string): string {
  return value.length > 0
    ? value[0]!.toLocaleUpperCase(locale) + value.slice(1)
    : value;
}

function formatTime(now: Temporal.ZonedDateTime): string {
  return `${String(now.hour).padStart(2, '0')}:${String(now.minute).padStart(2, '0')}`;
}

function formatLongDate(date: Temporal.PlainDate, locale: string): string {
  return capitalize(
    date.toLocaleString(locale, {
      weekday: 'long',
      day: 'numeric',
      month: 'long',
    }),
    locale,
  );
}

function formatWeekday(date: Temporal.PlainDate, locale: string): string {
  return date.toLocaleString(locale, { weekday: 'short' });
}

function formatOrientationDay(
  date: Temporal.PlainDate,
  relation: 'past' | 'today' | 'future',
  locale: string,
  todayLabel: string,
): string {
  const label = formatLongDate(date, locale);
  return relation === 'today' ? `${todayLabel} · ${label}` : label;
}

function WeatherGlyph({ condition }: Pick<DailyWeatherForecast, 'condition'>) {
  return (
    <span
      className={`day-context-weather-glyph day-context-weather-glyph--${condition}`}
      aria-hidden="true"
    >
      <span />
    </span>
  );
}

function OrientationWeatherMark({
  gradientId,
}: Readonly<{ gradientId: string }>) {
  const haloId = `${gradientId}-halo`;

  return (
    <span className="day-context-orientation-weather" aria-hidden="true">
      <svg viewBox="0 0 32 32">
        <defs>
          <radialGradient id={haloId} cx="50%" cy="50%" r="50%">
            <stop offset="0" stopColor="#ffd67a" stopOpacity=".32" />
            <stop offset=".58" stopColor="#ffbd62" stopOpacity=".08" />
            <stop offset="1" stopColor="#ffad54" stopOpacity="0" />
          </radialGradient>
          <radialGradient id={gradientId} cx="34%" cy="28%" r="72%">
            <stop offset="0" stopColor="#fff8d8" />
            <stop offset=".36" stopColor="#ffe18a" />
            <stop offset=".72" stopColor="#ffc45e" />
            <stop offset="1" stopColor="#e98f39" />
          </radialGradient>
        </defs>
        <circle cx="16" cy="16" r="12.5" fill={`url(#${haloId})`} />
        <g
          fill="none"
          stroke="#ffd98a"
          strokeWidth="1.25"
          strokeLinecap="round"
          opacity=".7"
        >
          <path d="M16 3.6v2.8M16 25.6v2.8M3.6 16h2.8M25.6 16h2.8M7.35 7.35l1.95 1.95M22.7 22.7l1.95 1.95M24.65 7.35L22.7 9.3M9.3 22.7l-1.95 1.95" />
        </g>
        <circle cx="16" cy="16" r="6.9" fill={`url(#${gradientId})`} />
        <circle cx="13.8" cy="13.5" r="1.5" fill="#fffbe9" opacity=".58" />
      </svg>
    </span>
  );
}

function useElementWidth<T extends HTMLElement>(fallback: number) {
  const ref = useRef<T | null>(null);
  const [width, setWidth] = useState(fallback);

  useEffect(() => {
    const element = ref.current;
    if (!element) {
      return;
    }

    const applyWidth = (nextWidth: number) => {
      if (Number.isFinite(nextWidth) && nextWidth > 0) {
        setWidth((current) =>
          Math.abs(current - nextWidth) < 0.5 ? current : nextWidth,
        );
      }
    };

    if (typeof ResizeObserver !== 'function') {
      const initialFrame = window.requestAnimationFrame(() =>
        applyWidth(element.getBoundingClientRect().width),
      );
      const onResize = () => applyWidth(element.getBoundingClientRect().width);
      window.addEventListener('resize', onResize);
      return () => {
        window.cancelAnimationFrame(initialFrame);
        window.removeEventListener('resize', onResize);
      };
    }

    const observer = new ResizeObserver((entries) => {
      const nextWidth = entries[0]?.contentRect.width;
      if (nextWidth !== undefined) {
        applyWidth(nextWidth);
      }
    });
    observer.observe(element);
    return () => observer.disconnect();
  }, []);

  return [ref, width] as const;
}

function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = useState(() =>
    typeof window === 'undefined'
      ? false
      : window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  );

  useEffect(() => {
    const media = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = () => setReducedMotion(media.matches);
    media.addEventListener('change', onChange);
    return () => media.removeEventListener('change', onChange);
  }, []);

  return reducedMotion;
}

function DayRibbon({
  progress,
  nowLabel,
}: Readonly<{
  progress: number | null;
  nowLabel: string;
}>) {
  const visualId = useId().replace(/:/g, '');
  const reducedMotion = useReducedMotion();
  const [routeRef, routeWidth] = useElementWidth<HTMLDivElement>(
    DEFAULT_ROUTE_WIDTH,
  );
  const geometry = useMemo(
    () => createDayRouteGeometry(routeWidth),
    [routeWidth],
  );
  const pulseGradientRef = useRef<SVGLinearGradientElement | null>(null);
  const walkerRef = useRef<SVGGElement | null>(null);
  const frameRefs = useRef<Array<SVGGElement | null>>([]);
  const nowPoint =
    progress === null ? null : pointOnDayRoute(progress, routeWidth);
  const sceneNowX = nowPoint?.x ?? 0;
  const spriteWidth = WALKER_FRAMES[0][0].length * WALKER_SCALE;
  const spriteHeight = WALKER_FRAMES[0].length * WALKER_SCALE;
  const walkerX = clamp(
    sceneNowX - spriteWidth / 2,
    0,
    Math.max(0, geometry.width - spriteWidth),
  );
  const walkerBaseY = DAY_ROUTE_ROAD_Y - spriteHeight + 2;
  const roadPath = `M10.00,${DAY_ROUTE_ROAD_Y.toFixed(2)} L${Math.max(
    10,
    geometry.width - 10,
  ).toFixed(2)},${DAY_ROUTE_ROAD_Y.toFixed(2)}`;
  const roadFillPath = `${roadPath} L${Math.max(
    10,
    geometry.width - 10,
  ).toFixed(2)},${DAY_ROUTE_HEIGHT.toFixed(2)} L10,${DAY_ROUTE_HEIGHT.toFixed(2)} Z`;
  const routeStyle: RouteStyle = {
    '--day-route-x': `${(progress ?? 0) * 100}%`,
  };

  useEffect(() => {
    const walker = walkerRef.current;
    if (!walker || progress === null) {
      return;
    }

    let raf = 0;
    let startTimestamp: number | null = null;
    let visibleFrame = -1;

    const setFrame = (index: number) => {
      if (visibleFrame === index) {
        return;
      }
      visibleFrame = index;
      frameRefs.current.forEach((frame, frameIndex) => {
        frame?.setAttribute('display', frameIndex === index ? 'inline' : 'none');
      });
    };

    const setStaticWalker = () => {
      walker.setAttribute(
        'transform',
        `translate(${walkerX.toFixed(2)},${walkerBaseY.toFixed(2)})`,
      );
      setFrame(0);
    };

    if (reducedMotion) {
      setStaticWalker();
      return;
    }

    const animate = (timestamp: number) => {
      startTimestamp ??= timestamp;
      const elapsed = timestamp - startTimestamp;
      const bob =
        Math.sin(
          ((timestamp % MASCOT_IDLE_MS) / MASCOT_IDLE_MS) * Math.PI * 2,
        ) * MASCOT_IDLE_AMPLITUDE;
      walker.setAttribute(
        'transform',
        `translate(${walkerX.toFixed(2)},${(walkerBaseY + bob).toFixed(2)})`,
      );
      setFrame(Math.floor(elapsed / WALKER_FRAME_MS) % WALKER_FRAMES.length);

      const gradient = pulseGradientRef.current;
      if (gradient) {
        const p = (elapsed % RIBBON_ANIMATION_MS) / RIBBON_ANIMATION_MS;
        const span = Math.max(240, geometry.width * 0.62);
        const center = -span * 0.35 + p * (geometry.width + span * 0.7);
        gradient.setAttribute('x1', (center - span / 2).toFixed(2));
        gradient.setAttribute('x2', (center + span / 2).toFixed(2));
        gradient.setAttribute('y1', '0');
        gradient.setAttribute('y2', '0');
      }

      raf = window.requestAnimationFrame(animate);
    };

    raf = window.requestAnimationFrame(animate);
    return () => window.cancelAnimationFrame(raf);
  }, [geometry.width, progress, reducedMotion, walkerBaseY, walkerX]);

  return (
    <div
      ref={routeRef}
      className="home-day-route day-context-route"
      style={routeStyle}
      aria-label="Percorso della giornata"
    >
      <svg
        className="day-ribbon-svg"
        viewBox={geometry.viewBox}
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id={`${visualId}-wave`} x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#9c77ff" />
            <stop offset="23%" stopColor="#ff997f" />
            <stop offset="49%" stopColor="#ffe498" />
            <stop offset="77%" stopColor="#86d6ff" />
            <stop offset="100%" stopColor="#aa89ff" />
          </linearGradient>
          <linearGradient
            id={`${visualId}-road`}
            gradientUnits="userSpaceOnUse"
            x1="0"
            y1="0"
            x2={geometry.width}
            y2="0"
          >
            <stop offset="0%" stopColor="#7a68df" />
            <stop offset="40%" stopColor="#ffbc62" />
            <stop offset="60%" stopColor="#ffd86f" />
            <stop offset="85%" stopColor="#65c8ff" />
            <stop offset="100%" stopColor="#9579ef" />
          </linearGradient>
          <linearGradient
            ref={pulseGradientRef}
            id={`${visualId}-pulse`}
            gradientUnits="userSpaceOnUse"
            x1="-300"
            y1="0"
            x2="0"
            y2="0"
          >
            <stop offset="0%" stopColor="#fff8df" stopOpacity="0" />
            <stop offset="42%" stopColor="#fff8df" stopOpacity="0" />
            <stop offset="47%" stopColor="#fff8df" stopOpacity=".08" />
            <stop offset="50%" stopColor="#fff8df" stopOpacity=".92" />
            <stop offset="53%" stopColor="#fff8df" stopOpacity=".08" />
            <stop offset="58%" stopColor="#fff8df" stopOpacity="0" />
            <stop offset="100%" stopColor="#fff8df" stopOpacity="0" />
          </linearGradient>
          <filter
            id={`${visualId}-glow`}
            x="-20%"
            y="-100%"
            width="140%"
            height="300%"
          >
            <feGaussianBlur stdDeviation="3.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <linearGradient
            id={`${visualId}-mask-gradient`}
            x1="0"
            y1="0"
            x2="1"
            y2="0"
          >
            <stop offset="0%" stopColor="#fff" stopOpacity="0" />
            <stop offset="4%" stopColor="#fff" stopOpacity="1" />
            <stop offset="96%" stopColor="#fff" stopOpacity="1" />
            <stop offset="100%" stopColor="#fff" stopOpacity="0" />
          </linearGradient>
          <mask id={`${visualId}-mask`}>
            <rect
              x="0"
              y="0"
              width={geometry.width}
              height={geometry.height}
              fill={`url(#${visualId}-mask-gradient)`}
            />
          </mask>
        </defs>

        <g mask={`url(#${visualId}-mask)`}>
          <image
            href={dayRibbonBackdropUrl}
            x="0"
            y="-2"
            width={geometry.width}
            height={DAY_ROUTE_SCENE_BOTTOM_Y + 4}
            preserveAspectRatio="none"
          />
          <rect
            x="0"
            y="0"
            width={geometry.width}
            height={DAY_ROUTE_SCENE_BOTTOM_Y}
            fill="rgba(4,8,18,.012)"
          />
          <rect
            x="0"
            y={DAY_ROUTE_SCENE_BOTTOM_Y}
            width={geometry.width}
            height={Math.max(
              0,
              DAY_ROUTE_ROAD_Y - DAY_ROUTE_SCENE_BOTTOM_Y - 1,
            )}
            fill="rgba(4,8,18,.015)"
          />

          <path d={roadFillPath} fill="rgba(0,0,0,0)" stroke="none" />
          <path
            d={roadPath}
            fill="none"
            stroke={`url(#${visualId}-road)`}
            strokeWidth="4.2"
            strokeLinecap="round"
            opacity=".52"
            filter={`url(#${visualId}-glow)`}
          />
          <path
            d={roadPath}
            fill="none"
            stroke={`url(#${visualId}-road)`}
            strokeWidth="1.8"
            strokeLinecap="round"
          />

          <path
            d={geometry.path}
            fill="none"
            stroke={`url(#${visualId}-wave)`}
            strokeWidth="7.5"
            strokeLinecap="round"
            opacity=".26"
            filter={`url(#${visualId}-glow)`}
          />
          <path
            d={geometry.path}
            fill="none"
            stroke={`url(#${visualId}-wave)`}
            strokeWidth="2.25"
            strokeLinecap="round"
          />

          {!reducedMotion ? (
            <>
              <path
                d={geometry.path}
                fill="none"
                stroke={`url(#${visualId}-pulse)`}
                strokeWidth="7.2"
                strokeLinecap="round"
                opacity=".36"
                filter={`url(#${visualId}-glow)`}
              />
              <path
                d={geometry.path}
                fill="none"
                stroke={`url(#${visualId}-pulse)`}
                strokeWidth="2.8"
                strokeLinecap="round"
                opacity=".82"
              />
            </>
          ) : null}

          {nowPoint ? (
            <>
              <line
                x1={nowPoint.x}
                x2={nowPoint.x}
                y1={nowPoint.y}
                y2={DAY_ROUTE_ROAD_Y}
                stroke="rgba(255,234,164,.26)"
                strokeWidth="5"
                filter={`url(#${visualId}-glow)`}
              />
              <line
                x1={nowPoint.x}
                x2={nowPoint.x}
                y1={nowPoint.y}
                y2={DAY_ROUTE_ROAD_Y}
                stroke="rgba(255,243,188,.86)"
                strokeWidth="1.1"
              />
              <circle
                cx={nowPoint.x}
                cy={nowPoint.y}
                r="7.8"
                fill="rgba(255,223,117,.20)"
                filter={`url(#${visualId}-glow)`}
              />
              <circle
                cx={nowPoint.x}
                cy={nowPoint.y}
                r="4.5"
                fill="#ffd95a"
                stroke="#fff1b7"
                strokeWidth="1.2"
              />
              <g
                ref={walkerRef}
                className="day-context-pixel-walker"
                transform={`translate(${walkerX.toFixed(2)},${walkerBaseY.toFixed(2)})`}
              >
                {WALKER_FRAMES.map((frame, frameIndex) => (
                  <g
                    key={frameIndex}
                    ref={(node) => {
                      frameRefs.current[frameIndex] = node;
                    }}
                    display={frameIndex === 0 ? 'inline' : 'none'}
                  >
                    {frame.flatMap((row, y) =>
                      [...row].map((pixel, x) => {
                        if (pixel === '.') {
                          return null;
                        }
                        const color =
                          WALKER_COLORS[pixel as keyof typeof WALKER_COLORS];
                        return (
                          <rect
                            key={`${x}-${y}`}
                            x={x * WALKER_SCALE}
                            y={y * WALKER_SCALE}
                            width={WALKER_SCALE}
                            height={WALKER_SCALE}
                            fill={color}
                          />
                        );
                      }),
                    )}
                  </g>
                ))}
              </g>
            </>
          ) : null}
        </g>
      </svg>

      {nowPoint ? (
        <span className="home-day-now day-context-now">{nowLabel}</span>
      ) : null}
    </div>
  );
}

export function DayContextStrip({
  viewedDateIso,
  preferredName,
}: DayContextStripProps) {
  const { t, i18n } = useTranslation('common');
  const locale = resolveLocale(i18n.resolvedLanguage);
  const timeZone = useMemo(() => getBrowserTimeZone(), []);
  const now = useMinuteClock(timeZone);
  const snapshot = useMemo(
    () => createDayContextSnapshot(viewedDateIso, now),
    [now, viewedDateIso],
  );
  const forecast = createPrototypeWeeklyForecast(snapshot.viewedDate);
  const triggerForecast = forecast.days[0];
  const [selectedWeatherDate, setSelectedWeatherDate] = useState<string | null>(
    null,
  );
  const selectedForecast =
    forecast.days.find((day) => day.date.toString() === selectedWeatherDate) ??
    triggerForecast;
  const panelId = useId();
  const weatherGradientId = `${useId().replace(/:/g, '')}-orientation-sun`;
  const disclosureRef = useRef<HTMLDivElement | null>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const [isForecastOpen, setIsForecastOpen] = useState(false);

  useEffect(() => {
    if (!isForecastOpen) {
      return;
    }

    const onPointerDown = (event: PointerEvent) => {
      const target = event.target;
      if (target instanceof Node && !disclosureRef.current?.contains(target)) {
        setIsForecastOpen(false);
      }
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsForecastOpen(false);
        triggerRef.current?.focus();
      }
    };

    document.addEventListener('pointerdown', onPointerDown);
    document.addEventListener('keydown', onKeyDown);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown);
      document.removeEventListener('keydown', onKeyDown);
    };
  }, [isForecastOpen]);

  if (!triggerForecast || !selectedForecast) {
    return null;
  }

  const greetingPeriod = getDayGreetingPeriod(now.hour);
  const greetingLabel =
    greetingPeriod === 'morning'
      ? t(($) => $.common.home.orientation.greetings.morning)
      : greetingPeriod === 'afternoon'
        ? t(($) => $.common.home.orientation.greetings.afternoon)
        : greetingPeriod === 'evening'
          ? t(($) => $.common.home.orientation.greetings.evening)
          : t(($) => $.common.home.orientation.greetings.night);
  const displayName = normalizePreferredName(preferredName);
  const greetingAccessibleLabel = displayName
    ? `${greetingLabel}, ${displayName}.`
    : `${greetingLabel}.`;
  const dayTitle = formatOrientationDay(
    snapshot.viewedDate,
    snapshot.relation,
    locale,
    t(($) => $.common.home.orientation.dayKicker),
  );
  const nowLabel = formatTime(now);
  const longGreeting = greetingPeriod === 'afternoon' || (displayName?.length ?? 0) > 12;

  return (
    <section
      className="home-day-strip day-context-strip"
      aria-label="Orientamento Home"
    >
      <div className="home-day-greeting day-context-greeting">
        <h2
          className={longGreeting ? 'is-long-greeting' : undefined}
          aria-label={greetingAccessibleLabel}
        >
          <span className="day-context-greeting-salutation">
            {displayName ? `${greetingLabel},` : `${greetingLabel}.`}
          </span>
          {displayName ? (
            <>
              {' '}
              <span className="day-context-greeting-name">{displayName}</span>
              <span className="day-context-greeting-punctuation">.</span>
            </>
          ) : null}
        </h2>
      </div>

      <div className="day-context-disclosure" ref={disclosureRef}>
        <button
          ref={triggerRef}
          type="button"
          className="home-day-meta day-context-trigger"
          aria-expanded={isForecastOpen}
          aria-controls={panelId}
          onClick={() => setIsForecastOpen((open) => !open)}
        >
          <OrientationWeatherMark gradientId={weatherGradientId} />
          <span className="day-context-trigger-copy">
            <strong>{dayTitle}</strong>
            <span>
              Alba {triggerForecast.sunrise} · Tramonto {triggerForecast.sunset}
            </span>
          </span>
        </button>

        {isForecastOpen ? (
          <section
            id={panelId}
            className="day-context-panel"
            role="region"
            aria-label="Meteo della settimana"
          >
            <header className="day-context-panel-header">
              <div>
                <small>METEO · ANTEPRIMA FRONTEND</small>
                <strong>{formatLongDate(selectedForecast.date, locale)}</strong>
              </div>
              <button
                type="button"
                className="day-context-panel-close"
                aria-label="Chiudi meteo"
                onClick={() => {
                  setIsForecastOpen(false);
                  triggerRef.current?.focus();
                }}
              >
                ×
              </button>
            </header>

            <div className="day-context-weather-hero">
              <div className="day-context-weather-hero-temperature">
                <WeatherGlyph condition={selectedForecast.condition} />
                <strong>{selectedForecast.highCelsius}°</strong>
                <span>{selectedForecast.lowCelsius}°</span>
              </div>
              <div className="day-context-weather-hero-details">
                <span>{selectedForecast.conditionLabel}</span>
                <span>
                  Precipitazioni: {selectedForecast.precipitationPercent}%
                </span>
                <span>
                  Alba {selectedForecast.sunrise} · Tramonto{' '}
                  {selectedForecast.sunset}
                </span>
              </div>
              <div className="day-context-weather-hero-title">
                <strong>Meteo</strong>
                <span>{formatLongDate(selectedForecast.date, locale)}</span>
                <span>{selectedForecast.conditionLabel}</span>
              </div>
            </div>

            <ul
              className="day-context-week"
              aria-label="Previsioni per sette giorni"
            >
              {forecast.days.map((day) => {
                const dateKey = day.date.toString();
                const isSelected =
                  dateKey === selectedForecast.date.toString();

                return (
                  <li key={dateKey}>
                    <button
                      type="button"
                      className="day-context-forecast-day"
                      data-selected={isSelected ? 'true' : 'false'}
                      aria-current={isSelected ? 'date' : undefined}
                      onClick={() => setSelectedWeatherDate(dateKey)}
                      aria-label={`${formatLongDate(day.date, locale)}, ${day.conditionLabel}, massima ${day.highCelsius} gradi, minima ${day.lowCelsius} gradi, precipitazioni ${day.precipitationPercent} percento`}
                    >
                      <span>{formatWeekday(day.date, locale)}</span>
                      <WeatherGlyph condition={day.condition} />
                      <span className="day-context-forecast-temperatures">
                        <strong>{day.highCelsius}°</strong>
                        <small>{day.lowCelsius}°</small>
                      </span>
                      <em>{day.precipitationPercent}%</em>
                    </button>
                  </li>
                );
              })}
            </ul>

            <footer className="day-context-source">
              Dati demo · provider meteo non collegato
            </footer>
          </section>
        ) : null}
      </div>

      <DayRibbon progress={snapshot.progress} nowLabel={nowLabel} />
    </section>
  );
}

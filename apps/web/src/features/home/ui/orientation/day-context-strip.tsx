import { Temporal } from '@dante/time';
import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';

import {
  createDayContextSnapshot,
  createPrototypeWeeklyForecast,
  getBrowserTimeZone,
  type DailyWeatherForecast,
} from '../../model/day-context';
import {
  createDayRouteGeometry,
  DAY_ROUTE_HEIGHT,
  DAY_ROUTE_ROAD_Y,
  DAY_ROUTE_SCENE_BOTTOM_Y,
  minuteToProgress,
  pointOnDayRoute,
} from './day-route-geometry';
import { useMinuteClock } from './use-minute-clock';
import './day-context-strip.css';

type RouteStyle = CSSProperties & {
  '--day-route-x'?: string;
};

const DEFAULT_ROUTE_WIDTH = 900;
const WALKER_SCALE = 2;
const WALKER_FRAME = ['..G..', '.GGG.', 'GGGGG', '.G.G.', 'G...G'] as const;
const ROUTE_STARS = [
  [0.05, 10, 0.75],
  [0.13, 19, 0.4],
  [0.23, 8, 0.58],
  [0.36, 17, 0.34],
  [0.49, 7, 0.72],
  [0.68, 13, 0.42],
  [0.82, 8, 0.66],
  [0.94, 18, 0.38],
] as const;

function formatTime(now: Temporal.ZonedDateTime): string {
  return `${String(now.hour).padStart(2, '0')}:${String(now.minute).padStart(2, '0')}`;
}

function formatDayLabel(date: Temporal.PlainDate, locale: string): string {
  return date.toLocaleString(locale, {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
  });
}

function formatWeekday(date: Temporal.PlainDate, locale: string): string {
  return date.toLocaleString(locale, { weekday: 'short' });
}

function formatLongDate(date: Temporal.PlainDate, locale: string): string {
  return date.toLocaleString(locale, {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });
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

function useElementWidth<T extends HTMLElement>(fallback: number) {
  const ref = useRef<T | null>(null);
  const [width, setWidth] = useState(fallback);

  useEffect(() => {
    const element = ref.current;
    if (!element) {
      return;
    }

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      const nextWidth = entry?.contentRect.width;
      if (nextWidth !== undefined && Number.isFinite(nextWidth) && nextWidth > 0) {
        setWidth(nextWidth);
      }
    });
    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return [ref, width] as const;
}

export function DayContextStrip() {
  const locale = typeof navigator === 'undefined' ? 'it-IT' : navigator.language;
  const timeZone = useMemo(() => getBrowserTimeZone(), []);
  const now = useMinuteClock(timeZone);
  const snapshot = useMemo(
    () => createDayContextSnapshot(undefined, now),
    [now],
  );
  const forecast = useMemo(
    () => createPrototypeWeeklyForecast(snapshot.today),
    [snapshot.today],
  );
  const todayForecast = forecast.days[0];
  const [selectedWeatherDate, setSelectedWeatherDate] = useState<string | null>(null);
  const selectedForecast =
    forecast.days.find((day) => day.date.toString() === selectedWeatherDate) ??
    todayForecast;
  const panelId = useId();
  const visualId = useId().replace(/:/g, '');
  const disclosureRef = useRef<HTMLDivElement | null>(null);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const [isForecastOpen, setIsForecastOpen] = useState(false);
  const [routeRef, routeWidth] = useElementWidth<HTMLDivElement>(
    DEFAULT_ROUTE_WIDTH,
  );
  const geometry = useMemo(
    () => createDayRouteGeometry(routeWidth),
    [routeWidth],
  );
  const nowPoint =
    snapshot.progress === null
      ? null
      : pointOnDayRoute(snapshot.progress, routeWidth);

  useEffect(() => {
    if (!isForecastOpen) {
      return;
    }

    const onPointerDown = (event: PointerEvent) => {
      const target = event.target;
      if (
        target instanceof Node &&
        !disclosureRef.current?.contains(target)
      ) {
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

  if (!todayForecast || !selectedForecast) {
    return null;
  }

  const routeProgress = snapshot.progress ?? 0;
  const routeStyle: RouteStyle = {
    '--day-route-x': `${routeProgress * 100}%`,
  };
  const walkerWidth = WALKER_FRAME[0].length * WALKER_SCALE;
  const walkerHeight = WALKER_FRAME.length * WALKER_SCALE;
  const walkerX = Math.max(
    6,
    Math.min(
      geometry.width - walkerWidth - 6,
      routeProgress * geometry.width - walkerWidth / 2,
    ),
  );
  const walkerY = DAY_ROUTE_ROAD_Y - walkerHeight - 1;
  const mountainY = DAY_ROUTE_SCENE_BOTTOM_Y;

  return (
    <section
      className="home-day-strip day-context-strip"
      aria-label="Contesto della giornata"
    >
      <div className="home-day-greeting day-context-greeting">
        <small>Oggi</small>
        <strong>{formatLongDate(snapshot.today, locale)}</strong>
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
          <span className="home-day-weather">
            <WeatherGlyph condition={todayForecast.condition} />
          </span>
          <span className="day-context-trigger-copy">
            <small>Oggi · {formatDayLabel(snapshot.today, locale)}</small>
            <strong>
              {todayForecast.highCelsius}° / {todayForecast.lowCelsius}° · {formatTime(now)}
            </strong>
            <span>
              {todayForecast.conditionLabel} · ↑ {todayForecast.sunrise} · ↓{' '}
              {todayForecast.sunset}
            </span>
          </span>
          <span className="day-context-trigger-chevron" aria-hidden="true" />
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
                <span>Precipitazioni: {selectedForecast.precipitationPercent}%</span>
                <span>
                  Alba {selectedForecast.sunrise} · Tramonto {selectedForecast.sunset}
                </span>
              </div>
              <div className="day-context-weather-hero-title">
                <strong>Meteo</strong>
                <span>{formatLongDate(selectedForecast.date, locale)}</span>
                <span>{selectedForecast.conditionLabel}</span>
              </div>
            </div>

            <ul className="day-context-week" aria-label="Previsioni per sette giorni">
              {forecast.days.map((day) => {
                const dateKey = day.date.toString();
                const isSelected = dateKey === selectedForecast.date.toString();

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

      <div
        ref={routeRef}
        className="home-day-route day-context-route"
        style={routeStyle}
        aria-label={`Avanzamento della giornata: ${formatTime(now)}`}
      >
        <svg
          viewBox={geometry.viewBox}
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <defs>
            <linearGradient id={`${visualId}-sky`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#10122b" />
              <stop offset="24%" stopColor="#4a235f" />
              <stop offset="50%" stopColor="#de643c" />
              <stop offset="67%" stopColor="#315c9e" />
              <stop offset="100%" stopColor="#08142b" />
            </linearGradient>
            <linearGradient id={`${visualId}-route`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#b768ff" />
              <stop offset="31%" stopColor="#ff79a8" />
              <stop offset="55%" stopColor="#ffd45e" />
              <stop offset="76%" stopColor="#72e6ff" />
              <stop offset="100%" stopColor="#5f8cff" />
            </linearGradient>
            <radialGradient id={`${visualId}-sunset`} cx="50%" cy="58%" r="46%">
              <stop offset="0%" stopColor="#ffd879" stopOpacity="0.92" />
              <stop offset="35%" stopColor="#ff8659" stopOpacity="0.42" />
              <stop offset="100%" stopColor="#ff8659" stopOpacity="0" />
            </radialGradient>
            <linearGradient id={`${visualId}-road`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#a765ff" stopOpacity="0.56" />
              <stop offset="52%" stopColor="#ffcf65" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#58a9ff" stopOpacity="0.62" />
            </linearGradient>
            <linearGradient id={`${visualId}-fade`} x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="white" stopOpacity="0" />
              <stop offset="4%" stopColor="white" />
              <stop offset="96%" stopColor="white" />
              <stop offset="100%" stopColor="white" stopOpacity="0" />
            </linearGradient>
            <mask id={`${visualId}-mask`}>
              <rect width={geometry.width} height={geometry.height} fill={`url(#${visualId}-fade)`} />
            </mask>
          </defs>

          <g mask={`url(#${visualId}-mask)`} className="day-context-route-scene">
            <rect
              x="0"
              y="0"
              width={geometry.width}
              height={DAY_ROUTE_SCENE_BOTTOM_Y}
              fill={`url(#${visualId}-sky)`}
              opacity="0.5"
            />
            <rect
              x="0"
              y="0"
              width={geometry.width}
              height={DAY_ROUTE_SCENE_BOTTOM_Y}
              fill={`url(#${visualId}-sunset)`}
              opacity="0.85"
            />
            {ROUTE_STARS.map(([x, y, opacity]) => (
              <circle
                key={`${x}-${y}`}
                cx={geometry.width * x}
                cy={y}
                r="0.75"
                fill="#e7f2ff"
                opacity={opacity}
              />
            ))}
            <path
              d={`M 0 ${mountainY} L ${geometry.width * 0.12} ${mountainY - 6} L ${geometry.width * 0.2} ${mountainY - 2} L ${geometry.width * 0.32} ${mountainY - 11} L ${geometry.width * 0.43} ${mountainY - 4} L ${geometry.width * 0.55} ${mountainY - 15} L ${geometry.width * 0.66} ${mountainY - 4} L ${geometry.width * 0.78} ${mountainY - 9} L ${geometry.width * 0.9} ${mountainY - 3} L ${geometry.width} ${mountainY - 7} L ${geometry.width} ${mountainY + 2} L 0 ${mountainY + 2} Z`}
              className="day-context-route-mountains"
            />
            <circle
              cx={geometry.width * 0.55}
              cy={mountainY - 12}
              r="3.8"
              className="day-context-route-sun"
            />
          </g>

          <path
            className="day-context-route-wave-glow"
            d={geometry.path}
            stroke={`url(#${visualId}-route)`}
          />
          <path
            className="day-context-route-wave"
            d={geometry.path}
            stroke={`url(#${visualId}-route)`}
          />

          <line
            x1="10"
            y1={DAY_ROUTE_ROAD_Y}
            x2={Math.max(10, geometry.width - 10)}
            y2={DAY_ROUTE_ROAD_Y}
            className="day-context-route-road-shadow"
          />
          <line
            x1="10"
            y1={DAY_ROUTE_ROAD_Y}
            x2={Math.max(10, geometry.width - 10)}
            y2={DAY_ROUTE_ROAD_Y}
            className="day-context-route-road"
            stroke={`url(#${visualId}-road)`}
          />

          {nowPoint ? (
            <>
              <line
                x1={nowPoint.x}
                y1="9"
                x2={nowPoint.x}
                y2={DAY_ROUTE_ROAD_Y - 2}
                className="day-context-route-now-guide"
              />
              <g
                className="day-context-pixel-walker"
                transform={`translate(${walkerX.toFixed(2)} ${walkerY.toFixed(2)})`}
              >
                {WALKER_FRAME.flatMap((row, y) =>
                  [...row].map((pixel, x) =>
                    pixel === '.' ? null : (
                      <rect
                        key={`${x}-${y}`}
                        x={x * WALKER_SCALE}
                        y={y * WALKER_SCALE}
                        width={WALKER_SCALE}
                        height={WALKER_SCALE}
                        rx="0.3"
                      />
                    ),
                  ),
                )}
              </g>
            </>
          ) : null}
        </svg>

        {([todayForecast.sunrise, '12:00', todayForecast.sunset] as const).map(
          (time, index) => {
            const point = pointOnDayRoute(minuteToProgress(time), routeWidth);
            return (
              <span
                key={time}
                className="day-context-route-tick"
                style={{
                  left: `${(point.x / geometry.width) * 100}%`,
                  top: `${(point.y / DAY_ROUTE_HEIGHT) * 100}%`,
                }}
                aria-hidden="true"
              >
                {index === 0 ? '↑ ' : index === 2 ? '↓ ' : ''}
                {time}
              </span>
            );
          },
        )}

        {nowPoint ? (
          <span className="home-day-now day-context-now">{formatTime(now)}</span>
        ) : null}
      </div>
    </section>
  );
}

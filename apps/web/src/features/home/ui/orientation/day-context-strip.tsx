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
  minuteToProgress,
  pointOnDayRoute,
} from './day-route-geometry';
import { useMinuteClock } from './use-minute-clock';
import './day-context-strip.css';

type DayContextStripProps = Readonly<{
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
}>;

type RouteStyle = CSSProperties & {
  '--day-route-x'?: string;
  '--day-route-y'?: string;
  '--day-route-rotation'?: string;
};

const DEFAULT_ROUTE_WIDTH = 900;

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

    const update = (nextWidth: number) => {
      if (Number.isFinite(nextWidth) && nextWidth > 0) {
        setWidth(nextWidth);
      }
    };

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (entry) {
        update(entry.contentRect.width);
      }
    });
    observer.observe(element);

    return () => observer.disconnect();
  }, []);

  return [ref, width] as const;
}

export function DayContextStrip({
  viewedDateIso,
  onViewedDateChange,
}: DayContextStripProps) {
  const locale = typeof navigator === 'undefined' ? 'it-IT' : navigator.language;
  const timeZone = useMemo(() => getBrowserTimeZone(), []);
  const now = useMinuteClock(timeZone);
  const snapshot = useMemo(
    () => createDayContextSnapshot(viewedDateIso, now),
    [now, viewedDateIso],
  );
  const forecast = useMemo(
    () => createPrototypeWeeklyForecast(snapshot.viewedDate),
    [snapshot.viewedDate],
  );
  const selectedForecast = forecast.days[0];
  const panelId = useId();
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
  const nowPoint = useMemo(
    () =>
      snapshot.progress === null
        ? null
        : pointOnDayRoute(snapshot.progress, routeWidth),
    [routeWidth, snapshot.progress],
  );

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

  if (!selectedForecast) {
    return null;
  }

  const changeViewedDate = (date: Temporal.PlainDate) => {
    onViewedDateChange?.(
      Temporal.PlainDate.compare(date, snapshot.today) === 0
        ? undefined
        : date.toString(),
    );
  };
  const routeStyle: RouteStyle | undefined = nowPoint
    ? {
        '--day-route-x': `${(nowPoint.x / 1000) * 100}%`,
        '--day-route-y': `${(nowPoint.y / 74) * 100}%`,
        '--day-route-rotation': `${nowPoint.rotation.toFixed(2)}deg`,
      }
    : undefined;

  return (
    <section
      className="home-day-strip day-context-strip"
      aria-label="Contesto della giornata"
      data-day-relation={snapshot.relation}
    >
      <div className="home-day-greeting day-context-greeting">
        <small>{snapshot.relation === 'today' ? 'Oggi' : 'Giornata'}</small>
        <strong>{formatLongDate(snapshot.viewedDate, locale)}</strong>
      </div>

      <div className="day-context-disclosure" ref={disclosureRef}>
        <button
          ref={triggerRef}
          type="button"
          className="home-day-meta day-context-trigger"
          aria-expanded={isForecastOpen}
          aria-controls={panelId}
          aria-haspopup="dialog"
          onClick={() => setIsForecastOpen((open) => !open)}
        >
          <span className="home-day-weather">
            <WeatherGlyph condition={selectedForecast.condition} />
          </span>
          <span className="day-context-trigger-copy">
            <small>{formatDayLabel(snapshot.viewedDate, locale)}</small>
            <strong>
              {selectedForecast.highCelsius}° / {selectedForecast.lowCelsius}°
              {snapshot.relation === 'today' ? ` · ${formatTime(now)}` : ''}
            </strong>
            <span>
              {selectedForecast.conditionLabel} · ↑ {selectedForecast.sunrise} · ↓{' '}
              {selectedForecast.sunset}
            </span>
          </span>
          <span className="day-context-trigger-chevron" aria-hidden="true" />
        </button>

        {isForecastOpen ? (
          <div
            id={panelId}
            className="day-context-panel"
            role="dialog"
            aria-label="Meteo e selezione giorno"
          >
            <div className="day-context-panel-header">
              <div>
                <small>PREVISIONI · ANTEPRIMA FRONTEND</small>
                <strong>{formatLongDate(snapshot.viewedDate, locale)}</strong>
              </div>
              <button
                type="button"
                className="day-context-panel-close"
                aria-label="Chiudi previsioni"
                onClick={() => {
                  setIsForecastOpen(false);
                  triggerRef.current?.focus();
                }}
              >
                ×
              </button>
            </div>

            <div className="day-context-day-nav" aria-label="Cambia giorno">
              <button
                type="button"
                aria-label="Giorno precedente"
                onClick={() => changeViewedDate(snapshot.viewedDate.subtract({ days: 1 }))}
              >
                ←
              </button>
              <button
                type="button"
                className="day-context-today-button"
                disabled={snapshot.relation === 'today'}
                onClick={() => changeViewedDate(snapshot.today)}
              >
                Oggi
              </button>
              <button
                type="button"
                aria-label="Giorno successivo"
                onClick={() => changeViewedDate(snapshot.viewedDate.add({ days: 1 }))}
              >
                →
              </button>
            </div>

            <ul className="day-context-week" aria-label="Sette giorni">
              {forecast.days.map((day) => (
                <li key={day.date.toString()}>
                  <button
                    type="button"
                    className="day-context-forecast-day"
                    data-selected={
                      Temporal.PlainDate.compare(day.date, snapshot.viewedDate) === 0
                        ? 'true'
                        : 'false'
                    }
                    onClick={() => changeViewedDate(day.date)}
                    aria-label={`${formatLongDate(day.date, locale)}, ${day.conditionLabel}, massima ${day.highCelsius} gradi, minima ${day.lowCelsius} gradi`}
                  >
                    <span>{formatDayLabel(day.date, locale)}</span>
                    <WeatherGlyph condition={day.condition} />
                    <strong>{day.highCelsius}°</strong>
                    <small>{day.lowCelsius}°</small>
                    <em>{day.precipitationPercent}%</em>
                  </button>
                </li>
              ))}
            </ul>

            <div className="day-context-sun-row">
              <span>Alba <strong>{selectedForecast.sunrise}</strong></span>
              <span>Tramonto <strong>{selectedForecast.sunset}</strong></span>
              <span className="day-context-source">Dati demo: adapter meteo non collegato</span>
            </div>
          </div>
        ) : null}
      </div>

      <div
        ref={routeRef}
        className="home-day-route day-context-route"
        style={routeStyle}
        aria-label={
          snapshot.relation === 'today'
            ? `Avanzamento della giornata: ${formatTime(now)}`
            : snapshot.relation === 'past'
              ? 'Giornata passata'
              : 'Giornata futura'
        }
      >
        <svg
          viewBox={geometry.viewBox}
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <defs>
            <linearGradient id="day-context-route-gradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#5ad66f" />
              <stop offset="54%" stopColor="#b8ef5a" />
              <stop offset="100%" stopColor="#ffd25a" />
            </linearGradient>
          </defs>
          <path className="home-day-route-glow" d={geometry.path} />
          <path
            className="home-day-route-line day-context-route-line"
            d={geometry.path}
          />
        </svg>

        {([selectedForecast.sunrise, '12:00', selectedForecast.sunset] as const).map(
          (time, index) => {
            const point = pointOnDayRoute(minuteToProgress(time), routeWidth);
            return (
              <span
                key={time}
                className="day-context-route-tick"
                style={{
                  left: `${(point.x / 1000) * 100}%`,
                  top: `${(point.y / 74) * 100}%`,
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
          <>
            <span className="home-day-now day-context-now">{formatTime(now)}</span>
            <span className="home-day-marker day-context-marker" aria-hidden="true" />
            <span className="day-context-walker" aria-hidden="true">
              <span className="day-context-walker-head" />
              <span className="day-context-walker-body" />
              <span className="day-context-walker-leg day-context-walker-leg--a" />
              <span className="day-context-walker-leg day-context-walker-leg--b" />
            </span>
          </>
        ) : (
          <span className="day-context-route-state">
            {snapshot.relation === 'past' ? 'Completata' : 'In arrivo'}
          </span>
        )}
      </div>
    </section>
  );
}

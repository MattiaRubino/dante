import { Temporal } from '@dante/time';
import { useEffect, useId, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  createDayContextSnapshot,
  createPrototypeWeeklyForecast,
  getBrowserTimeZone,
  getDayGreetingPeriod,
  normalizePreferredName,
  type DailyWeatherForecast,
  type WeatherCondition,
} from '../../model/day-context';
import { DayRibbon } from './day-ribbon';
import { useMinuteClock } from './use-minute-clock';
import './day-context-strip.css';

type DayContextStripProps = Readonly<{
  preferredName?: string | undefined;
}>;

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

export function DayContextStrip({ preferredName }: DayContextStripProps) {
  const { t, i18n } = useTranslation('common');
  const locale = resolveLocale(i18n.resolvedLanguage);
  const timeZone = useMemo(() => getBrowserTimeZone(), []);
  const now = useMinuteClock(timeZone);
  const snapshot = useMemo(
    () => createDayContextSnapshot(undefined, now),
    [now],
  );
  const todayKey = snapshot.today.toString();
  const forecast = useMemo(
    () => createPrototypeWeeklyForecast(Temporal.PlainDate.from(todayKey)),
    [todayKey],
  );
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
  const dayTitle = `${t(($) => $.common.home.orientation.dayKicker)} · ${formatLongDate(
    snapshot.today,
    locale,
  )}`;
  const nowLabel = formatTime(now);
  const longGreeting =
    greetingPeriod === 'afternoon' || (displayName?.length ?? 0) > 12;

  const weatherLabel = (condition: WeatherCondition): string => {
    switch (condition) {
      case 'clear':
        return t(($) => $.common.home.orientation.dayContext.conditions.clear);
      case 'partly-cloudy':
        return t(($) =>
          $.common.home.orientation.dayContext.conditions.partlyCloudy,
        );
      case 'cloudy':
        return t(($) => $.common.home.orientation.dayContext.conditions.cloudy);
      case 'rain':
        return t(($) => $.common.home.orientation.dayContext.conditions.rain);
      case 'storm':
        return t(($) => $.common.home.orientation.dayContext.conditions.storm);
    }
  };

  const selectedConditionLabel = weatherLabel(selectedForecast.condition);

  return (
    <section
      className="home-day-strip day-context-strip"
      aria-label={t(($) => $.common.home.orientation.dayContext.regionLabel)}
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
              {t(($) => $.common.home.orientation.dayContext.sunrise)}{' '}
              {triggerForecast.sunrise} ·{' '}
              {t(($) => $.common.home.orientation.dayContext.sunset)}{' '}
              {triggerForecast.sunset}
            </span>
          </span>
        </button>

        {isForecastOpen ? (
          <section
            id={panelId}
            className="day-context-panel"
            role="region"
            aria-label={t(($) =>
              $.common.home.orientation.dayContext.weatherPanelLabel,
            )}
          >
            <header className="day-context-panel-header">
              <div>
                <small>
                  {t(($) => $.common.home.orientation.dayContext.weatherPreview)}
                </small>
                <strong>{formatLongDate(selectedForecast.date, locale)}</strong>
              </div>
              <button
                type="button"
                className="day-context-panel-close"
                aria-label={t(($) =>
                  $.common.home.orientation.dayContext.closeWeather,
                )}
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
                <span>{selectedConditionLabel}</span>
                <span>
                  {t(($) => $.common.home.orientation.dayContext.precipitation)}:{' '}
                  {selectedForecast.precipitationPercent}%
                </span>
                <span>
                  {t(($) => $.common.home.orientation.dayContext.sunrise)}{' '}
                  {selectedForecast.sunrise} ·{' '}
                  {t(($) => $.common.home.orientation.dayContext.sunset)}{' '}
                  {selectedForecast.sunset}
                </span>
              </div>
              <div className="day-context-weather-hero-title">
                <strong>
                  {t(($) => $.common.home.orientation.dayContext.weatherTitle)}
                </strong>
                <span>{formatLongDate(selectedForecast.date, locale)}</span>
                <span>{selectedConditionLabel}</span>
              </div>
            </div>

            <ul
              className="day-context-week"
              aria-label={t(($) =>
                $.common.home.orientation.dayContext.sevenDayForecast,
              )}
            >
              {forecast.days.map((day) => {
                const dateKey = day.date.toString();
                const isSelected =
                  dateKey === selectedForecast.date.toString();
                const conditionLabel = weatherLabel(day.condition);
                const forecastAriaLabel = [
                  formatLongDate(day.date, locale),
                  conditionLabel,
                  `${t(($) => $.common.home.orientation.dayContext.maximum)} ${day.highCelsius} ${t(($) => $.common.home.orientation.dayContext.degrees)}`,
                  `${t(($) => $.common.home.orientation.dayContext.minimum)} ${day.lowCelsius} ${t(($) => $.common.home.orientation.dayContext.degrees)}`,
                  `${t(($) => $.common.home.orientation.dayContext.precipitation)} ${day.precipitationPercent} ${t(($) => $.common.home.orientation.dayContext.percent)}`,
                ].join(', ');

                return (
                  <li key={dateKey}>
                    <button
                      type="button"
                      className="day-context-forecast-day"
                      data-selected={isSelected ? 'true' : 'false'}
                      aria-current={isSelected ? 'date' : undefined}
                      onClick={() => setSelectedWeatherDate(dateKey)}
                      aria-label={forecastAriaLabel}
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
              {t(($) => $.common.home.orientation.dayContext.sourceDemo)}
            </footer>
          </section>
        ) : null}
      </div>

      <DayRibbon
        progress={snapshot.progress}
        nowLabel={nowLabel}
        routeLabel={t(($) => $.common.home.orientation.dayContext.routeLabel)}
      />
    </section>
  );
}

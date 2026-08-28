import { useTranslation } from 'react-i18next';

export function DayContextStrip() {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-day-strip"
      data-home-region="day-strip"
      aria-label={t(($) => $.common.home.orientation.dayTitle)}
    >
      <div className="home-day-greeting">
        <strong>{t(($) => $.common.home.orientation.greeting)}</strong>
      </div>

      <div className="home-day-meta">
        <span className="home-day-weather" aria-hidden="true">
          <span />
        </span>
        <span>
          <small>{t(($) => $.common.home.orientation.dayKicker)}</small>
          <strong>{t(($) => $.common.home.orientation.dayTitle)}</strong>
          <span>{t(($) => $.common.home.orientation.dayMeta)}</span>
        </span>
      </div>

      <div className="home-day-route" aria-hidden="true">
        <svg viewBox="0 0 720 74" preserveAspectRatio="none">
          <defs>
            <linearGradient id="home-day-route-gradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="currentColor" stopOpacity="0.08" />
              <stop offset="0.42" stopColor="currentColor" stopOpacity="0.75" />
              <stop offset="0.68" stopColor="currentColor" stopOpacity="0.42" />
              <stop offset="1" stopColor="currentColor" stopOpacity="0.1" />
            </linearGradient>
          </defs>
          <path
            className="home-day-route-glow"
            d="M0 47 C74 12, 130 62, 208 36 S344 13, 424 38 S558 62, 720 28"
          />
          <path
            className="home-day-route-line"
            d="M0 47 C74 12, 130 62, 208 36 S344 13, 424 38 S558 62, 720 28"
            stroke="url(#home-day-route-gradient)"
          />
        </svg>
        <span className="home-day-now">15:00</span>
        <span className="home-day-marker" />
      </div>
    </section>
  );
}

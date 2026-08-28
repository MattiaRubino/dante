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
          <svg viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="3.5" />
            <path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M18.5 5.5l-1.7 1.7M7.2 16.8l-1.7 1.7" />
          </svg>
        </span>
        <span>
          <small>{t(($) => $.common.home.orientation.dayKicker)}</small>
          <strong>Venerdì 28 agosto</strong>
          <span>Alba 06:17 · Tramonto 19:34</span>
        </span>
      </div>

      <div className="home-day-route" aria-hidden="true">
        <svg viewBox="0 0 760 78" preserveAspectRatio="none">
          <defs>
            <linearGradient id="home-day-road-gradient" gradientUnits="userSpaceOnUse" x1="0%" y1="0" x2="100%" y2="0">
              <stop offset="0%" stopColor="#69767b" stopOpacity=".22" />
              <stop offset="36%" stopColor="#EA5C12" stopOpacity=".55" />
              <stop offset="62%" stopColor="#F0A06F" stopOpacity=".92" />
              <stop offset="100%" stopColor="#69767b" stopOpacity=".2" />
            </linearGradient>
            <linearGradient id="home-day-sky-gradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0" stopColor="#7498b2" stopOpacity=".06" />
              <stop offset=".52" stopColor="#EA5C12" stopOpacity=".13" />
              <stop offset="1" stopColor="#2a3840" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            className="home-day-route-sky"
            d="M0 62 C112 60 170 38 252 32 C340 25 397 15 474 20 C552 24 616 43 760 56 L760 78 L0 78 Z"
            fill="url(#home-day-sky-gradient)"
          />
          <path
            className="home-day-route-road-glow"
            d="M0 63 C112 61 170 39 252 33 C340 26 397 16 474 21 C552 25 616 44 760 57"
          />
          <path
            className="home-day-route-road"
            d="M0 63 C112 61 170 39 252 33 C340 26 397 16 474 21 C552 25 616 44 760 57"
            stroke="url(#home-day-road-gradient)"
          />
          <circle className="home-day-route-sunrise" cx="96" cy="58" r="3.2" />
          <circle className="home-day-route-sunset" cx="690" cy="50" r="3.2" />
        </svg>
        <span className="home-day-route-label home-day-route-label-start">06:17</span>
        <span className="home-day-route-label home-day-route-label-end">19:34</span>
        <span className="home-day-now">15:00</span>
        <span className="home-day-marker" />
      </div>
    </section>
  );
}

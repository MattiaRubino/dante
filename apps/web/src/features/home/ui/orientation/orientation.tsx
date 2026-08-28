import { useTranslation } from 'react-i18next';

export function Orientation() {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-orientation"
      data-home-region="orientation"
      aria-label={t(($) => $.common.home.orientation.title)}
    >
      <h1 className="home-visually-hidden">
        {t(($) => $.common.home.orientation.title)}
      </h1>

      <article
        className="home-orientation-now"
        data-home-orientation="now-next"
      >
        <div className="home-orientation-kicker-row">
          <span>{t(($) => $.common.home.orientation.nowNext)}</span>
          <span className="home-orientation-status-dot" aria-hidden="true" />
        </div>
        <strong>14:57</strong>
        <p>Studio · grammatica avanzata</p>
        <div className="home-orientation-progress" aria-hidden="true">
          <span />
        </div>
        <footer>
          <span>fino alle 15:00</span>
          <span>15:15 · Ideazione concept</span>
        </footer>
      </article>

      <article
        className="home-orientation-highlight"
        data-home-orientation="highlight"
      >
        <div className="home-orientation-kicker-row">
          <span>{t(($) => $.common.home.orientation.highlight)}</span>
          <span className="home-orientation-badge">3 aperte</span>
        </div>
        <strong>Revisione concept</strong>
        <p>Tre decisioni ad alta leva stanno bloccando i prossimi passaggi.</p>
        <footer>
          <span>Priorità alta</span>
          <span>aggiornato 12 min fa</span>
        </footer>
      </article>

      <article
        className="home-orientation-for-you"
        data-home-orientation="for-you"
      >
        <div className="home-orientation-kicker-row">
          <span>{t(($) => $.common.home.orientation.forYou)}</span>
          <span className="home-orientation-weather" aria-hidden="true">
            ☼
          </span>
        </div>
        <strong>Uscita fotografica al tramonto</strong>
        <p>
          Luce migliore dalle 18:42. Hai una finestra utile dopo il debrief.
        </p>
        <footer>
          <span>54 min liberi</span>
          <span>meteo favorevole</span>
        </footer>
      </article>
    </section>
  );
}

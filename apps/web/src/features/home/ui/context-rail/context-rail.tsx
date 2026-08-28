import { useTranslation } from 'react-i18next';

export function ContextRail() {
  const { t } = useTranslation('common');

  return (
    <aside
      className="home-context-rail"
      data-home-region="context-rail"
      aria-label={t(($) => $.common.home.contextRail.label)}
    >
      <section data-home-context="capture">
        <header className="home-context-heading">
          <span className="home-context-icon" aria-hidden="true">
            +
          </span>
          <h2>{t(($) => $.common.home.contextRail.capture)}</h2>
        </header>

        <div className="home-capture-foundation" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
      </section>

      <section data-home-context="resolution">
        <header className="home-context-heading">
          <span className="home-context-icon" aria-hidden="true">
            ✓
          </span>
          <h2>{t(($) => $.common.home.contextRail.resolution)}</h2>
        </header>

        <div className="home-resolution-foundation" aria-hidden="true">
          <span />
          <span />
          <span />
        </div>
      </section>
    </aside>
  );
}

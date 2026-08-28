import { useTranslation } from 'react-i18next';

export function CentralStage() {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-central-stage"
      data-home-region="central-stage"
      aria-label={t(($) => $.common.home.stage.label)}
    >
      <h2 className="home-visually-hidden">
        {t(($) => $.common.home.stage.continuity)}
      </h2>

      <div className="home-stage-dock" aria-hidden="true">
        <span className="home-stage-dock-chevron">‹</span>
        <span className="home-stage-dock-label">
          {t(($) => $.common.home.stage.continuity)}
        </span>
        <span className="home-stage-dock-chevron">›</span>
      </div>

      <div className="home-stage-atmosphere" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>

      <div className="home-stage-worlds" aria-hidden="true">
        <span className="home-stage-world world-small" />
        <span className="home-stage-world world-medium" />
        <span className="home-stage-world world-active" />
        <span className="home-stage-world world-medium" />
        <span className="home-stage-world world-small" />
      </div>
    </section>
  );
}

import { useTranslation } from 'react-i18next';

type AISurfaceProps = {
  collapsed: boolean;
  onToggleCollapsed: () => void;
};

export function AISurface({
  collapsed,
  onToggleCollapsed,
}: AISurfaceProps) {
  const { t } = useTranslation('common');

  return (
    <section
      className="home-ai-surface"
      data-home-region="ai-surface"
      data-home-ai-state={collapsed ? 'collapsed' : 'expanded'}
      aria-label={t(($) => $.common.home.ai.label)}
    >
      {collapsed ? (
        <>
          <button
            className="home-ai-rail-toggle"
            type="button"
            onClick={onToggleCollapsed}
            aria-label={t(($) => $.common.home.ai.expand)}
            aria-expanded="false"
          >
            <span aria-hidden="true">›</span>
          </button>
          <span className="home-ai-rail-label" aria-hidden="true">
            AI
          </span>
        </>
      ) : (
        <>
          <header className="home-ai-heading">
            <div className="home-ai-identity">
              <span className="home-ai-mark" aria-hidden="true" />
              <h2>{t(($) => $.common.home.ai.title)}</h2>
            </div>
            <button
              className="home-ai-collapse"
              type="button"
              onClick={onToggleCollapsed}
              aria-label={t(($) => $.common.home.ai.collapse)}
              aria-expanded="true"
            >
              <span aria-hidden="true">‹</span>
            </button>
          </header>

          <div className="home-ai-thread-foundation" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>

          <div className="home-ai-composer-foundation" aria-hidden="true">
            <span />
            <span />
          </div>
        </>
      )}
    </section>
  );
}

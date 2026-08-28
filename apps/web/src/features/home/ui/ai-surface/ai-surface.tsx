import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';

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
            <img src={danteSymbolUrl} alt="" aria-hidden="true" />
            <span aria-hidden="true">›</span>
          </button>
          <span className="home-ai-rail-label" aria-hidden="true">
            DANTE
          </span>
        </>
      ) : (
        <>
          <header className="home-ai-heading">
            <div className="home-ai-identity" aria-label="DANTE">
              <img className="home-ai-symbol" src={danteSymbolUrl} alt="" aria-hidden="true" />
            </div>

            <div className="home-ai-head-actions">
              <button
                className="home-ai-head-button"
                type="button"
                disabled
                aria-label="Continua su"
                title="Continua su"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M14 5h5v5M19 5l-8 8M18 13v5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" />
                </svg>
              </button>
              <button
                className="home-ai-head-button"
                type="button"
                disabled
                aria-label="Espandi la conversazione"
                title="Schermo intero"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M8 3H3v5M16 3h5v5M8 21H3v-5M16 21h5v-5" />
                </svg>
              </button>
              <button
                className="home-ai-collapse"
                type="button"
                onClick={onToggleCollapsed}
                aria-label={t(($) => $.common.home.ai.collapse)}
                aria-expanded="true"
              >
                <span aria-hidden="true">‹</span>
              </button>
            </div>
          </header>

          <div className="home-ai-thread" role="log" aria-live="polite">
            <article className="home-ai-turn home-ai-turn-assistant">
              <span className="home-ai-turn-avatar" aria-hidden="true">
                <img src={danteSymbolUrl} alt="" />
              </span>
              <p>
                Hai due cose da rivedere e una finestra libera dalle 18:30.
                Posso aiutarti a sistemare il resto della giornata.
              </p>
            </article>

            <article className="home-ai-turn home-ai-turn-user">
              <p>Sì, ma non spostare la call delle 19:00.</p>
            </article>

            <article className="home-ai-turn home-ai-turn-assistant">
              <span className="home-ai-turn-avatar" aria-hidden="true">
                <img src={danteSymbolUrl} alt="" />
              </span>
              <p>Va bene. La tengo fissa e considero solo il resto.</p>
            </article>
          </div>

          <div className="home-ai-composer" aria-label="Scrivi a DANTE">
            <button
              className="home-ai-compose-tool"
              type="button"
              disabled
              aria-label="Allega o aggiungi"
              title="Allega o aggiungi"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 5v14M5 12h14" />
              </svg>
            </button>
            <textarea
              rows={1}
              readOnly
              aria-label="Messaggio a DANTE"
              placeholder="Scrivi a DANTE..."
            />
            <div className="home-ai-compose-actions">
              <button
                className="home-ai-compose-tool"
                type="button"
                disabled
                aria-label="Parla"
                title="Parla"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z" />
                  <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3M9 21h6" />
                </svg>
              </button>
              <button
                className="home-ai-send"
                type="button"
                disabled
                aria-label="Invia"
                title="Invia"
              >
                <svg viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M12 19V5M6.5 10.5 12 5l5.5 5.5" />
                </svg>
              </button>
            </div>
          </div>
        </>
      )}
    </section>
  );
}

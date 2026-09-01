import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';

type WorldFocusDanteSurfaceProps = Readonly<{
  world: WorldFocusWorld;
  collapsed: boolean;
  onToggleCollapsed: () => void;
}>;

/**
 * Structural pre-backend DANTE surface for World Focus.
 *
 * It reserves the real conversational footprint and collapse/expand behavior
 * now, while remaining explicit that no request is sent to a real DANTE/LLM
 * runtime in this frontend-only phase.
 */
export function WorldFocusDanteSurface({
  world,
  collapsed,
  onToggleCollapsed,
}: WorldFocusDanteSurfaceProps) {
  const { t } = useTranslation('common');
  const worldLabel = t(($) => $.common.worldFocus.worlds[world.id].label);

  return (
    <section
      className="world-focus-dante"
      data-world-focus-dante-state={collapsed ? 'collapsed' : 'expanded'}
      data-world-focus-dante-runtime="pre-backend"
      aria-label={t(($) => $.common.worldFocus.dante.label, {
        world: worldLabel,
      })}
    >
      {collapsed ? (
        <button
          className="world-focus-dante-rail-toggle"
          type="button"
          onClick={onToggleCollapsed}
          aria-label={t(($) => $.common.worldFocus.dante.expand)}
          aria-expanded="false"
        >
          <img src={danteSymbolUrl} alt="" aria-hidden="true" />
          <span className="world-focus-dante-rail-label" aria-hidden="true">
            DANTE
          </span>
          <span className="world-focus-dante-rail-chevron" aria-hidden="true">
            ›
          </span>
        </button>
      ) : (
        <>
          <header className="world-focus-dante-heading">
            <div className="world-focus-dante-identity">
              <img
                className="world-focus-dante-symbol"
                src={danteSymbolUrl}
                alt=""
                aria-hidden="true"
              />
              <div>
                <strong>DANTE</strong>
                <span>{t(($) => $.common.worldFocus.dante.preview)}</span>
              </div>
            </div>

            <button
              className="world-focus-dante-collapse"
              type="button"
              onClick={onToggleCollapsed}
              aria-label={t(($) => $.common.worldFocus.dante.collapse)}
              aria-expanded="true"
            >
              <span aria-hidden="true">‹</span>
            </button>
          </header>

          <div
            className="world-focus-dante-thread"
            role="log"
            aria-live="polite"
            aria-label={t(($) => $.common.worldFocus.dante.threadLabel)}
          >
            <article className="world-focus-dante-turn world-focus-dante-turn-assistant">
              <span className="world-focus-dante-turn-avatar" aria-hidden="true">
                <img src={danteSymbolUrl} alt="" />
              </span>
              <p>
                {t(($) => $.common.worldFocus.dante.previewAssistant, {
                  world: worldLabel,
                })}
              </p>
            </article>

            <article className="world-focus-dante-turn world-focus-dante-turn-user">
              <p>{t(($) => $.common.worldFocus.dante.previewUser)}</p>
            </article>

            <article className="world-focus-dante-turn world-focus-dante-turn-assistant">
              <span className="world-focus-dante-turn-avatar" aria-hidden="true">
                <img src={danteSymbolUrl} alt="" />
              </span>
              <p>{t(($) => $.common.worldFocus.dante.previewReply)}</p>
            </article>
          </div>

          <div
            className="world-focus-dante-composer"
            aria-label={t(($) => $.common.worldFocus.dante.composerLabel)}
          >
            <button
              className="world-focus-dante-compose-tool"
              type="button"
              disabled
              aria-label={t(($) => $.common.worldFocus.dante.add)}
            >
              <span aria-hidden="true">+</span>
            </button>
            <textarea
              rows={1}
              readOnly
              aria-label={t(($) => $.common.worldFocus.dante.messageLabel)}
              placeholder={t(($) => $.common.worldFocus.dante.placeholder)}
            />
            <button
              className="world-focus-dante-send"
              type="button"
              disabled
              aria-label={t(($) => $.common.worldFocus.dante.send)}
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 19V5M6.5 10.5 12 5l5.5 5.5" />
              </svg>
            </button>
          </div>
        </>
      )}
    </section>
  );
}

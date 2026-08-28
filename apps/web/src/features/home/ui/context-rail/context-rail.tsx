import { useTranslation } from 'react-i18next';

export function ContextRail() {
  const { t } = useTranslation('common');
  return (
    <aside className="home-context-rail" data-home-region="context-rail" aria-label={t(($) => $.common.home.contextRail.label)}>
      <section className="home-capture-panel" data-home-context="capture">
        <header className="home-context-heading"><div><span className="home-context-kicker">INPUT RAPIDO</span><h2>{t(($) => $.common.home.contextRail.capture)}</h2></div><span className="home-context-state-dot" aria-hidden="true" /></header>
        <div className="home-capture-composer">
          <textarea aria-label="Cattura rapida" placeholder="Scrivi qualcosa…" readOnly />
          <div className="home-capture-actions">
            <button type="button" disabled aria-label="Allega alla cattura">+</button>
            <button type="button" disabled aria-label="Registra voce"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z" /><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3M9 21h6" /></svg></button>
            <button className="home-capture-send" type="button" disabled aria-label="Registra cattura"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M6.5 10.5 12 5l5.5 5.5" /></svg></button>
          </div>
        </div>
        <div className="home-capture-history">
          <div><span className="home-capture-history-dot" aria-hidden="true" /><p><strong>Idea per il prossimo brano</strong><small>Registrato · 12 min fa</small></p></div>
          <div><span className="home-capture-history-dot" aria-hidden="true" /><p><strong>Controllare itinerario weekend</strong><small>Registrato · 46 min fa</small></p></div>
        </div>
        <button className="home-context-link" type="button" disabled>Registro completo <span aria-hidden="true">›</span></button>
      </section>
      <section className="home-resolution-panel" data-home-context="resolution">
        <header className="home-context-heading"><div><span className="home-context-kicker">DA DANTE A TE</span><h2>Da risolvere</h2></div><span className="home-resolution-count">3</span></header>
        <div className="home-resolution-list">
          <article><div className="home-resolution-row"><span className="home-resolution-status is-partial">Parziale</span><time>13:42</time></div><strong>Revisione concept</strong><p>Una decisione resta ambigua prima di continuare.</p><div className="home-resolution-actions"><button className="home-resolution-confirm" type="button" disabled>Conferma</button><button type="button" disabled>Correggi</button></div></article>
          <article><div className="home-resolution-row"><span className="home-resolution-status is-done">Fatto</span><time>12:18</time></div><strong>Studio inglese</strong><p>Sessione completata. Verifica il tempo registrato.</p><button className="home-resolution-details" type="button" disabled>Dettagli</button></article>
          <article><div className="home-resolution-row"><span className="home-resolution-status is-skipped">Saltato</span><time>10:05</time></div><strong>Promemoria chiamata</strong><p>Non eseguito: serve una nuova decisione.</p><button className="home-resolution-details" type="button" disabled>Dettagli</button></article>
        </div>
      </section>
    </aside>
  );
}

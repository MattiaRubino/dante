import './signal-stage.css';

function FocusGraphic() {
  return (
    <div className="home-synthesis-bars" aria-hidden="true">
      {[42, 68, 54, 82, 62].map((height, index) => (
        <i key={index} style={{ height }} />
      ))}
    </div>
  );
}

function SleepGraphic() {
  return (
    <svg
      className="home-synthesis-line"
      viewBox="0 0 230 92"
      role="img"
      aria-label="Andamento del sonno"
    >
      <polyline points="8,65 50,40 90,61 128,28 163,51 194,19 224,38" />
      <circle cx="194" cy="19" r="6" />
    </svg>
  );
}

function SpendGraphic() {
  return (
    <div className="home-synthesis-bars home-synthesis-bars-spend" aria-hidden="true">
      {[34, 50, 40, 68, 84, 58].map((height, index) => (
        <i key={index} style={{ height }} />
      ))}
    </div>
  );
}

export function SignalStage() {
  return (
    <section className="home-stats-stage" aria-label="Sintesi" role="region">
      <div className="home-stats-track" role="list">
        <article className="home-synthesis-metric home-synthesis-focus" role="listitem">
          <span className="home-synthesis-kicker">FOCUS</span>
          <strong className="home-synthesis-value">5h 20m</strong>
          <FocusGraphic />
          <small className="home-synthesis-detail">questa settimana</small>
        </article>

        <article className="home-synthesis-metric home-synthesis-sleep" role="listitem">
          <span className="home-synthesis-kicker">SONNO</span>
          <strong className="home-synthesis-value">6h 38m</strong>
          <SleepGraphic />
          <small className="home-synthesis-detail">↓ 42m · media 3 sett.</small>
        </article>

        <article className="home-synthesis-metric home-synthesis-spend" role="listitem">
          <span className="home-synthesis-kicker">SPESA</span>
          <strong className="home-synthesis-value">€412</strong>
          <SpendGraphic />
          <small className="home-synthesis-detail">↑ 18% · questo mese</small>
        </article>
      </div>
    </section>
  );
}

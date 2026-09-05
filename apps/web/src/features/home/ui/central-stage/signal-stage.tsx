import { useState } from 'react';

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
    <div
      className="home-synthesis-bars home-synthesis-bars-spend"
      aria-hidden="true"
    >
      {[34, 50, 40, 68, 84, 58].map((height, index) => (
        <i key={index} style={{ height }} />
      ))}
    </div>
  );
}

const SYNTHESIS_METRICS = [
  {
    id: 'focus',
    className: 'home-synthesis-focus',
    kicker: 'FOCUS',
    value: '5h 20m',
    detail: 'questa settimana',
    Graphic: FocusGraphic,
  },
  {
    id: 'sleep',
    className: 'home-synthesis-sleep',
    kicker: 'SONNO',
    value: '6h 38m',
    detail: '↓ 42m · media 3 sett.',
    Graphic: SleepGraphic,
  },
  {
    id: 'spend',
    className: 'home-synthesis-spend',
    kicker: 'SPESA',
    value: '€412',
    detail: '↑ 18% · questo mese',
    Graphic: SpendGraphic,
  },
] as const;

function modulo(value: number, divisor: number) {
  return ((value % divisor) + divisor) % divisor;
}

export function SignalStage() {
  const [offset, setOffset] = useState(0);
  const visibleMetrics = SYNTHESIS_METRICS.map(
    (_, slot) =>
      SYNTHESIS_METRICS[modulo(slot + offset, SYNTHESIS_METRICS.length)]!,
  );

  const step = (direction: -1 | 1) => {
    setOffset((current) =>
      modulo(current + direction, SYNTHESIS_METRICS.length),
    );
  };

  return (
    <section className="home-stats-stage" aria-label="Sintesi" role="region">
      <div className="home-stats-track" role="list">
        {visibleMetrics.map((metric) => {
          const Graphic = metric.Graphic;

          return (
            <article
              key={metric.id}
              className={`home-synthesis-metric ${metric.className}`}
              role="listitem"
            >
              <span className="home-synthesis-kicker">{metric.kicker}</span>
              <strong className="home-synthesis-value">{metric.value}</strong>
              <Graphic />
              <small className="home-synthesis-detail">{metric.detail}</small>
            </article>
          );
        })}
      </div>

      <button
        className="home-world-arrow home-world-arrow-prev"
        type="button"
        onClick={() => step(-1)}
        aria-label="Sintesi precedente"
      >
        ‹
      </button>
      <button
        className="home-world-arrow home-world-arrow-next"
        type="button"
        onClick={() => step(1)}
        aria-label="Sintesi successiva"
      >
        ›
      </button>
    </section>
  );
}

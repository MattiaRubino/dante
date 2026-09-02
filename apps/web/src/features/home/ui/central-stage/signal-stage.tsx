import { useState } from 'react';
import { useTranslation } from 'react-i18next';

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

function SleepGraphic({ ariaLabel }: { ariaLabel: string }) {
  return (
    <svg
      className="home-synthesis-line"
      viewBox="0 0 230 92"
      role="img"
      aria-label={ariaLabel}
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

const SIGNAL_METRICS = [
  { id: 'focus', className: 'home-synthesis-focus' },
  { id: 'sleep', className: 'home-synthesis-sleep' },
  { id: 'spend', className: 'home-synthesis-spend' },
] as const;

function modulo(value: number, divisor: number) {
  return ((value % divisor) + divisor) % divisor;
}

export function SignalStage() {
  const { t } = useTranslation('common');
  const [offset, setOffset] = useState(0);
  const visibleMetrics = SIGNAL_METRICS.map(
    (_, slot) => SIGNAL_METRICS[modulo(slot + offset, SIGNAL_METRICS.length)]!,
  );

  const step = (direction: -1 | 1) => {
    setOffset((current) =>
      modulo(current + direction, SIGNAL_METRICS.length),
    );
  };

  const metricCopy = {
    focus: {
      kicker: t(($) => $.common.home.stage.signalMetrics.focus.kicker),
      value: t(($) => $.common.home.stage.signalMetrics.focus.value),
      detail: t(($) => $.common.home.stage.signalMetrics.focus.detail),
    },
    sleep: {
      kicker: t(($) => $.common.home.stage.signalMetrics.sleep.kicker),
      value: t(($) => $.common.home.stage.signalMetrics.sleep.value),
      detail: t(($) => $.common.home.stage.signalMetrics.sleep.detail),
    },
    spend: {
      kicker: t(($) => $.common.home.stage.signalMetrics.spend.kicker),
      value: t(($) => $.common.home.stage.signalMetrics.spend.value),
      detail: t(($) => $.common.home.stage.signalMetrics.spend.detail),
    },
  } as const;

  const sleepTrendLabel = t(($) => $.common.home.stage.signalSleepTrend);

  return (
    <section
      className="home-signal-stage"
      aria-label={t(($) => $.common.home.stage.signals)}
      role="region"
    >
      <div className="home-signal-track" role="list">
        {visibleMetrics.map((metric) => {
          const copy = metricCopy[metric.id];

          return (
            <article
              key={metric.id}
              className={`home-synthesis-metric ${metric.className}`}
              role="listitem"
            >
              <span className="home-synthesis-kicker">{copy.kicker}</span>
              <strong className="home-synthesis-value">{copy.value}</strong>
              {metric.id === 'focus' ? (
                <FocusGraphic />
              ) : metric.id === 'sleep' ? (
                <SleepGraphic ariaLabel={sleepTrendLabel} />
              ) : (
                <SpendGraphic />
              )}
              <small className="home-synthesis-detail">{copy.detail}</small>
            </article>
          );
        })}
      </div>

      <button
        className="home-world-arrow home-world-arrow-prev"
        type="button"
        onClick={() => step(-1)}
        aria-label={t(($) => $.common.home.stage.signalsPrevious)}
      >
        ‹
      </button>
      <button
        className="home-world-arrow home-world-arrow-next"
        type="button"
        onClick={() => step(1)}
        aria-label={t(($) => $.common.home.stage.signalsNext)}
      >
        ›
      </button>
    </section>
  );
}

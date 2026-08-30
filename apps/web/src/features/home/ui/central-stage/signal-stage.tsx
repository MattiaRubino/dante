import {
  useCallback,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type KeyboardEvent as ReactKeyboardEvent,
  type PointerEvent as ReactPointerEvent,
} from 'react';

import './signal-stage.css';

type SignalId =
  | 'balance'
  | 'time'
  | 'movement'
  | 'sleep'
  | 'focus'
  | 'load'
  | 'routines';

type SignalDefinition = Readonly<{
  id: SignalId;
  kicker: string;
  title: string;
  accent: string;
  value: string;
  detail: string;
}>;

type SignalDragState = {
  pointerId: number;
  startX: number;
  lastX: number;
  pressedIndex: number | null;
};

const SIGNALS: readonly SignalDefinition[] = [
  {
    id: 'balance',
    kicker: 'Panoramica',
    title: 'Equilibrio aree',
    accent: '#8b7bff',
    value: '6 aree',
    detail: 'ultimi 30 giorni',
  },
  {
    id: 'time',
    kicker: 'Panoramica',
    title: 'Tempo per area',
    accent: '#c07bff',
    value: '38%',
    detail: 'quota maggiore: Lavoro',
  },
  {
    id: 'movement',
    kicker: 'Corpo',
    title: 'Movimento',
    accent: '#4f92ff',
    value: '5 / 7',
    detail: 'giorni attivi',
  },
  {
    id: 'sleep',
    kicker: 'Corpo',
    title: 'Sonno',
    accent: '#3fc9e0',
    value: '7h 14m',
    detail: 'media 7 giorni',
  },
  {
    id: 'focus',
    kicker: 'Mente',
    title: 'Focus',
    accent: '#55c99a',
    value: '11h 20m',
    detail: 'settimana corrente',
  },
  {
    id: 'load',
    kicker: 'Carico',
    title: 'Carico per area',
    accent: '#f0b357',
    value: '+12%',
    detail: 'vs 4 settimane fa',
  },
  {
    id: 'routines',
    kicker: 'Routine',
    title: 'Costanza routine',
    accent: '#f2778c',
    value: '81%',
    detail: 'completamento medio',
  },
] as const;

const SIGNAL_DRAG_THRESHOLD = 34;

function modulo(value: number, divisor: number) {
  return ((value % divisor) + divisor) % divisor;
}

function signalAt(index: number) {
  const signal = SIGNALS[modulo(index, SIGNALS.length)];
  if (!signal) {
    throw new Error(`Home synthesis invariant violated at index ${index}`);
  }
  return signal;
}

function SignalGraphic({ id }: Readonly<{ id: SignalId }>) {
  switch (id) {
    case 'balance':
      return (
        <svg
          viewBox="38 8 84 94"
          role="img"
          aria-label="Radar equilibrio aree"
          preserveAspectRatio="xMidYMid meet"
        >
          <g className="home-stat-grid">
            <polygon points="80,12 117.2,33.5 117.2,76.5 80,98 42.8,76.5 42.8,33.5" />
            <polygon points="80,33 100.8,45 100.8,69 80,81 59.2,69 59.2,45" />
          </g>
          <polygon
            className="home-stat-series-a"
            points="80,19 108,37 111,72 80,94 55,70 51,36"
          />
          <g className="home-stat-node">
            <circle cx="80" cy="19" r="1.9" />
            <circle cx="108" cy="37" r="1.9" />
            <circle cx="111" cy="72" r="1.9" />
            <circle cx="80" cy="94" r="1.9" />
            <circle cx="55" cy="70" r="1.9" />
            <circle cx="51" cy="36" r="1.9" />
          </g>
        </svg>
      );
    case 'time':
      return (
        <svg
          viewBox="38 12 84 84"
          role="img"
          aria-label="Distribuzione del tempo per area"
          preserveAspectRatio="xMidYMid meet"
        >
          <g transform="translate(80,54) rotate(-90)">
            <circle className="home-stat-ring-track" r="34" fill="none" />
            <circle
              className="home-stat-segment home-stat-segment-1"
              r="34"
              fill="none"
              strokeDasharray="81.2 132.4"
            />
            <circle
              className="home-stat-segment home-stat-segment-2"
              r="34"
              fill="none"
              strokeDasharray="55.5 158.1"
              strokeDashoffset="-81.2"
            />
            <circle
              className="home-stat-segment home-stat-segment-3"
              r="34"
              fill="none"
              strokeDasharray="42.7 170.9"
              strokeDashoffset="-136.7"
            />
            <circle
              className="home-stat-segment home-stat-segment-4"
              r="34"
              fill="none"
              strokeDasharray="34.2 179.4"
              strokeDashoffset="-179.4"
            />
          </g>
          <text className="home-stat-center" x="80" y="59" textAnchor="middle">
            38%
          </text>
        </svg>
      );
    case 'movement':
      return (
        <svg
          viewBox="18 18 128 84"
          role="img"
          aria-label="Movimento negli ultimi 7 giorni"
          preserveAspectRatio="xMidYMid meet"
        >
          <g className="home-stat-bars">
            <rect x="22" y="58" width="12" height="40" rx="5" />
            <rect x="40" y="44" width="12" height="54" rx="5" />
            <rect x="58" y="70" width="12" height="28" rx="5" />
            <rect x="76" y="32" width="12" height="66" rx="5" />
            <rect x="94" y="50" width="12" height="48" rx="5" />
            <rect className="is-peak" x="112" y="22" width="12" height="76" rx="5" />
            <rect x="130" y="76" width="12" height="22" rx="5" />
          </g>
        </svg>
      );
    case 'sleep':
      return (
        <svg
          viewBox="14 26 136 76"
          role="img"
          aria-label="Sonno negli ultimi 7 giorni"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            <linearGradient id="home-sleep-fill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor="currentColor" stopOpacity="0.24" />
              <stop offset="1" stopColor="currentColor" stopOpacity="0" />
            </linearGradient>
          </defs>
          <path
            className="home-stat-area"
            fill="url(#home-sleep-fill)"
            d="M18 62 L40 46 L62 74 L84 38 L106 52 L128 30 L146 42 L146 98 L18 98 Z"
          />
          <polyline
            className="home-stat-series-line"
            points="18,62 40,46 62,74 84,38 106,52 128,30 146,42"
          />
          <g className="home-stat-node">
            <circle cx="128" cy="30" r="2.2" />
          </g>
        </svg>
      );
    case 'focus':
      return (
        <svg
          viewBox="38 12 84 84"
          role="img"
          aria-label="Focus rispetto all obiettivo"
          preserveAspectRatio="xMidYMid meet"
        >
          <g transform="translate(80,54) rotate(-90)">
            <circle className="home-stat-ring-track" r="36" fill="none" />
            <circle
              className="home-stat-ring-value"
              r="36"
              fill="none"
              strokeDasharray="158.3 67.9"
              strokeLinecap="round"
            />
          </g>
          <text className="home-stat-center" x="80" y="59" textAnchor="middle">
            70%
          </text>
        </svg>
      );
    case 'load':
      return (
        <svg
          viewBox="20 26 128 76"
          role="img"
          aria-label="Carico per area"
          preserveAspectRatio="xMidYMid meet"
        >
          <g className="home-stat-stack">
            <rect className="k1" x="24" y="62" width="18" height="36" rx="4" />
            <rect className="k2" x="24" y="46" width="18" height="14" rx="4" />
            <rect className="k3" x="24" y="34" width="18" height="10" rx="4" />
            <rect className="k1" x="58" y="70" width="18" height="28" rx="4" />
            <rect className="k2" x="58" y="50" width="18" height="18" rx="4" />
            <rect className="k3" x="58" y="40" width="18" height="8" rx="4" />
            <rect className="k1" x="92" y="56" width="18" height="42" rx="4" />
            <rect className="k2" x="92" y="42" width="18" height="12" rx="4" />
            <rect className="k3" x="92" y="30" width="18" height="10" rx="4" />
            <rect className="k1" x="126" y="66" width="18" height="32" rx="4" />
            <rect className="k2" x="126" y="48" width="18" height="16" rx="4" />
            <rect className="k3" x="126" y="38" width="18" height="8" rx="4" />
          </g>
        </svg>
      );
    case 'routines':
      return (
        <svg
          viewBox="18 18 123 72"
          role="img"
          aria-label="Costanza routine"
          preserveAspectRatio="xMidYMid meet"
        >
          <g className="home-stat-cells">
            {[
              0.85, 0.45, 0.9, 0.7, 0.95, 0.3, 0.6,
              0.6, 0.9, 0.35, 0.8, 0.55, 0.9, 0.75,
              0.9, 0.7, 0.85, 0.4, 0.8, 0.65, 0.95,
              0.5, 0.85, 0.7, 0.9, 0.45, 0.8, 0.6,
            ].map((opacity, index) => {
              const column = index % 7;
              const row = Math.floor(index / 7);
              return (
                <rect
                  key={index}
                  x={22 + column * 17}
                  y={22 + row * 17}
                  width="13"
                  height="13"
                  rx="4"
                  opacity={opacity}
                />
              );
            })}
          </g>
        </svg>
      );
  }
}

export function SignalStage() {
  const [activeIndex, setActiveIndex] = useState(0);
  const dragRef = useRef<SignalDragState | null>(null);

  const step = useCallback((direction: -1 | 1) => {
    setActiveIndex((current) => modulo(current + direction, SIGNALS.length));
  }, []);

  const visibleSignals = useMemo(
    () =>
      [-1, 0, 1].map((offset) => {
        const index = modulo(activeIndex + offset, SIGNALS.length);
        return { index, offset, signal: signalAt(index) };
      }),
    [activeIndex],
  );

  const handlePointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (event.pointerType === 'mouse' && event.button !== 0) return;
    const target = event.target;
    const visual =
      target instanceof Element
        ? target.closest<HTMLElement>('[data-signal-index]')
        : null;

    dragRef.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      lastX: event.clientX,
      pressedIndex: visual ? Number(visual.dataset.signalIndex) : null,
    };

    event.currentTarget.dataset.dragging = 'true';
    try {
      event.currentTarget.setPointerCapture(event.pointerId);
    } catch {
      // Pointer capture is optional in synthetic/test environments.
    }
  };

  const handlePointerMove = (event: ReactPointerEvent<HTMLDivElement>) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) return;
    drag.lastX = event.clientX;
  };

  const finishPointer = (
    event: ReactPointerEvent<HTMLDivElement>,
    cancelled: boolean,
  ) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) return;

    dragRef.current = null;
    delete event.currentTarget.dataset.dragging;

    if (cancelled) return;

    const travel = event.clientX - drag.startX;
    if (Math.abs(travel) >= SIGNAL_DRAG_THRESHOLD) {
      step(travel < 0 ? 1 : -1);
      return;
    }

    if (drag.pressedIndex !== null && Number.isFinite(drag.pressedIndex)) {
      setActiveIndex(modulo(drag.pressedIndex, SIGNALS.length));
    }
  };

  const handleKeyDown = (event: ReactKeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      step(-1);
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      step(1);
    }
  };

  return (
    <div className="home-stats-stage" aria-label="Sintesi">
      <div
        className="home-stats-track"
        role="list"
        tabIndex={0}
        onKeyDown={handleKeyDown}
        onPointerDown={handlePointerDown}
        onPointerMove={handlePointerMove}
        onPointerUp={(event) => finishPointer(event, false)}
        onPointerCancel={(event) => finishPointer(event, true)}
      >
        {visibleSignals.map(({ index, offset, signal }) => (
          <article
            key={`${signal.id}-${offset}`}
            className="home-stat-visual"
            data-active={offset === 0 ? 'true' : 'false'}
            data-signal-index={index}
            role="listitem"
            tabIndex={0}
            style={{ '--stat-accent': signal.accent } as CSSProperties}
            onFocus={() => setActiveIndex(index)}
            onClick={(event) => {
              if (event.detail === 0) setActiveIndex(index);
            }}
          >
            <span className="home-stat-kicker">{signal.kicker}</span>
            <strong className="home-stat-title">{signal.title}</strong>
            <div className="home-stat-chart">
              <SignalGraphic id={signal.id} />
            </div>
            <div className="home-stat-meta">
              <b>{signal.value}</b>
              <small>{signal.detail}</small>
            </div>
          </article>
        ))}
      </div>

      <button
        className="home-stat-arrow home-stat-arrow-prev"
        type="button"
        onClick={() => step(-1)}
        aria-label="Grafico precedente"
      >
        ‹
      </button>
      <button
        className="home-stat-arrow home-stat-arrow-next"
        type="button"
        onClick={() => step(1)}
        aria-label="Grafico successivo"
      >
        ›
      </button>
    </div>
  );
}

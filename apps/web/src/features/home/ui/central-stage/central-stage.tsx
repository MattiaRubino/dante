import { useMemo, useState, type CSSProperties } from 'react';
import { useTranslation } from 'react-i18next';

type WorldIconName =
  | 'body'
  | 'music'
  | 'travel'
  | 'study'
  | 'finance'
  | 'people'
  | 'work'
  | 'growth'
  | 'routine'
  | 'project';

type World = {
  name: string;
  color: string;
  description: string;
  icon: WorldIconName;
  progress: number | null;
};

const WORLDS: readonly World[] = [
  {
    name: 'Corpo',
    color: '#b060ff',
    description: 'La tua base. La tua energia. Il tuo veicolo.',
    icon: 'body',
    progress: 0.68,
  },
  {
    name: 'Musica',
    color: '#ffad34',
    description: 'Creatività, ascolto e progetti musicali.',
    icon: 'music',
    progress: null,
  },
  {
    name: 'Viaggi',
    color: '#27d9f5',
    description: 'Esperienze, luoghi e prossime partenze.',
    icon: 'travel',
    progress: null,
  },
  {
    name: 'Studio',
    color: '#4288ff',
    description: 'Apprendimento, competenze e percorsi.',
    icon: 'study',
    progress: 0.42,
  },
  {
    name: 'Finanza',
    color: '#8bdc47',
    description: 'Risorse, risparmio e obiettivi economici.',
    icon: 'finance',
    progress: 0.76,
  },
  {
    name: 'Relazioni',
    color: '#d85bff',
    description: 'Persone, legami e tempo condiviso.',
    icon: 'people',
    progress: null,
  },
  {
    name: 'Lavoro',
    color: '#ff9e43',
    description: 'Progetti, risultati e crescita professionale.',
    icon: 'work',
    progress: 0.55,
  },
  {
    name: 'Crescita',
    color: '#39e6d0',
    description: 'Abitudini, consapevolezza e direzione.',
    icon: 'growth',
    progress: null,
  },
  {
    name: 'Routine',
    color: '#ff6c7c',
    description: 'Ritmi, sistemi e consistenza quotidiana.',
    icon: 'routine',
    progress: 0.81,
  },
  {
    name: 'Progetti',
    color: '#8a74ff',
    description: 'Idee in movimento e prossimi traguardi.',
    icon: 'project',
    progress: 0.35,
  },
] as const;

function getWorld(index: number): World {
  const world = WORLDS[index];

  if (!world) {
    throw new Error(
      `Home stage invariant violated: missing world at index ${index}`,
    );
  }

  return world;
}

function WorldIcon({ name }: { name: WorldIconName }) {
  switch (name) {
    case 'body':
      return (
        <svg viewBox="0 0 48 48">
          <circle cx="24" cy="11" r="6" />
          <path d="M16 42v-9c0-4 2-7 4-9m12 18v-9c0-4-2-7-4-9M17 22c2-3 4-4 7-4s5 1 7 4M21 27c1 2 2 3 3 3s2-1 3-3" />
        </svg>
      );
    case 'music':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M19 34V13l18-4v21" />
          <circle cx="14" cy="35" r="5" />
          <circle cx="32" cy="31" r="5" />
        </svg>
      );
    case 'travel':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M6 27l35-17-13 31-6-12-16-2zM22 29l19-19" />
        </svg>
      );
    case 'study':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M6 12c7-3 13-3 18 2v25c-5-5-11-5-18-2V12zm36 0c-7-3-13-3-18 2v25c5-5 11-5 18-2V12z" />
        </svg>
      );
    case 'finance':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M30 8c-2-2-4-3-7-3-5 0-9 3-9 8 0 11 19 6 19 17 0 5-4 9-10 9-4 0-7-1-10-4M24 2v44" />
        </svg>
      );
    case 'people':
      return (
        <svg viewBox="0 0 48 48">
          <circle cx="18" cy="17" r="6" />
          <circle cx="33" cy="18" r="5" />
          <path d="M6 40c1-8 5-12 12-12s11 4 12 12M29 29c7 0 11 4 12 11" />
        </svg>
      );
    case 'work':
      return (
        <svg viewBox="0 0 48 48">
          <rect x="6" y="14" width="36" height="25" rx="4" />
          <path d="M17 14v-4h14v4M6 25h36M20 25v4h8v-4" />
        </svg>
      );
    case 'growth':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M24 42V24M24 28C15 28 9 22 9 13c9 0 15 5 15 15zm0-4c0-9 6-15 15-15 0 9-6 15-15 15z" />
        </svg>
      );
    case 'routine':
      return (
        <svg viewBox="0 0 48 48">
          <circle cx="24" cy="24" r="17" />
          <path d="M24 13v12l8 5M11 11l-4 7h8" />
        </svg>
      );
    case 'project':
      return (
        <svg viewBox="0 0 48 48">
          <path d="M24 5l6 12 13 7-13 7-6 12-6-12-13-7 13-7 6-12z" />
        </svg>
      );
  }
}

function SignalCards() {
  return (
    <div className="home-signal-track" role="list" aria-label="Segnali">
      <article className="home-signal-card signal-balance" role="listitem">
        <span>Panoramica</span>
        <strong>Equilibrio aree</strong>
        <svg viewBox="0 0 160 104" aria-hidden="true">
          <polygon
            className="signal-grid"
            points="80,12 117,33 117,76 80,98 43,76 43,33"
          />
          <polygon
            className="signal-series"
            points="80,19 108,37 111,72 80,94 55,70 51,36"
          />
        </svg>
        <footer>
          <b>6 aree</b>
          <small>ultimi 30 giorni</small>
        </footer>
      </article>
      <article className="home-signal-card signal-time" role="listitem">
        <span>Panoramica</span>
        <strong>Tempo per area</strong>
        <div className="home-signal-ring" aria-hidden="true">
          <b>38%</b>
        </div>
        <footer>
          <b>38%</b>
          <small>quota maggiore: Lavoro</small>
        </footer>
      </article>
      <article className="home-signal-card signal-movement" role="listitem">
        <span>Corpo</span>
        <strong>Movimento</strong>
        <div className="home-signal-bars" aria-hidden="true">
          {[40, 54, 28, 66, 48, 76, 22].map((height, index) => (
            <i key={index} style={{ height }} />
          ))}
        </div>
        <footer>
          <b>5 / 7</b>
          <small>giorni attivi</small>
        </footer>
      </article>
    </div>
  );
}

export function CentralStage() {
  const { t } = useTranslation('common');
  const [mode, setMode] = useState<'worlds' | 'signals'>('worlds');
  const [activeIndex, setActiveIndex] = useState(0);

  const visibleWorlds = useMemo(
    () =>
      [-2, -1, 0, 1, 2].map((offset) => {
        const index = (activeIndex + offset + WORLDS.length) % WORLDS.length;
        return { world: getWorld(index), index };
      }),
    [activeIndex],
  );

  const activeWorld = getWorld(activeIndex);

  const moveWorld = (direction: -1 | 1) => {
    setActiveIndex(
      (value) => (value + direction + WORLDS.length) % WORLDS.length,
    );
  };

  const switchMode = () =>
    setMode((value) => (value === 'worlds' ? 'signals' : 'worlds'));

  return (
    <section
      className="home-central-stage"
      data-home-region="central-stage"
      data-home-stage-mode={mode === 'worlds' ? 'continuity' : 'signals'}
      aria-label={t(($) => $.common.home.stage.label)}
    >
      <h2 className="home-visually-hidden">
        {mode === 'worlds'
          ? t(($) => $.common.home.stage.continuity)
          : t(($) => $.common.home.stage.signals)}
      </h2>

      <div className="home-stage-dock">
        <button
          type="button"
          onClick={switchMode}
          aria-label="Proiezione precedente"
        >
          ‹
        </button>
        <span>{mode === 'worlds' ? 'MONDI' : 'SEGNALI'}</span>
        <button
          type="button"
          onClick={switchMode}
          aria-label="Proiezione successiva"
        >
          ›
        </button>
      </div>

      <div className="home-stage-atmosphere" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>

      {mode === 'worlds' ? (
        <>
          <div className="home-world-selected-copy" aria-live="polite">
            <span>World selezionato</span>
            <strong>{activeWorld.name}</strong>
            <p>{activeWorld.description}</p>
          </div>

          <button
            className="home-stage-arrow home-stage-arrow-prev"
            type="button"
            onClick={() => moveWorld(-1)}
            aria-label="Mondo precedente"
          >
            ‹
          </button>

          <div className="home-stage-worlds" role="list" aria-label="Mondi">
            {visibleWorlds.map(({ world, index }, slotIndex) => {
              const isActive = index === activeIndex;

              return (
                <button
                  key={`${world.name}-${slotIndex}`}
                  className={`home-world-orb slot-${slotIndex}${isActive ? ' is-active' : ''}`}
                  type="button"
                  style={{ '--world-color': world.color } as CSSProperties}
                  onClick={() => setActiveIndex(index)}
                  aria-label={world.name}
                  aria-current={isActive ? 'true' : undefined}
                >
                  <span className="home-world-halo" aria-hidden="true" />
                  <span className="home-world-core" aria-hidden="true">
                    <WorldIcon name={world.icon} />
                  </span>
                  {world.progress !== null ? (
                    <span
                      className="home-world-progress"
                      style={
                        {
                          '--world-progress': `${world.progress * 360}deg`,
                        } as CSSProperties
                      }
                      aria-hidden="true"
                    />
                  ) : null}
                  <span className="home-world-label">
                    <b>{world.name}</b>
                    <small>
                      {world.progress !== null
                        ? `${Math.round(world.progress * 100)}%`
                        : 'Attivo'}
                    </small>
                  </span>
                </button>
              );
            })}
          </div>

          <button
            className="home-stage-arrow home-stage-arrow-next"
            type="button"
            onClick={() => moveWorld(1)}
            aria-label="Mondo successivo"
          >
            ›
          </button>
        </>
      ) : (
        <SignalCards />
      )}
    </section>
  );
}

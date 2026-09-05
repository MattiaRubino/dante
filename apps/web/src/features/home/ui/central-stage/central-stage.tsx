import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import './central-stage.css';
import { SignalStage } from './signal-stage';

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

type World = Readonly<{
  name: string;
  color: string;
  description: string;
  icon: WorldIconName;
  progress: number | null;
}>;

type VisibleWorld = Readonly<{
  logical: number;
  index: number;
  world: World;
  active: boolean;
  distance: number;
  x: number;
  y: number;
  scale: number;
  opacity: number;
  zIndex: number;
}>;

type SceneSize = Readonly<{
  width: number;
  height: number;
}>;

type DragState = {
  pointerId: number;
  startX: number;
  lastX: number;
  startPosition: number;
  pressedLogical: number | null;
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

const DEFAULT_SCENE_SIZE: SceneSize = { width: 900, height: 300 };
const WORLD_DRAG_PIXELS_PER_ITEM = 170;
const WORLD_CLICK_TRAVEL_THRESHOLD = 7;
const WORLD_ANIMATION_MS = 260;

function clamp(value: number, minimum: number, maximum: number) {
  return Math.max(minimum, Math.min(maximum, value));
}

function modulo(value: number, divisor: number) {
  return ((value % divisor) + divisor) % divisor;
}

function lerp(start: number, end: number, progress: number) {
  return start + (end - start) * progress;
}

function getWorld(index: number): World {
  const world = WORLDS[index];

  if (!world) {
    throw new Error(
      `Home stage invariant violated: missing world at index ${index}`,
    );
  }

  return world;
}

function getCarouselMetrics(width: number) {
  return {
    spacing: clamp(142 + (width - 1150) * 0.085, 142, 170),
    scale: clamp(width / 1450, 0.88, 1),
  };
}

function smoothAdjacentWeight(distance: number) {
  const raw = Math.max(0, 1 - Math.abs(distance - 1) / 0.68);
  return raw * raw * (3 - 2 * raw);
}

function projectVisibleWorlds(position: number, width: number) {
  const visible: VisibleWorld[] = [];
  const count = WORLDS.length;
  const metrics = getCarouselMetrics(width);
  const center = position;

  for (let slot = -3; slot <= 3; slot += 1) {
    const logical = Math.round(center) + slot;
    const index = modulo(logical, count);
    let delta = logical - center;

    if (count > 1) {
      while (delta > count / 2) delta -= count;
      while (delta < -count / 2) delta += count;
    }

    if (Math.abs(delta) > 2.65) continue;

    const distance = Math.abs(delta);
    const sign = delta === 0 ? 0 : delta < 0 ? -1 : 1;
    const adjacentWeight = smoothAdjacentWeight(distance);
    const baseX = delta * metrics.spacing;
    const x = baseX + sign * (7 * adjacentWeight);
    const magnet = Math.max(0, 1 - distance / 1.06);
    const baseScale =
      (0.62 + magnet * 0.52 + Math.max(0, 1 - distance / 2.45) * 0.1) *
      metrics.scale;
    const scale = clamp(baseScale + 0.03 * adjacentWeight, 0.58, 1.18);
    const opacity = clamp(1 - distance * 0.17, 0.5, 1);
    const y = 9 - Math.max(0, 1 - distance / 1.56) * 18 - 1.5 * adjacentWeight;

    visible.push({
      logical,
      index,
      world: getWorld(index),
      active: distance < 0.42,
      distance,
      x,
      y,
      scale,
      opacity,
      zIndex: 30 - Math.round(distance * 6),
    });
  }

  return visible;
}

function hexRgb(hex: string): readonly [number, number, number] {
  const numeric = Number.parseInt(hex.replace('#', ''), 16);
  return [(numeric >> 16) & 255, (numeric >> 8) & 255, numeric & 255];
}

function rgba(rgb: readonly [number, number, number], alpha: number) {
  return `rgba(${rgb[0]},${rgb[1]},${rgb[2]},${alpha})`;
}

function drawWorldEffects(
  canvas: HTMLCanvasElement,
  worlds: readonly VisibleWorld[],
  size: SceneSize,
) {
  const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
  const width = Math.max(1, size.width);
  const height = Math.max(1, size.height);

  canvas.width = Math.round(width * ratio);
  canvas.height = Math.round(height * ratio);
  canvas.style.width = `${width}px`;
  canvas.style.height = `${height}px`;

  const context = canvas.getContext('2d');
  if (!context) return;

  context.setTransform(ratio, 0, 0, ratio, 0, 0);
  context.clearRect(0, 0, width, height);

  for (const item of worlds) {
    const rgb = hexRgb(item.world.color);
    const x = width / 2 + item.x;
    const y = height * 0.54 + item.y;
    const radius = 59 * item.scale;

    context.save();
    context.globalCompositeOperation = 'screen';

    const glow = context.createRadialGradient(x, y, 0, x, y, radius + 92);
    glow.addColorStop(0, rgba(rgb, item.active ? 0.11 : 0.07));
    glow.addColorStop(0.48, rgba(rgb, item.active ? 0.045 : 0.028));
    glow.addColorStop(1, 'rgba(0,0,0,0)');
    context.fillStyle = glow;
    context.beginPath();
    context.arc(x, y, radius + 92, 0, Math.PI * 2);
    context.fill();

    for (let arc = 0; arc < 4; arc += 1) {
      const ringRadius = radius + 8 + arc * 6;
      context.beginPath();
      context.arc(x, y, ringRadius, -2.38 + arc * 0.2, -1.54 + arc * 0.2);
      context.strokeStyle = rgba(rgb, (item.active ? 0.21 : 0.17) - arc * 0.03);
      context.lineWidth = 1;
      context.stroke();

      context.beginPath();
      context.arc(x, y, ringRadius, 0.72 + arc * 0.17, 1.5 + arc * 0.16);
      context.strokeStyle = rgba(
        rgb,
        (item.active ? 0.18 : 0.145) - arc * 0.025,
      );
      context.lineWidth = 0.95;
      context.stroke();
    }

    const ellipseCount = item.active ? 4 : 3;
    for (let ellipse = 0; ellipse < ellipseCount; ellipse += 1) {
      context.beginPath();
      context.ellipse(
        x,
        y + 2,
        radius + ellipse * 7,
        Math.max(18, radius * 0.34) + ellipse * 3,
        -0.03,
        0,
        Math.PI * 2,
      );
      context.strokeStyle = rgba(
        rgb,
        item.active ? 0.07 - ellipse * 0.012 : 0.045 - ellipse * 0.009,
      );
      context.lineWidth = item.active ? 0.9 : 0.64;
      context.stroke();
    }

    context.restore();
  }
}

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true
  );
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

export function CentralStage() {
  const { t } = useTranslation('common');
  const [mode, setMode] = useState<'worlds' | 'signals'>('worlds');
  const [position, setPosition] = useState(0);
  const [sceneSize, setSceneSize] = useState<SceneSize>(DEFAULT_SCENE_SIZE);
  const sceneRef = useRef<HTMLDivElement | null>(null);
  const fxCanvasRef = useRef<HTMLCanvasElement | null>(null);
  const positionRef = useRef(0);
  const animationFrameRef = useRef<number | null>(null);
  const dragFrameRef = useRef<number | null>(null);
  const dragRef = useRef<DragState | null>(null);

  const setCarouselPosition = useCallback((nextPosition: number) => {
    positionRef.current = nextPosition;
    setPosition(nextPosition);
  }, []);

  const cancelCarouselAnimation = useCallback(() => {
    if (animationFrameRef.current !== null) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
  }, []);

  const animateTo = useCallback(
    (target: number) => {
      cancelCarouselAnimation();

      const count = WORLDS.length;
      const start = positionRef.current;
      let goal = target;
      let distance = goal - start;

      while (distance > count / 2) {
        goal -= count;
        distance = goal - start;
      }
      while (distance < -count / 2) {
        goal += count;
        distance = goal - start;
      }

      if (prefersReducedMotion()) {
        setCarouselPosition(modulo(Math.round(goal), count));
        return;
      }

      const startedAt = performance.now();
      const step = (now: number) => {
        const progress = Math.min(1, (now - startedAt) / WORLD_ANIMATION_MS);
        const eased = 1 - Math.pow(1 - progress, 5);
        setCarouselPosition(lerp(start, goal, eased));

        if (progress < 1) {
          animationFrameRef.current = requestAnimationFrame(step);
        } else {
          animationFrameRef.current = null;
          setCarouselPosition(modulo(Math.round(goal), count));
        }
      };

      animationFrameRef.current = requestAnimationFrame(step);
    },
    [cancelCarouselAnimation, setCarouselPosition],
  );

  useEffect(() => {
    const scene = sceneRef.current;
    if (!scene) return;

    const measure = () => {
      const rect = scene.getBoundingClientRect();
      const width = rect.width || scene.clientWidth;
      const height = rect.height || scene.clientHeight;

      if (width <= 0 || height <= 0) return;

      setSceneSize((current) =>
        current.width === width && current.height === height
          ? current
          : { width, height },
      );
    };

    measure();

    if (typeof ResizeObserver === 'undefined') {
      window.addEventListener('resize', measure);
      return () => window.removeEventListener('resize', measure);
    }

    const observer = new ResizeObserver(measure);
    observer.observe(scene);
    return () => observer.disconnect();
  }, [mode]);

  useEffect(
    () => () => {
      cancelCarouselAnimation();
      if (dragFrameRef.current !== null) {
        cancelAnimationFrame(dragFrameRef.current);
      }
    },
    [cancelCarouselAnimation],
  );

  const visibleWorlds = useMemo(
    () => projectVisibleWorlds(position, sceneSize.width),
    [position, sceneSize.width],
  );

  const activeWorld = getWorld(modulo(Math.round(position), WORLDS.length));

  useEffect(() => {
    const canvas = fxCanvasRef.current;
    if (!canvas || mode !== 'worlds') return;
    drawWorldEffects(canvas, visibleWorlds, sceneSize);
  }, [mode, sceneSize, visibleWorlds]);

  const stepWorlds = (direction: -1 | 1) => {
    animateTo(Math.round(positionRef.current) + direction);
  };

  const switchMode = () => {
    cancelCarouselAnimation();
    setMode((value) => (value === 'worlds' ? 'signals' : 'worlds'));
  };

  const handleScenePointerDown = (event: ReactPointerEvent<HTMLDivElement>) => {
    if (event.pointerType === 'mouse' && event.button !== 0) return;

    const target = event.target;
    if (!(target instanceof Element)) return;
    if (target.closest('.home-world-arrow')) return;

    const pressedWorld = target.closest<HTMLElement>('[data-world-logical]');
    const logical = pressedWorld?.dataset.worldLogical;

    cancelCarouselAnimation();
    dragRef.current = {
      pointerId: event.pointerId,
      startX: event.clientX,
      lastX: event.clientX,
      startPosition: positionRef.current,
      pressedLogical: logical === undefined ? null : Number(logical),
    };

    event.currentTarget.dataset.dragging = 'true';
    try {
      event.currentTarget.setPointerCapture(event.pointerId);
    } catch {
      // Pointer capture can be unavailable in synthetic/test environments.
    }
  };

  const handleScenePointerMove = (event: ReactPointerEvent<HTMLDivElement>) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) return;

    drag.lastX = event.clientX;
    if (dragFrameRef.current !== null) return;

    dragFrameRef.current = requestAnimationFrame(() => {
      dragFrameRef.current = null;
      const current = dragRef.current;
      if (!current) return;
      setCarouselPosition(
        current.startPosition -
          (current.lastX - current.startX) / WORLD_DRAG_PIXELS_PER_ITEM,
      );
    });
  };

  const finishScenePointer = (
    event: ReactPointerEvent<HTMLDivElement>,
    cancelled: boolean,
  ) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId) return;

    if (dragFrameRef.current !== null) {
      cancelAnimationFrame(dragFrameRef.current);
      dragFrameRef.current = null;
      setCarouselPosition(
        drag.startPosition -
          (event.clientX - drag.startX) / WORLD_DRAG_PIXELS_PER_ITEM,
      );
    }

    const travel = Math.abs(event.clientX - drag.startX);
    const clickedLogical = cancelled ? null : drag.pressedLogical;
    dragRef.current = null;
    delete event.currentTarget.dataset.dragging;

    if (
      travel < WORLD_CLICK_TRAVEL_THRESHOLD &&
      clickedLogical !== null &&
      Number.isFinite(clickedLogical)
    ) {
      animateTo(clickedLogical);
    } else {
      animateTo(Math.round(positionRef.current));
    }
  };

  const stageStyle = {
    '--home-world-active-color': activeWorld.color,
  } as CSSProperties;

  return (
    <section
      className="home-central-stage"
      data-home-region="central-stage"
      data-home-stage-mode={mode === 'worlds' ? 'continuity' : 'signals'}
      aria-label={t(($) => $.common.home.stage.label)}
      style={stageStyle}
    >
      <h2 className="home-visually-hidden">
        {mode === 'worlds'
          ? t(($) => $.common.home.stage.continuity)
          : t(($) => $.common.home.stage.signals)}
      </h2>

      <div className="home-stage-dock" aria-label="Cambia superficie centrale">
        <button
          className="home-stage-mode-arrow"
          type="button"
          onClick={switchMode}
          aria-label="Proiezione precedente"
        >
          ‹
        </button>
        <span className="home-stage-surface-label" aria-hidden="true">
          {mode === 'worlds' ? 'MONDI' : 'SINTESI'}
        </span>
        <button
          className="home-stage-mode-arrow"
          type="button"
          onClick={switchMode}
          aria-label="Proiezione successiva"
        >
          ›
        </button>
      </div>

      {mode === 'worlds' ? (
        <div
          ref={sceneRef}
          className="home-world-scene"
          onPointerDown={handleScenePointerDown}
          onPointerMove={handleScenePointerMove}
          onPointerUp={(event) => finishScenePointer(event, false)}
          onPointerCancel={(event) => finishScenePointer(event, true)}
        >
          <canvas
            ref={fxCanvasRef}
            className="home-world-fx"
            aria-hidden="true"
          />

          <div className="home-world-layer" role="list" aria-label="Mondi">
            {visibleWorlds.map((item) => (
              <button
                key={item.logical}
                className={`home-world stellar-world${item.active ? ' active' : ''}${item.world.progress !== null ? ' measurable' : ''}`}
                type="button"
                data-world-logical={item.logical}
                style={
                  {
                    '--col': item.world.color,
                    '--p': item.world.progress ?? 0,
                    transform: `translate(-50%, -50%) translate3d(${item.x}px, ${item.y}px, 0) scale(${item.scale})`,
                    opacity: item.opacity,
                    zIndex: item.zIndex,
                  } as CSSProperties
                }
                onClick={(event) => {
                  if (event.detail === 0) animateTo(item.logical);
                }}
                aria-label={item.world.name}
                aria-current={item.active ? 'true' : undefined}
                role="listitem"
              >
                <span className="stellar-node">
                  <span className="node-back" aria-hidden="true" />
                  <span className="node-halo" aria-hidden="true" />
                  <span className="node-progress" aria-hidden="true" />
                  <span className="node-content">
                    <span className="icon" aria-hidden="true">
                      <WorldIcon name={item.world.icon} />
                    </span>
                    <span className="node-name">{item.world.name}</span>
                  </span>
                </span>
              </button>
            ))}
          </div>

          <button
            className="home-world-arrow home-world-arrow-prev"
            type="button"
            onPointerDown={(event) => event.stopPropagation()}
            onClick={() => stepWorlds(-1)}
            aria-label="Mondo precedente"
          >
            ‹
          </button>
          <button
            className="home-world-arrow home-world-arrow-next"
            type="button"
            onPointerDown={(event) => event.stopPropagation()}
            onClick={() => stepWorlds(1)}
            aria-label="Mondo successivo"
          >
            ›
          </button>
        </div>
      ) : (
        <SignalStage />
      )}
    </section>
  );
}

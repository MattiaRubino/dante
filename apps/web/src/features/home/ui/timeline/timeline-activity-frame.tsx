import { useId, useLayoutEffect, useRef } from 'react';

const round = (value: number) => Math.round(value * 100) / 100;
const smooth = (value: number) => value * value * (3 - 2 * value);

/** One continuous, even-odd rim, adapted from the approved activity card prototype. */
export function activityFramePath(
  width: number,
  height: number,
): {
  d: string;
  radius: number;
} {
  const w = width;
  const h = height;
  // At compact Timeline sizes, leave a straight segment between the corners.
  const r = Math.max(1, Math.min(58, h * 0.35, w * 0.35));
  const base = Math.min(3, Math.max(1, h * 0.015));
  const left = Math.min(Math.max(base + 0.8, h * 0.06), r * 0.45);
  const rightCorner = Math.min(Math.max(base + 2.7, h * 0.04), r * 0.26);
  const rightSideRun = Math.max(0, Math.min(r * 1.24, h * 0.4, h - 2 * r));
  const bottomRun = Math.max(0, Math.min(r * 1.06, h * 0.32, w - 2 * r));
  const outside: Array<[number, number]> = [];
  const inside: Array<[number, number]> = [];

  function point(
    x: number,
    y: number,
    nx: number,
    ny: number,
    thickness: number,
  ) {
    outside.push([round(x), round(y)]);
    inside.push([round(x - nx * thickness), round(y - ny * thickness)]);
  }

  function arc(
    cx: number,
    cy: number,
    start: number,
    end: number,
    steps: number,
    thickness: (progress: number) => number,
  ) {
    for (let i = 1; i <= steps; i += 1) {
      const progress = i / steps;
      const angle = start + (end - start) * progress;
      const nx = Math.cos(angle);
      const ny = Math.sin(angle);
      point(cx + r * nx, cy + r * ny, nx, ny, thickness(progress));
    }
  }

  point(r, 0, 0, -1, base);
  point(w - r, 0, 0, -1, base);
  arc(w - r, r, -Math.PI / 2, 0, 32, () => base);

  const sideTangency = base + (rightCorner - base) * 0.7;
  const bottomTangency = base + (rightCorner - base) * 0.66;
  const peak = base + (rightCorner - base) * 0.94;
  const peakAt = 0.58;
  const ramp = (value: number) => value * 0.72 + smooth(value) * 0.28;
  const rightStart = h - r - rightSideRun;

  for (let i = 0; i <= 28; i += 1) {
    const progress = i / 28;
    point(
      w,
      rightStart + rightSideRun * progress,
      1,
      0,
      base + (sideTangency - base) * ramp(progress),
    );
  }
  arc(w - r, h - r, 0, Math.PI / 2, 96, (progress) => {
    if (progress <= peakAt) {
      return sideTangency + (peak - sideTangency) * ramp(progress / peakAt);
    }
    return (
      peak + (bottomTangency - peak) * ramp((progress - peakAt) / (1 - peakAt))
    );
  });
  for (let i = 1; i <= 24; i += 1) {
    const progress = i / 24;
    point(
      w - r - bottomRun * progress,
      h,
      0,
      1,
      bottomTangency + (base - bottomTangency) * ramp(progress),
    );
  }
  point(r, h, 0, 1, base);
  arc(
    r,
    h - r,
    Math.PI / 2,
    Math.PI,
    48,
    (progress) => base + (left - base) * smooth(progress),
  );
  point(0, r, -1, 0, left);
  arc(
    r,
    r,
    Math.PI,
    Math.PI * 1.5,
    48,
    (progress) => left - (left - base) * smooth(progress),
  );

  const path = (points: Array<[number, number]>) =>
    `${points.map(([x, y], index) => `${index ? 'L' : 'M'}${x} ${y}`).join(' ')} Z`;
  return { d: `${path(outside)} ${path(inside.reverse())}`, radius: r };
}

export function TimelineActivityFrame() {
  const frameRef = useRef<SVGSVGElement>(null);
  const gradientId = useId().replaceAll(':', '');

  useLayoutEffect(() => {
    const frame = frameRef.current;
    const card = frame?.parentElement;
    const rim = frame?.querySelector('path');
    if (!frame || !card || !rim) return;

    const draw = () => {
      const { width, height } = card.getBoundingClientRect();
      if (width < 2 || height < 2) return;
      const { d, radius } = activityFramePath(width, height);
      rim.setAttribute('d', d);
      frame.setAttribute('viewBox', `0 0 ${width} ${height}`);
      card.style.borderRadius = `${radius}px`;
    };

    draw();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(draw);
    observer.observe(card);
    return () => observer.disconnect();
  }, []);

  return (
    <svg
      ref={frameRef}
      className="timeline-activity-frame"
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" />
          <stop offset="44%" />
          <stop offset="76%" />
          <stop offset="100%" />
        </linearGradient>
      </defs>
      <path
        className="timeline-activity-frame__rim"
        fill={`url(#${gradientId})`}
        fillRule="evenodd"
      />
    </svg>
  );
}

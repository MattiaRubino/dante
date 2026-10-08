import { useId, useLayoutEffect, useRef, useState } from 'react';

// The two ribbons retain the selected reference's exact geometry. The second
// is the first rotated through 180 degrees, so their points stay paired.
const ribbon = `M 8 218
  C 18 192, 30 160, 43 126
  C 52 102, 60 80, 66 61
  C 71 45, 77 35, 87 30
  C 91 28, 96 27, 102 27
  L 727 27
  C 737 27, 743 32, 744 40
  C 745 46, 743 52, 741 58
  L 679 219
  L 737 57
  C 739 51, 740 46, 739 42
  C 738 35, 733 32, 726 32
  L 103 32
  C 95 32, 89 36, 84 43
  C 80 49, 77 56, 73 66
  C 66 86, 58 108, 49 132
  C 36 166, 24 194, 8 218 Z`;

export function eventFrameGeometry(width: number, height: number) {
  const w = Math.max(1, width);
  const h = Math.max(1, height);
  const sx = w / 772;
  // Scale the original short-card corners within a fixed pixel band. Only
  // the straight middle can grow when a Schedule spans several hours.
  const top = Math.min(4, h * 0.035);
  const tail = Math.min(70, Math.max(22, h * 0.26));
  const sy = Math.max(0.01, (tail - top) / (218 - 27));
  const offset = top - 27 * sy;
  const leftTop = 8 * sx;
  const leftBottom = w - 679 * sx;
  const rightTop = 679 * sx;
  const rightBottom = w - 8 * sx;
  const bridge = h > 2 * tail + 8
    ? `M ${leftTop} ${tail} L ${leftTop} ${h - tail - 16} L ${leftBottom} ${h - tail}
       M ${rightTop} ${tail} L ${rightTop} ${h - tail - 16} L ${rightBottom} ${h - tail}`
    : '';
  return {
    topTransform: `matrix(${sx} 0 0 ${sy} 0 ${offset})`,
    bottomTransform: `matrix(${-sx} 0 0 ${-sy} ${w} ${h - offset})`,
    bridge,
  };
}

export function TimelineEventFrame() {
  const id = useId().replaceAll(':', '');
  const ref = useRef<SVGSVGElement>(null);
  const [size, setSize] = useState({ width: 250, height: 100 });
  useLayoutEffect(() => {
    const card = ref.current?.parentElement;
    if (!card) return;
    const measure = () => {
      const { width, height } = card.getBoundingClientRect();
      if (width > 1 && height > 1) {
        setSize((current) => current.width === width && current.height === height
          ? current : { width, height });
      }
    };
    measure();
    if (typeof ResizeObserver === 'undefined') return;
    const observer = new ResizeObserver(measure);
    observer.observe(card);
    return () => observer.disconnect();
  }, []);
  const { topTransform, bottomTransform, bridge } = eventFrameGeometry(
    size.width,
    size.height,
  );
  return (
    <svg
      ref={ref}
      className="timeline-event-frame"
      viewBox={`0 0 ${size.width} ${size.height}`}
      aria-hidden="true"
      focusable="false"
    >
      <defs>
        <linearGradient id={`${id}-paint`} x1="0" y1="1" x2="1" y2="0">
          <stop
            offset="0"
            stopColor="color-mix(in srgb, var(--timeline-group-color) 91%, #ff4712)"
          />
          <stop
            offset="0.23"
            stopColor="color-mix(in srgb, var(--timeline-group-color) 89%, #ff5908)"
          />
          <stop
            offset="0.5"
            stopColor="color-mix(in srgb, var(--timeline-group-color) 86%, #ff7000)"
          />
          <stop
            offset="0.82"
            stopColor="color-mix(in srgb, var(--timeline-group-color) 84%, #ff7900)"
          />
          <stop
            offset="1"
            stopColor="color-mix(in srgb, var(--timeline-group-color) 78%, #ffa000)"
          />
        </linearGradient>
        <filter
          id={`${id}-glow`}
          x="-12%"
          y="-18%"
          width="124%"
          height="136%"
          colorInterpolationFilters="sRGB"
        >
          <feGaussianBlur stdDeviation="2.2" result="blur" />
          <feComponentTransfer in="blur" result="soft">
            <feFuncA type="linear" slope="0.52" />
          </feComponentTransfer>
          <feMerge>
            <feMergeNode in="soft" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <path id={`${id}-ribbon`} d={ribbon} />
      </defs>
      <use
        href={`#${id}-ribbon`}
        transform={topTransform}
        fill={`url(#${id}-paint)`}
        filter={`url(#${id}-glow)`}
      />
      <use
        href={`#${id}-ribbon`}
        transform={bottomTransform}
        fill={`url(#${id}-paint)`}
        filter={`url(#${id}-glow)`}
      />
      {bridge ? (
        <path
          d={bridge}
          fill="none"
          stroke={`url(#${id}-paint)`}
          strokeWidth="1.6"
          strokeLinejoin="round"
          filter={`url(#${id}-glow)`}
        />
      ) : null}
    </svg>
  );
}

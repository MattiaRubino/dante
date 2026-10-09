import { useId, useLayoutEffect, useRef, useState } from 'react';

// Same path construction as the approved manual resize prototype. One ribbon
// and an exact 180-degree counterpart; each side is a straight, single path.
export function eventFrameGeometry(width: number, height: number) {
  const w = Math.max(1, width);
  const h = Math.max(1, height);
  const sx = Math.min(1, w / 772);
  const sy = Math.min(1, h / 305);
  const extraW = Math.max(0, w - 772);
  const extraH = Math.max(0, h - 305);
  const q = (value: number) => Math.round(value * 100) / 100;
  const lx = (x: number) => q(x * sx);
  const rx = (x: number) => q((x + extraW) * sx);
  const ty = (y: number) => q(y * sy);
  const by = (y: number) => q((y + extraH) * sy);

  const ribbon = [
    `M ${lx(8)} ${by(218)}`,
    `L ${lx(66)} ${ty(61)}`,
    `C ${lx(71)} ${ty(45)}, ${lx(77)} ${ty(35)}, ${lx(87)} ${ty(30)}`,
    `C ${lx(91)} ${ty(28)}, ${lx(96)} ${ty(27)}, ${lx(102)} ${ty(27)}`,
    `L ${rx(727)} ${ty(27)}`,
    `C ${rx(737)} ${ty(27)}, ${rx(743)} ${ty(32)}, ${rx(744)} ${ty(40)}`,
    `C ${rx(745)} ${ty(46)}, ${rx(743)} ${ty(52)}, ${rx(741)} ${ty(58)}`,
    `L ${rx(679)} ${by(219)}`,
    `L ${rx(737)} ${ty(57)}`,
    `C ${rx(739)} ${ty(51)}, ${rx(740)} ${ty(46)}, ${rx(739)} ${ty(42)}`,
    `C ${rx(738)} ${ty(35)}, ${rx(733)} ${ty(32)}, ${rx(726)} ${ty(32)}`,
    `L ${lx(103)} ${ty(32)}`,
    `C ${lx(95)} ${ty(32)}, ${lx(89)} ${ty(36)}, ${lx(84)} ${ty(43)}`,
    `C ${lx(80)} ${ty(49)}, ${lx(77)} ${ty(56)}, ${lx(73)} ${ty(66)}`,
    `L ${lx(8)} ${by(218)}`,
    'Z',
  ].join(' ');
  const mirrorY = h <= 305 ? 281 * sy : h - 24;
  return { ribbon, mirrorTransform: `translate(${q(w)} ${q(mirrorY)}) scale(-1 -1)` };
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
  const { ribbon, mirrorTransform } = eventFrameGeometry(size.width, size.height);
  return (
    <svg ref={ref} className="timeline-event-frame"
      viewBox={`0 0 ${size.width} ${size.height}`}
      preserveAspectRatio="none" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id={`${id}-paint`} x1="0" y1="1" x2="1" y2="0">
          <stop offset="0" stopColor="color-mix(in srgb, var(--timeline-group-color) 91%, #ff4712)" />
          <stop offset="0.23" stopColor="color-mix(in srgb, var(--timeline-group-color) 89%, #ff5908)" />
          <stop offset="0.5" stopColor="color-mix(in srgb, var(--timeline-group-color) 86%, #ff7000)" />
          <stop offset="0.82" stopColor="color-mix(in srgb, var(--timeline-group-color) 84%, #ff7900)" />
          <stop offset="1" stopColor="color-mix(in srgb, var(--timeline-group-color) 78%, #ffa000)" />
        </linearGradient>
        <filter id={`${id}-glow`} x="-12%" y="-18%" width="124%" height="136%"
          colorInterpolationFilters="sRGB">
          <feGaussianBlur stdDeviation="2.2" result="blur" />
          <feComponentTransfer in="blur" result="soft">
            <feFuncA type="linear" slope="0.52" />
          </feComponentTransfer>
          <feMerge><feMergeNode in="soft" /><feMergeNode in="SourceGraphic" /></feMerge>
        </filter>
        <path id={`${id}-ribbon`} d={ribbon} />
      </defs>
      <use href={`#${id}-ribbon`} fill={`url(#${id}-paint)`} filter={`url(#${id}-glow)`} />
      <use href={`#${id}-ribbon`} transform={mirrorTransform}
        fill={`url(#${id}-paint)`} filter={`url(#${id}-glow)`} />
    </svg>
  );
}

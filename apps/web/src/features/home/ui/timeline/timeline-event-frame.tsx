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
  // The source art is 772×305. Short cards retain its exact original shape.
  // Taller cards insert a stretched horizontal slice through the unchanged
  // artwork, so the sides grow without moving either corner or adding joins.
  const originalHeight = (w * 305) / 772;
  const addedHeight = h <= originalHeight + 4 ? 0 : h - originalHeight;
  const topHeight = (Math.min(h, originalHeight) * 140.5) / 305;
  return {
    addedHeight,
    topHeight,
    bottomHeight: h - topHeight - addedHeight,
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
  const { addedHeight, topHeight, bottomHeight } = eventFrameGeometry(
    size.width,
    size.height,
  );
  const ribbons = <>
    <use href={`#${id}-ribbon`} fill={`url(#${id}-paint)`} filter={`url(#${id}-glow)`} />
    <use href={`#${id}-ribbon`} transform="translate(772 281) scale(-1 -1)"
      fill={`url(#${id}-paint)`} filter={`url(#${id}-glow)`} />
  </>;
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
      {addedHeight === 0 ? (
        <svg width={size.width} height={size.height} viewBox="0 0 772 305"
          preserveAspectRatio="none">{ribbons}</svg>
      ) : (
        <>
          <svg width={size.width} height={topHeight} viewBox="0 0 772 140.5"
            preserveAspectRatio="none">{ribbons}</svg>
          <svg y={topHeight} width={size.width} height={addedHeight}
            viewBox="0 140 772 1" preserveAspectRatio="none">{ribbons}</svg>
          <svg y={topHeight + addedHeight} width={size.width} height={bottomHeight}
            viewBox="0 140.5 772 164.5" preserveAspectRatio="none">{ribbons}</svg>
        </>
      )}
    </svg>
  );
}

export const TIMELINE_REDUCED_MOTION_QUERY =
  '(prefers-reduced-motion: reduce)' as const;

export function timelineEffectiveScrollBehavior(
  requested: ScrollBehavior,
  reduceMotion: boolean,
): ScrollBehavior {
  return reduceMotion && requested === 'smooth' ? 'auto' : requested;
}

export function timelinePrefersReducedMotion(): boolean {
  return (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia(TIMELINE_REDUCED_MOTION_QUERY).matches
  );
}

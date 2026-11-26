/**
 * Factual Session interval editing rules.
 *
 * Stored intervals remain immutable until explicitly corrected; this module
 * only returns proposals for a single edited field or an unsaved interval.
 * All bounds use absolute milliseconds so the UI's time zone and DST are
 * handled by its existing Temporal conversion layer.
 */
export const SESSION_MINUTE_MS = 60_000;

export type SessionSpan = Readonly<{ start: number; end: number }>;
export type SessionBoundary = 'start' | 'end';
export type SessionBounds = Readonly<{ min: number; max: number }>;

export function sessionBounds(input: Readonly<{
  boundary: SessionBoundary;
  current: SessionSpan;
  previous?: SessionSpan | null;
  next?: SessionSpan | null;
  parent?: SessionSpan | null;
  now: number;
}>): SessionBounds | null {
  const { boundary, current, previous, next, parent, now } = input;
  const floorNow = Math.floor(now / SESSION_MINUTE_MS) * SESSION_MINUTE_MS;
  if (
    !Number.isFinite(current.start) ||
    !Number.isFinite(current.end) ||
    (parent && (!Number.isFinite(parent.start) || !Number.isFinite(parent.end)))
  ) return null;

  const parentMin = parent?.start ?? Number.NEGATIVE_INFINITY;
  const parentMax = parent?.end ?? Number.POSITIVE_INFINITY;
  const before = previous?.end === undefined
    ? Number.NEGATIVE_INFINITY
    : previous.end + SESSION_MINUTE_MS;
  const after = next?.start === undefined
    ? Number.POSITIVE_INFINITY
    : next.start - SESSION_MINUTE_MS;

  const min = boundary === 'start'
    ? Math.max(parentMin, before)
    : Math.max(current.start + SESSION_MINUTE_MS, parentMin + SESSION_MINUTE_MS);
  const max = boundary === 'start'
    ? Math.min(current.end - SESSION_MINUTE_MS, parentMax - SESSION_MINUTE_MS, floorNow - SESSION_MINUTE_MS)
    : Math.min(parentMax, floorNow, after);
  return min <= max ? { min, max } : null;
}

export function normalizeSessionBoundary(
  value: number,
  bounds: SessionBounds | null,
): number | null {
  if (bounds === null || !Number.isFinite(value)) return null;
  return Math.max(bounds.min, Math.min(bounds.max, value));
}

export function nextFactualInterval(input: Readonly<{
  previousEnd: number;
  now: number;
  parentEnd?: number;
  desiredMinutes?: number;
}>): SessionSpan | null {
  const latest = Math.min(
    Math.floor(input.now / SESSION_MINUTE_MS) * SESSION_MINUTE_MS,
    input.parentEnd ?? Number.POSITIVE_INFINITY,
  );
  const start = input.previousEnd + SESSION_MINUTE_MS;
  if (!Number.isFinite(start) || start + SESSION_MINUTE_MS > latest) return null;
  const minutes = Math.max(1, input.desiredMinutes ?? 30);
  return {
    start,
    end: Math.min(latest, start + minutes * SESSION_MINUTE_MS),
  };
}

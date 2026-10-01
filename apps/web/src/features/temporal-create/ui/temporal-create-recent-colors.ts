import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';

export const TEMPORAL_CREATE_DEFAULT_COLOR = '#EA5C12';
export const TEMPORAL_CREATE_RECENT_COLORS_KEY =
  'dante.temporal-create.recent-used-colors';

function normalizeColor(value: string): string | null {
  const canonical = value.trim().toUpperCase();
  return /^#[0-9A-F]{6}$/.test(canonical) ? canonical : null;
}

export function temporalCreateEffectiveColor(
  draft: TemporalCreateU2AuthoringDraft,
): string {
  const candidate =
    draft.lifeArea.kind === 'none'
      ? draft.itemColorCode
      : draft.lifeArea.colorCode;
  return normalizeColor(candidate ?? '') ?? TEMPORAL_CREATE_DEFAULT_COLOR;
}

export function readTemporalCreateRecentUsedColors(): readonly string[] {
  try {
    const raw = window.localStorage.getItem(TEMPORAL_CREATE_RECENT_COLORS_KEY);
    if (!raw) return Object.freeze([]);
    const parsed: unknown = JSON.parse(raw);
    if (!Array.isArray(parsed)) return Object.freeze([]);
    return Object.freeze(
      parsed
        .map((value) => (typeof value === 'string' ? normalizeColor(value) : null))
        .filter((value): value is string => value !== null)
        .slice(0, 3),
    );
  } catch {
    return Object.freeze([]);
  }
}

export function rememberTemporalCreateUsedColor(colorCode: string): void {
  const canonical = normalizeColor(colorCode);
  if (canonical === null) return;
  const current = readTemporalCreateRecentUsedColors();
  const next = Object.freeze(
    [canonical, ...current.filter((color) => color !== canonical)].slice(0, 3),
  );
  try {
    window.localStorage.setItem(
      TEMPORAL_CREATE_RECENT_COLORS_KEY,
      JSON.stringify(next),
    );
  } catch {
    // Recent colors are a local UI convenience only.
  }
}

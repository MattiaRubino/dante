import type {
  TimelineGroup,
  TimelineSemanticTone,
} from './timeline-types';

export type TimelineLocalContextResult = Readonly<{
  group: TimelineGroup;
  created: boolean;
}>;

function normalizeLabel(label: string): string {
  return label.trim().replace(/\s+/g, ' ');
}

function comparableLabel(label: string): string {
  return normalizeLabel(label).toLocaleLowerCase();
}

function slugify(label: string): string {
  return normalizeLabel(label)
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function createTimelineLocalContext(
  groups: readonly TimelineGroup[],
  label: string,
  tone: TimelineSemanticTone,
): TimelineLocalContextResult {
  const normalized = normalizeLabel(label);
  const existing = groups.find(
    (group) => comparableLabel(group.label) === comparableLabel(normalized),
  );
  if (existing) {
    return Object.freeze({ group: existing, created: false });
  }

  const stem = slugify(normalized) || 'context';
  const baseId = `local-context:${stem}`;
  const occupied = new Set(groups.map((group) => group.id));
  let id = baseId;
  let suffix = 2;
  while (occupied.has(id)) {
    id = `${baseId}-${suffix}`;
    suffix += 1;
  }

  return Object.freeze({
    group: Object.freeze({ id, label: normalized, tone }),
    created: true,
  });
}

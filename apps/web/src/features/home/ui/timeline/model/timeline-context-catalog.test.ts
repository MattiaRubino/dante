import { describe, expect, it } from 'vitest';

import { createTimelineLocalContext } from './timeline-context-catalog';
import type { TimelineGroup } from './timeline-types';

const GROUPS: readonly TimelineGroup[] = Object.freeze([
  { id: 'focus', label: 'Focus / lavoro profondo', tone: 'focus' },
  { id: 'studio', label: 'Studio', tone: 'creative' },
  {
    id: 'local-context:studio-2',
    label: 'Studio secondario',
    tone: 'personal',
  },
]);

describe('Timeline local context catalog', () => {
  it('reuses an existing context by normalized label', () => {
    const result = createTimelineLocalContext(GROUPS, '  STUDIO  ', 'urgent');

    expect(result.created).toBe(false);
    expect(result.group).toBe(GROUPS[1]);
  });

  it('creates a deterministic local id without pretending server identity', () => {
    const result = createTimelineLocalContext(
      GROUPS,
      'Progetto Àlpha',
      'focus',
    );

    expect(result).toEqual({
      created: true,
      group: {
        id: 'local-context:progetto-alpha',
        label: 'Progetto Àlpha',
        tone: 'focus',
      },
    });
  });

  it('adds a suffix only when an id is already occupied', () => {
    const result = createTimelineLocalContext(
      [
        ...GROUPS,
        {
          id: 'local-context:nuovo',
          label: 'Nome diverso',
          tone: 'meeting',
        },
      ],
      'Nuovo',
      'health',
    );

    expect(result.group.id).toBe('local-context:nuovo-2');
  });
});

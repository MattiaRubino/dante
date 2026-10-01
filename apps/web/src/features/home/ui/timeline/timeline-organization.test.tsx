import { describe, expect, it } from 'vitest';

import type { OrganizationSnapshot } from '../../../temporal/remote-organization';
import {
  canonicalOrganizationGroups,
  LEGACY_UNASSIGNED_GROUP,
} from './timeline-organization';

const AREA_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const UNASSIGNED_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';

function snapshot(
  overrides: Partial<OrganizationSnapshot> = {},
): OrganizationSnapshot {
  return {
    areas: [
      {
        ref: AREA_REF,
        name: 'Lavoro',
        revision: 1,
        sortOrder: 0,
        archived: false,
        hidden: true,
        iconCode: null,
        colorCode: '#F4C95D',
      },
    ],
    assignments: [
      {
        kind: 'event',
        itemRef: '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d',
        areaRef: AREA_REF,
        revision: 1,
      },
    ],
    unassigned: [],
    tags: [],
    tagEdges: [],
    ...overrides,
  };
}

describe('Timeline organization groups', () => {
  it('retains canonical Life Area revision/color metadata without manufacturing Personal', () => {
    expect(canonicalOrganizationGroups(snapshot())).toEqual([
      {
        id: AREA_REF,
        label: 'Lavoro',
        tone: 'personal',
        organizationRevision: 1,
        colorCode: '#F4C95D',
        hidden: true,
        archived: false,
      },
    ]);
  });

  it('keeps unassigned grouping neutral while retaining each item color', () => {
    const groups = canonicalOrganizationGroups(
      snapshot({
        assignments: [],
        unassigned: [
          {
            kind: 'event',
            itemRef: UNASSIGNED_REF,
            title: 'Storico',
            colorCode: '#EA5C12',
          },
        ],
      }),
    );
    expect(groups.at(-1)).toMatchObject({
      id: LEGACY_UNASSIGNED_GROUP,
      label: 'Senza Life Area',
      itemColorCodes: {
        [`event:${UNASSIGNED_REF}`]: '#EA5C12',
      },
    });
    expect(groups.at(-1)?.colorCode).toBeUndefined();
    expect(groups.some((group) => group.label === 'Personale')).toBe(false);
  });
});

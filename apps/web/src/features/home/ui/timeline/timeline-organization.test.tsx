import { describe, expect, it } from 'vitest';

import type { OrganizationSnapshot } from '../../../temporal/remote-organization';
import {
  canonicalOrganizationGroups,
  LEGACY_UNASSIGNED_GROUP,
} from './timeline-organization';

const AREA_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';

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
        colorCode: null,
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
  it('retains the real hidden Life Area as canonical group instead of manufacturing Personal', () => {
    expect(canonicalOrganizationGroups(snapshot())).toEqual([
      {
        id: AREA_REF,
        label: 'Lavoro',
        tone: 'personal',
        hidden: true,
        archived: false,
      },
    ]);
  });

  it('makes legacy/unassigned state explicit rather than assigning an invented default area', () => {
    const groups = canonicalOrganizationGroups(
      snapshot({
        assignments: [],
        unassigned: [
          {
            kind: 'event',
            itemRef: '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d',
            title: 'Storico',
          },
        ],
      }),
    );
    expect(groups.at(-1)).toMatchObject({
      id: LEGACY_UNASSIGNED_GROUP,
      label: 'Senza Life Area',
    });
    expect(groups.some((group) => group.label === 'Personale')).toBe(false);
  });
});

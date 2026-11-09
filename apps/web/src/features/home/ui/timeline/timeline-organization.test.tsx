import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalTimelineItem } from '../../../temporal/timeline-read';

import type { OrganizationSnapshot } from '../../../temporal/remote-organization';
import {
  canonicalOrganizationGroups,
  canonicalItemLifeAreaGroup,
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

  // Regression 2026-11-09: "Solo questa istanza" was saved correctly in
  // the Event occurrence but its card still used the recurring source's
  // assigned Life Area (and therefore its old color). These three variants
  // distinguish inheritance, replacement, and explicit removal.
  it('projects an Event occurrence local Life Area instead of the source assignment', () => {
    const eventRef = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
    const areaNew = '0199a8c0-6e74-7bc0-8ad0-a2f403f5617d';
    const assignments = new Map([[`event:${eventRef}`, AREA_REF]]);
    const item = {
      kind: 'scheduled_occurrence',
      occurrenceRef: '0199a8c0-6e75-7bc0-8ad0-a2f403f5617d',
      sourceKind: 'event',
      sourceNativeRef: eventRef,
      title: 'Event solo questa',
      coordinate: null,
      scheduleRef: '0199a8c0-6e76-7bc0-8ad0-a2f403f5617d',
      placementMaterialStateRef: '0199a8c0-6e77-7bc0-8ad0-a2f403f5617d',
      temporalForm: 'date-span',
      startDate: Temporal.PlainDate.from('2026-11-10'),
      endDateExclusive: Temporal.PlainDate.from('2026-11-11'),
    } as const satisfies TemporalTimelineItem;

    expect(canonicalItemLifeAreaGroup(item, assignments)).toBe(AREA_REF);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, lifeAreaOverridePresent: true, lifeAreaOverrideRef: areaNew },
        assignments,
      ),
    ).toBe(areaNew);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, lifeAreaOverridePresent: true, lifeAreaOverrideRef: null },
        assignments,
      ),
    ).toBe(LEGACY_UNASSIGNED_GROUP);
  });

  // Regression 2026-11-09: the converted Event's first physical Schedule
  // is represented as "scheduled_event", not "scheduled_occurrence".
  // It must obey the identical local override when "Solo questa" edits it.
  it('projects the converted recurring Event physical-first Schedule override', () => {
    const eventRef = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
    const assignments = new Map([[`event:${eventRef}`, AREA_REF]]);
    const item = {
      kind: 'scheduled_event',
      eventRef,
      scheduleRef: '0199a8c0-6e76-7bc0-8ad0-a2f403f5617d',
      placementMaterialStateRef: '0199a8c0-6e77-7bc0-8ad0-a2f403f5617d',
      title: 'Event prima istanza',
      temporalForm: 'date-span',
      startDate: Temporal.PlainDate.from('2026-11-10'),
      endDateExclusive: Temporal.PlainDate.from('2026-11-11'),
    } as const satisfies TemporalTimelineItem;

    expect(canonicalItemLifeAreaGroup(item, assignments)).toBe(AREA_REF);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, lifeAreaOverridePresent: true, lifeAreaOverrideRef: null },
        assignments,
      ),
    ).toBe(LEGACY_UNASSIGNED_GROUP);
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

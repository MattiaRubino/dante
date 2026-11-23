import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalTimelineItem } from '../../../temporal/timeline-read';

import type { OrganizationSnapshot } from '../../../temporal/remote-organization';
import {
  canonicalActivityPresentationColor,
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

  it('recolors the shared Life Area group for Activity and Event cards', () => {
    const current = snapshot({
      areas: [{ ...snapshot().areas[0]!, revision: 2, colorCode: '#33B679' }],
      assignments: [
        ...snapshot().assignments,
        {
          kind: 'activity',
          itemRef: UNASSIGNED_REF,
          areaRef: AREA_REF,
          revision: 1,
        },
      ],
    });
    const groups = canonicalOrganizationGroups(current);
    expect(groups.find((group) => group.id === AREA_REF)?.colorCode).toBe(
      '#33B679',
    );
    expect(
      current.assignments.map(
        (assignment) =>
          groups.find((group) => group.id === assignment.areaRef)?.colorCode,
      ),
    ).toEqual(['#33B679', '#33B679']);
  });

  it('gives the Session card the Activity color from its assigned Area or its own unassigned color', () => {
    const assigned = snapshot({
      assignments: [
        {
          kind: 'activity',
          itemRef: UNASSIGNED_REF,
          areaRef: AREA_REF,
          revision: 1,
        },
      ],
    });
    const assignments = new Map(
      assigned.assignments.map((entry) => [
        `${entry.kind}:${entry.itemRef}`,
        entry.areaRef,
      ]),
    );
    expect(
      canonicalActivityPresentationColor(
        UNASSIGNED_REF,
        canonicalOrganizationGroups(assigned),
        assignments,
      ),
    ).toBe('#F4C95D');

    const unassigned = snapshot({
      assignments: [],
      unassigned: [
        {
          kind: 'activity',
          itemRef: UNASSIGNED_REF,
          title: 'Studio',
          colorCode: '#EA5C12',
        },
      ],
    });
    expect(
      canonicalActivityPresentationColor(
        UNASSIGNED_REF,
        canonicalOrganizationGroups(unassigned),
        new Map(),
      ),
    ).toBe('#EA5C12');
    expect(
      canonicalActivityPresentationColor(UNASSIGNED_REF, null, new Map()),
    ).toBeNull();
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
        {
          ...item,
          lifeAreaOverridePresent: true,
          lifeAreaOverrideRef: areaNew,
        },
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

  it('uses a recurrence segment area for all cards and lets a local exception win', () => {
    const previousArea = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
    const segmentArea = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';
    const localArea = '0199a8c0-6e74-7bc0-8ad0-a2f403f5617d';
    const sourceNativeRef = '0199a8c0-6e75-7bc0-8ad0-a2f403f5617d';
    const assignments = new Map([[`event:${sourceNativeRef}`, previousArea]]);
    const item = {
      kind: 'expected_occurrence',
      occurrenceRef: '0199a8c0-6e76-7bc0-8ad0-a2f403f5617d',
      sourceKind: 'event',
      sourceNativeRef,
      title: 'Istanza futura',
      coordinate: {
        familyCode: 'calendar-wall-clock',
        generatedDate: Temporal.PlainDate.from('2026-11-22'),
        generatedWallTime: null,
        clockBasis: 'named-zone',
        zoneId: 'Europe/Rome',
        resolvedAt: null,
      },
      seriesLifeAreaPresent: true,
      seriesLifeAreaRef: segmentArea,
    } as const satisfies TemporalTimelineItem;

    expect(canonicalItemLifeAreaGroup(item, assignments)).toBe(segmentArea);
    expect(
      canonicalItemLifeAreaGroup(
        {
          ...item,
          lifeAreaOverridePresent: true,
          lifeAreaOverrideRef: localArea,
        },
        assignments,
      ),
    ).toBe(localArea);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, lifeAreaOverridePresent: true, lifeAreaOverrideRef: null },
        assignments,
      ),
    ).toBe(LEGACY_UNASSIGNED_GROUP);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, seriesLifeAreaRef: null },
        assignments,
      ),
    ).toBe(LEGACY_UNASSIGNED_GROUP);
    expect(
      canonicalItemLifeAreaGroup(
        { ...item, seriesLifeAreaPresent: false, seriesLifeAreaRef: null },
        assignments,
      ),
    ).toBe(previousArea);
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
      label: 'Senza Area',
      itemColorCodes: {
        [`event:${UNASSIGNED_REF}`]: '#EA5C12',
      },
    });
    expect(groups.at(-1)?.colorCode).toBeUndefined();
    expect(groups.some((group) => group.label === 'Personale')).toBe(false);
  });
});

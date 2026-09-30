import { useEffect, useMemo, useState } from 'react';

import './timeline-truth-inspector.css';

import { ActualRealizationControls } from './actual-realization-controls';
import { AdvancedRecurrenceControls } from './advanced-recurrence-controls';
import { ConditionalTemporalControls } from './conditional-temporal-controls';
import { useTemporalTimelineRuntime } from './timeline-runtime-boundary';
import type {
  TemporalTimelineItem,
  TemporalTimelineWindow,
} from './timeline-read';

export type TimelineTruthSubject = Readonly<{
  key: string;
  kind: 'activity' | 'event' | 'occurrence';
  ref: string;
  title: string;
  timelineLabel: string;
  recurrenceOwner: Readonly<{
    kind: 'routine' | 'event';
    ref: string;
  }> | null;
}>;

function timelineItemLabel(item: TemporalTimelineItem): string {
  if (item.kind === 'expected_occurrence') {
    switch (item.coordinate.familyCode) {
      case 'calendar-wall-clock':
        return item.coordinate.generatedWallTime === null
          ? item.coordinate.generatedDate.toString()
          : `${item.coordinate.generatedDate} ${item.coordinate.generatedWallTime}`;
      case 'elapsed-interval':
        return item.coordinate.expectedAt.toString();
      case 'quota-per-period':
        return `${item.coordinate.periodStartDate}–${item.coordinate.periodEndDateExclusive}`;
      case 'cyclic-positional':
        return `${item.coordinate.generatedDate} · ciclo ${item.coordinate.positionIndex}`;
    }
  }

  switch (item.temporalForm) {
    case 'date-span':
      return item.startDate.toString();
    case 'floating-local':
    case 'named-zone-local':
      return item.startsLocalAt.toString();
    case 'absolute':
      return item.displayStartsLocalAt.toString();
    case 'coarse-local-period':
      return `${item.localDate} · ${item.period}`;
  }
}

export function timelineTruthSubjects(
  window: TemporalTimelineWindow | null,
): readonly TimelineTruthSubject[] {
  if (window === null || window.kind === 'empty') return [];

  const subjects = new Map<string, TimelineTruthSubject>();
  for (const item of window.items) {
    const subject =
      item.kind === 'scheduled_activity'
        ? ({
            key: `activity:${item.activityRef}`,
            kind: 'activity' as const,
            ref: item.activityRef,
            title: item.title,
            timelineLabel: timelineItemLabel(item),
            recurrenceOwner: null,
          } satisfies TimelineTruthSubject)
        : item.kind === 'scheduled_event'
          ? ({
              key: `event:${item.eventRef}`,
              kind: 'event' as const,
              ref: item.eventRef,
              title: item.title,
              timelineLabel: timelineItemLabel(item),
              recurrenceOwner: { kind: 'event' as const, ref: item.eventRef },
            } satisfies TimelineTruthSubject)
          : ({
              key: `occurrence:${item.occurrenceRef}`,
              kind: 'occurrence' as const,
              ref: item.occurrenceRef,
              title: item.title,
              timelineLabel: timelineItemLabel(item),
              recurrenceOwner: {
                kind: item.sourceKind,
                ref: item.sourceNativeRef,
              },
            } satisfies TimelineTruthSubject);
    subjects.set(subject.key, subject);
  }
  return [...subjects.values()];
}

export function TimelineTruthInspector() {
  const { state } = useTemporalTimelineRuntime();
  const subjects = useMemo(
    () => timelineTruthSubjects(state.status === 'ready' ? state.window : null),
    [state],
  );
  const [selectedKey, setSelectedKey] = useState<string | null>(null);

  useEffect(() => {
    if (subjects.length === 0) {
      setSelectedKey(null);
      return;
    }
    if (selectedKey === null || !subjects.some((item) => item.key === selectedKey)) {
      setSelectedKey(subjects[0]?.key ?? null);
    }
  }, [selectedKey, subjects]);

  const selected =
    subjects.find((item) => item.key === selectedKey) ?? subjects[0] ?? null;

  return (
    <details className="timeline-truth-inspector" data-timeline-truth-inspector>
      <summary>Realtà / Outcome</summary>
      {selected === null ? (
        <div className="timeline-truth-inspector__body is-empty">
          <p>Nessun elemento della Timeline disponibile per lo stato reale.</p>
        </div>
      ) : (
        <div className="timeline-truth-inspector__body">
          <label>
            Elemento timeline
            <select
              aria-label="Elemento per stato reale"
              value={selected.key}
              onChange={(event) => setSelectedKey(event.currentTarget.value)}
            >
              {subjects.map((subject) => (
                <option key={subject.key} value={subject.key}>
                  {`${subject.kind} · ${subject.title} · ${subject.timelineLabel}`}
                </option>
              ))}
            </select>
          </label>
          <ActualRealizationControls
            key={`actual:${selected.key}`}
            kind={selected.kind}
            subjectRef={selected.ref}
          />
          <ConditionalTemporalControls
            key={`condition:${selected.key}`}
            kind={selected.kind}
            subjectRef={selected.ref}
          />
          {selected.recurrenceOwner === null ? null : (
            <AdvancedRecurrenceControls
              key={`${selected.recurrenceOwner.kind}:${selected.recurrenceOwner.ref}`}
              ownerKind={selected.recurrenceOwner.kind}
              sourceRef={selected.recurrenceOwner.ref}
            />
          )}
        </div>
      )}
    </details>
  );
}

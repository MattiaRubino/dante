import { useEffect, useMemo, useState } from 'react';

import './timeline-truth-inspector.css';

import { ActualRealizationControls } from './actual-realization-controls';
import { useTemporalTimelineRuntime } from './timeline-runtime-boundary';
import type { TemporalTimelineWindow } from './timeline-read';

export type TimelineTruthSubject = Readonly<{
  key: string;
  kind: 'activity' | 'event' | 'occurrence';
  ref: string;
  title: string;
}>;

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
          } satisfies TimelineTruthSubject)
        : item.kind === 'scheduled_event'
          ? ({
              key: `event:${item.eventRef}`,
              kind: 'event' as const,
              ref: item.eventRef,
              title: item.title,
            } satisfies TimelineTruthSubject)
          : ({
              key: `occurrence:${item.occurrenceRef}`,
              kind: 'occurrence' as const,
              ref: item.occurrenceRef,
              title: item.title,
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

  if (subjects.length === 0) return null;

  const selected = subjects.find((item) => item.key === selectedKey) ?? subjects[0];
  if (selected === undefined) return null;

  return (
    <details className="timeline-truth-inspector" data-timeline-truth-inspector>
      <summary>Realtà / Outcome</summary>
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
                {`${subject.kind} · ${subject.title}`}
              </option>
            ))}
          </select>
        </label>
        <ActualRealizationControls kind={selected.kind} subjectRef={selected.ref} />
      </div>
    </details>
  );
}

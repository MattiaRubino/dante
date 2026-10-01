import { useEffect, useState } from 'react';

import './activity-session-card-controls.css';

import {
  createRemoteTemporalSessionCapabilityDataSource,
  type TemporalSessionCapabilityDataSource,
} from './remote-session-capability-data-source';
import { SessionSubjectControls } from './session-subject-controls';

const defaultSource = createRemoteTemporalSessionCapabilityDataSource();
const capabilityReads = new Map<string, Promise<boolean>>();

function cachedCapability(activityRef: string): Promise<boolean> {
  const existing = capabilityReads.get(activityRef);
  if (existing !== undefined) {
    return existing;
  }
  const pending = defaultSource.activityEnabled(activityRef).catch((error) => {
    capabilityReads.delete(activityRef);
    throw error;
  });
  capabilityReads.set(activityRef, pending);
  return pending;
}

export function invalidateActivitySessionCardCapability(activityRef?: string): void {
  if (activityRef === undefined) {
    capabilityReads.clear();
    return;
  }
  capabilityReads.delete(activityRef);
}

export function ActivitySessionCardControls({
  activityRef,
  label,
  interactive = true,
  source = defaultSource,
}: Readonly<{
  activityRef: string;
  label: string;
  interactive?: boolean;
  source?: TemporalSessionCapabilityDataSource;
}>) {
  const [enabled, setEnabled] = useState<boolean | null>(null);

  useEffect(() => {
    let cancelled = false;
    setEnabled(null);
    const read =
      source === defaultSource
        ? cachedCapability(activityRef)
        : source.activityEnabled(activityRef);
    void read
      .then((value) => {
        if (!cancelled) {
          setEnabled(value);
        }
      })
      .catch(() => {
        if (!cancelled) {
          // Fail closed: an unread capability must never expose a runtime command.
          setEnabled(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [activityRef, source]);

  if (enabled !== true) {
    return null;
  }

  return (
    <div
      className="timeline-activity-session-card-controls"
      data-timeline-activity-session-controls={activityRef}
    >
      <SessionSubjectControls
        kind="activity"
        subjectRef={activityRef}
        label={label}
        variant="card"
        interactive={interactive}
      />
    </div>
  );
}

import { useEffect, useState } from 'react';

import './activity-session-card-controls.css';

import {
  createRemoteTemporalSessionCapabilityDataSource,
  type TemporalSessionCapabilityDataSource,
  type SessionCaptureMode,
} from './remote-session-capability-data-source';
import { SessionSubjectControls } from './session-subject-controls';

const defaultSource = createRemoteTemporalSessionCapabilityDataSource();
const capabilityReads = new Map<string, Promise<SessionCaptureMode>>();

function cachedCapability(activityRef: string): Promise<SessionCaptureMode> {
  const existing = capabilityReads.get(activityRef);
  if (existing !== undefined) {
    return existing;
  }
  const pending = defaultSource.activityMode!(activityRef).catch((error) => {
    capabilityReads.delete(activityRef);
    throw error;
  });
  capabilityReads.set(activityRef, pending);
  return pending;
}

export function invalidateActivitySessionCardCapability(
  activityRef?: string,
): void {
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
  const [mode, setMode] = useState<SessionCaptureMode | null>(null);

  useEffect(() => {
    let cancelled = false;
    setMode(null);
    const read =
      source === defaultSource
        ? cachedCapability(activityRef)
        : (source.activityMode?.(activityRef) ??
          source
            .activityEnabled(activityRef)
            .then((enabled) => (enabled ? 'live' : 'disabled')));
    void read
      .then((value) => {
        if (!cancelled) {
          setMode(value as SessionCaptureMode);
        }
      })
      .catch(() => {
        if (!cancelled) {
          // Fail closed: an unread capability must never expose a runtime command.
          setMode('disabled');
        }
      });
    return () => {
      cancelled = true;
    };
  }, [activityRef, source]);

  if (mode !== 'live' && mode !== 'record_and_live') {
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
        allowLive={mode === 'live' || mode === 'record_and_live'}
      />
    </div>
  );
}

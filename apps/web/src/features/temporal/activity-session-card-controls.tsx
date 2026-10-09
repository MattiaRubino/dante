import { useEffect, useState } from 'react';

import './activity-session-card-controls.css';

import { ActivityPlannedSessionsCardDetail } from './activity-planned-sessions-card-detail';
import {
  type TemporalSessionCapabilityDataSource,
  type SessionCaptureMode,
} from './remote-session-capability-data-source';
import { SessionSubjectControls } from './session-subject-controls';
import { cachedActivitySessionCapability, defaultActivitySessionSource } from './activity-session-capability-cache';

export function ActivitySessionCardControls({
  activityRef,
  label,
  interactive = true,
  showPlanned = true,
  variant = 'card',
  source = defaultActivitySessionSource,
}: Readonly<{
  activityRef: string;
  label: string;
  interactive?: boolean;
  showPlanned?: boolean;
  variant?: 'card' | 'inspector';
  source?: TemporalSessionCapabilityDataSource;
}>) {
  const [mode, setMode] = useState<SessionCaptureMode | null>(null);

  useEffect(() => {
    let cancelled = false;
    setMode(null);
    const read =
      source === defaultActivitySessionSource
        ? cachedActivitySessionCapability(activityRef)
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

  const live = mode === 'live' || mode === 'record_and_live';

  if (variant === 'inspector' && !live) return null;

  return (
    <div
      className="timeline-activity-session-card-controls"
      data-timeline-activity-session-controls={activityRef}
    >
      {live ? (
        <>
        <SessionSubjectControls
          kind="activity"
          subjectRef={activityRef}
          label={label}
          variant={variant === 'card' ? 'card' : 'detail'}
          compactRuntime
          interactive={interactive}
          allowLive
        />
        </>
      ) : null}
      {showPlanned ? (
        <ActivityPlannedSessionsCardDetail
          activityRef={activityRef}
          visible
          variant="indicator"
        />
      ) : null}
    </div>
  );
}

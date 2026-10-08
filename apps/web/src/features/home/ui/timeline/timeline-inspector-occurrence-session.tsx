import { useEffect, useState } from 'react';

import { createRemoteTemporalSessionDataSource } from '../../../temporal/remote-session-data-source';
import { SessionSubjectControls } from '../../../temporal/session-subject-controls';

export function TimelineInspectorOccurrenceSession({ occurrenceRef, label }: Readonly<{
  occurrenceRef: string;
  label: string;
}>) {
  const [hasSessions, setHasSessions] = useState(false);
  useEffect(() => {
    let active = true;
    void createRemoteTemporalSessionDataSource().list('occurrence', occurrenceRef)
      .then((rows) => { if (active) setHasSessions(rows.length > 0); })
      .catch(() => undefined);
    return () => { active = false; };
  }, [occurrenceRef]);
  if (!hasSessions) return null;
  return <div className="timeline-event-modal__session">
    <strong>Sessione</strong>
    <SessionSubjectControls kind="occurrence" subjectRef={occurrenceRef}
      label={label} compactRuntime />
  </div>;
}

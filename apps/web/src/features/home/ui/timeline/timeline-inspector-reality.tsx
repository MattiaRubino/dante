import { useEffect, useState } from 'react';

import { ActualRealizationControls } from '../../../temporal/actual-realization-controls';
import { ObjectiveControls } from '../../../temporal/objective-controls';
import {
  createRemoteRealityObjectiveDataSource,
  type RealityMode,
  type RealitySubjectKind,
} from '../../../temporal/remote-reality-objective-data-source';

export function TimelineInspectorReality({ kind, subjectRef }: Readonly<{
  kind: RealitySubjectKind;
  subjectRef: string;
}>) {
  const [mode, setMode] = useState<RealityMode | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let active = true;
    setMode(null);
    setFailed(false);
    void createRemoteRealityObjectiveDataSource(globalThis.fetch)
      .getRealityMode(kind, subjectRef)
      .then((value) => { if (active) setMode(value); })
      .catch(() => { if (active) setFailed(true); });
    return () => { active = false; };
  }, [kind, subjectRef]);

  return <>
    {failed ? <p role="alert">Verifica svolgimento non disponibile.</p> : null}
    {mode === 'review_on_end' ? (
      <div className="timeline-event-modal__reality" data-timeline-runtime-reality>
        <ActualRealizationControls kind={kind} subjectRef={subjectRef}
          compactReview showObjectives={false} />
      </div>
    ) : null}
    <ObjectiveControls kind={kind} subjectRef={subjectRef} />
  </>;
}

import { useEffect, useState } from 'react';

import { ActualRealizationControls } from '../../../temporal/actual-realization-controls';
import { ObjectiveControls } from '../../../temporal/objective-controls';
import {
  createRemoteRealityObjectiveDataSource,
  type RealityMode,
  type RealitySubjectKind,
} from '../../../temporal/remote-reality-objective-data-source';

export function TimelineInspectorReality({
  kind,
  subjectRef,
}: Readonly<{
  kind: RealitySubjectKind;
  subjectRef: string;
}>) {
  const requestKey = `${kind}:${subjectRef}`;
  const [result, setResult] = useState<
    Readonly<{ key: string; mode: RealityMode | null; failed: boolean }> | null
  >(null);
  // A previous subject's result must never flash on a different Inspector.
  const current = result?.key === requestKey ? result : null;
  const mode = current?.mode ?? null;
  const failed = current?.failed ?? false;

  useEffect(() => {
    let active = true;
    void createRemoteRealityObjectiveDataSource(globalThis.fetch)
      .getRealityMode(kind, subjectRef)
      .then((value) => {
        if (active) {
          setResult({ key: requestKey, mode: value, failed: false });
        }
      })
      .catch(() => {
        if (active) {
          setResult({ key: requestKey, mode: null, failed: true });
        }
      });
    return () => {
      active = false;
    };
  }, [kind, subjectRef, requestKey]);

  return (
    <>
      {failed ? (
        <p role="alert">Verifica svolgimento non disponibile.</p>
      ) : null}
      {mode === 'review_on_end' ? (
        <div
          className="timeline-event-modal__reality"
          data-timeline-runtime-reality
        >
          <ActualRealizationControls
            kind={kind}
            subjectRef={subjectRef}
            compactReview
            showObjectives={false}
          />
        </div>
      ) : null}
      <ObjectiveControls kind={kind} subjectRef={subjectRef} />
    </>
  );
}

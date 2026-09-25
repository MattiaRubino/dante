import { useCallback, useEffect, useMemo, useState } from 'react';

import './responsibility-controls.css';

import {
  createRemoteTemporalResponsibilityDataSource,
  type ParticipationRequirement,
  type ResponsibilitySubjectKind,
  type TemporalExpectedParticipationView,
  type TemporalResponsibilityView,
} from './remote-responsibility-data-source';

function operationId(): string {
  return crypto.randomUUID();
}

function rejection(fallback: string, error: unknown): string {
  if (error instanceof Error && error.message.trim()) {
    return `${fallback} ${error.message}`;
  }
  return fallback;
}

/**
 * B09-B authoring. Expected Participation states an intention; it is never
 * attendance, an Actual or an Outcome, and Responsibility is not Participation.
 */
export function ResponsibilityControls({
  kind,
  subjectRef,
}: Readonly<{
  kind: ResponsibilitySubjectKind;
  subjectRef: string;
}>) {
  const source = useMemo(
    () => createRemoteTemporalResponsibilityDataSource(globalThis.fetch),
    [],
  );

  const [responsibility, setResponsibility] =
    useState<TemporalResponsibilityView | null>(null);
  const [participation, setParticipation] = useState<
    readonly TemporalExpectedParticipationView[]
  >([]);
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const reload = useCallback(async () => {
    const current = await source.getResponsibility(kind, subjectRef);
    setResponsibility(current);
    if (kind === 'event') {
      setParticipation(await source.listExpectedParticipation(subjectRef));
    }
  }, [kind, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const current = await source.getResponsibility(kind, subjectRef);
        if (cancelled) {
          return;
        }
        setResponsibility(current);
        if (kind === 'event') {
          const listed = await source.listExpectedParticipation(subjectRef);
          if (!cancelled) {
            setParticipation(listed);
          }
        }
      } catch (error) {
        if (!cancelled) {
          setMessage(rejection('Responsabilità non disponibile.', error));
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [kind, subjectRef]);

  const run = (action: () => Promise<unknown>, failure: string) => {
    setPending(true);
    setMessage(null);
    void action()
      .then(() => reload())
      .catch((error: unknown) => setMessage(rejection(failure, error)))
      .finally(() => setPending(false));
  };

  const holderIsSelf = responsibility?.responsibleIsSelf === true;
  const selfParticipation =
    participation.find((item) => item.participantIsSelf) ?? null;

  return (
    <div
      className="timeline-responsibility-controls"
      data-timeline-responsibility-subject={subjectRef}
    >
      <p data-timeline-responsibility-state>
        {holderIsSelf ? 'Responsabile: tu' : 'Nessun responsabile'}
      </p>
      <button
        type="button"
        disabled={pending}
        data-timeline-responsibility-toggle
        onClick={() =>
          run(
            () =>
              source.setResponsibility(kind, subjectRef, {
                operationId: operationId(),
                holder: holderIsSelf ? null : 'self',
                expectedHolder: holderIsSelf ? 'self' : null,
              }),
            holderIsSelf
              ? 'Rimozione responsabilità rifiutata.'
              : 'Assegnazione responsabilità rifiutata.',
          )
        }
      >
        {holderIsSelf ? 'Rimuovi responsabilità' : 'Assegna a me'}
      </button>

      {kind === 'event' ? (
        <div className="timeline-responsibility-controls__participation">
          <p data-timeline-participation-state>
            {selfParticipation === null
              ? 'Partecipazione attesa: non indicata'
              : `Partecipazione attesa: ${
                  selfParticipation.requirementCode === 'required'
                    ? 'obbligatoria'
                    : 'facoltativa'
                }`}
          </p>
          {(['required', 'optional'] as const).map(
            (requirement: ParticipationRequirement) => (
              <button
                key={requirement}
                type="button"
                disabled={
                  pending || selfParticipation?.requirementCode === requirement
                }
                data-timeline-participation-set={requirement}
                onClick={() =>
                  run(
                    () =>
                      source.setExpectedParticipation(subjectRef, {
                        operationId: operationId(),
                        requirementCode: requirement,
                        expectedRequirementCode:
                          selfParticipation?.requirementCode ?? null,
                      }),
                    'Aggiornamento partecipazione rifiutato.',
                  )
                }
              >
                {requirement === 'required' ? 'Obbligatoria' : 'Facoltativa'}
              </button>
            ),
          )}
          {selfParticipation === null ? null : (
            <button
              type="button"
              disabled={pending}
              data-timeline-participation-remove
              onClick={() =>
                run(
                  () =>
                    source.setExpectedParticipation(subjectRef, {
                      operationId: operationId(),
                      requirementCode: null,
                      expectedRequirementCode:
                        selfParticipation.requirementCode,
                    }),
                  'Rimozione partecipazione rifiutata.',
                )
              }
            >
              Rimuovi partecipazione
            </button>
          )}
        </div>
      ) : null}

      {message === null ? null : <span role="status">{message}</span>}
    </div>
  );
}

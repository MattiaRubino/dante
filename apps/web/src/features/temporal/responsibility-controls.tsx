import { useCallback, useEffect, useMemo, useState } from 'react';

import './responsibility-controls.css';

import {
  createRemoteTemporalResponsibilityDataSource,
  type ParticipationRequirement,
  type ResponsibilitySubjectKind,
  type TemporalExpectedParticipationView,
  type TemporalPersonReferent,
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

/** Local labels present native Persons; expected involvement is never attendance. */
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
  const [people, setPeople] = useState<readonly TemporalPersonReferent[]>([]);
  const [selectedPerson, setSelectedPerson] = useState('self');
  const [personLabel, setPersonLabel] = useState('');
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [personCreated, setPersonCreated] = useState(false);

  const reload = useCallback(async () => {
    const [current, referents] = await Promise.all([
      source.getResponsibility(kind, subjectRef),
      source.listPersonReferents(),
    ]);
    setResponsibility(current);
    setPeople(referents);
    if (kind === 'event') {
      setParticipation(await source.listExpectedParticipation(subjectRef));
    }
  }, [kind, source, subjectRef]);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const [current, referents] = await Promise.all([
          source.getResponsibility(kind, subjectRef),
          source.listPersonReferents(),
        ]);
        if (cancelled) return;
        setResponsibility(current);
        setPeople(referents);
        if (kind === 'event') {
          const listed = await source.listExpectedParticipation(subjectRef);
          if (!cancelled) setParticipation(listed);
        }
      } catch (error) {
        if (!cancelled) {
          setMessage(rejection('Responsabilità non disponibile.', error));
        }
      }
    })();
    return () => { cancelled = true; };
  }, [kind, source, subjectRef]);

  const run = (action: () => Promise<unknown>, failure: string) => {
    setPending(true);
    setMessage(null);
    setPersonCreated(false);
    void action()
      .then(() => reload())
      .catch((error: unknown) => setMessage(rejection(failure, error)))
      .finally(() => setPending(false));
  };

  const labelFor = (ref: string | null, isSelf = false) =>
    isSelf ? 'tu' :
    people.find((person) => person.personRef === ref)?.displayLabel ??
    'referente non disponibile';

  const holder = responsibility?.responsiblePersonRef === null ||
    responsibility === null ? null :
    responsibility.responsibleIsSelf ? 'self' :
    responsibility.responsiblePersonRef;
  const selectedParticipation = participation.find((item) =>
    selectedPerson === 'self' ? item.participantIsSelf :
    item.participantPersonRef === selectedPerson,
  ) ?? null;
  const selectedLabel = selectedPerson === 'self' ? 'me' :
    labelFor(selectedPerson);
  const selectedIsHolder = holder !== null && holder === selectedPerson;

  return (
    <div
      className="timeline-responsibility-controls"
      data-timeline-responsibility-subject={subjectRef}
    >
      <strong>Responsabilità</strong>
      <p data-timeline-responsibility-state>
        {holder === null ? 'Nessun responsabile' :
          `Responsabile: ${labelFor(
            responsibility?.responsiblePersonRef ?? null,
            responsibility?.responsibleIsSelf,
          )}`}
      </p>
      <label className="timeline-responsibility-controls__person">
        Persona
        <select
          aria-label="Persona per responsabilità o partecipazione"
          value={selectedPerson}
          disabled={pending}
          onChange={(event) => setSelectedPerson(event.currentTarget.value)}
        >
          <option value="self">Io</option>
          {people.map((person) => (
            <option key={person.personRef} value={person.personRef}>
              {person.displayLabel}
            </option>
          ))}
        </select>
      </label>
      <button
        type="button"
        disabled={pending || responsibility === null}
        data-timeline-responsibility-toggle
        onClick={() => run(
          () => source.setResponsibility(kind, subjectRef, {
            operationId: operationId(),
            holder: selectedIsHolder ? null : selectedPerson,
            expectedHolder: holder,
          }),
          selectedIsHolder
            ? 'Rimozione responsabilità rifiutata.'
            : 'Assegnazione responsabilità rifiutata.',
        )}
      >
        {selectedIsHolder ? 'Rimuovi responsabilità' :
          selectedPerson === 'self' ? 'Assegna a me' :
          `Assegna a ${selectedLabel}`}
      </button>

      <div className="timeline-responsibility-controls__catalog">
        <label>
          Nome locale della persona
          <input
            aria-label="Nome locale della persona"
            maxLength={100}
            value={personLabel}
            disabled={pending}
            onChange={(event) => setPersonLabel(event.currentTarget.value)}
            placeholder="Es. Anna"
          />
        </label>
        <button
          type="button"
          disabled={pending || !personLabel.trim()}
          onClick={() => run(async () => {
            const created = await source.createPersonReferent(
              operationId(), personLabel,
            );
            setSelectedPerson(created.personRef);
            setPersonLabel('');
            setPersonCreated(true);
          }, 'Creazione persona rifiutata.')}
        >
          Aggiungi persona
        </button>
        {selectedPerson === 'self' ? null : (
          <button
            type="button"
            disabled={pending || !personLabel.trim()}
            onClick={() => run(async () => {
              const selected = people.find((person) =>
                person.personRef === selectedPerson);
              if (selected === undefined) return;
              await source.renamePersonReferent(
                selected.personRef, operationId(), selected.revision, personLabel,
              );
              setPersonLabel('');
            }, 'Modifica nome rifiutata.')}
          >
            Correggi nome
          </button>
        )}
      </div>
      {personCreated ? (
        <p role="status">Persona aggiunta. Per assegnarle la responsabilità, premi “Assegna a {selectedLabel}”.</p>
      ) : null}

      {kind === 'event' ? (
        <div className="timeline-responsibility-controls__participation">
          <strong>Partecipazione attesa all’Event</strong>
          <p data-timeline-participation-state>
            {selectedParticipation === null
              ? 'Partecipazione attesa: non indicata'
              : `Partecipazione attesa: ${
                  selectedParticipation.requirementCode === 'required'
                    ? 'obbligatoria' : 'facoltativa'
                }`}
          </p>
          {participation.length > 0 ? (
            <ul aria-label="Persone con partecipazione attesa">
              {participation.map((item) => (
                <li key={item.participantPersonRef}>
                  {labelFor(item.participantPersonRef, item.participantIsSelf)}:
                  {' '}{item.requirementCode === 'required' ?
                    'obbligatoria' : 'facoltativa'}
                </li>
              ))}
            </ul>
          ) : null}
          {(['required', 'optional'] as const).map(
            (requirement: ParticipationRequirement) => (
              <button
                key={requirement}
                type="button"
                disabled={pending ||
                  selectedParticipation?.requirementCode === requirement}
                data-timeline-participation-set={requirement}
                onClick={() => run(
                  () => source.setExpectedParticipation(subjectRef, {
                    operationId: operationId(),
                    participant: selectedPerson,
                    requirementCode: requirement,
                    expectedRequirementCode:
                      selectedParticipation?.requirementCode ?? null,
                  }),
                  'Aggiornamento partecipazione rifiutato.',
                )}
              >
                {requirement === 'required' ? 'Obbligatoria' : 'Facoltativa'}
              </button>
            ),
          )}
          {selectedParticipation === null ? null : (
            <button
              type="button"
              disabled={pending}
              data-timeline-participation-remove
              onClick={() => run(
                () => source.setExpectedParticipation(subjectRef, {
                  operationId: operationId(),
                  participant: selectedPerson,
                  requirementCode: null,
                  expectedRequirementCode:
                    selectedParticipation.requirementCode,
                }),
                'Rimozione partecipazione rifiutata.',
              )}
            >
              Rimuovi partecipazione
            </button>
          )}
        </div>
      ) : null}
      {message === null ? null : <span role="alert">{message}</span>}
    </div>
  );
}

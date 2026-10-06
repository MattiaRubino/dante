import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  createRemoteTemporalResponsibilityDataSource,
  type ParticipationRequirement,
  type TemporalPersonReferent,
} from '../../temporal/remote-responsibility-data-source';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-event-participants.css';

function operationId(): string {
  return crypto.randomUUID();
}

export function TemporalCreateEventParticipants() {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const source = useMemo(
    () => createRemoteTemporalResponsibilityDataSource(globalThis.fetch),
    [],
  );
  const [people, setPeople] = useState<readonly TemporalPersonReferent[]>([]);
  const [selectedPerson, setSelectedPerson] = useState('self');
  const [requirement, setRequirement] =
    useState<ParticipationRequirement>('required');
  const [newPersonLabel, setNewPersonLabel] = useState('');
  const [pending, setPending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    void source
      .listPersonReferents()
      .then((items) => {
        if (!cancelled) setPeople(items);
      })
      .catch(() => {
        if (!cancelled) {
          setMessage(
            italian
              ? 'Persone non disponibili in questo momento.'
              : 'People are unavailable right now.',
          );
        }
      });
    return () => {
      cancelled = true;
    };
  }, [italian, source]);

  const participantLabel = (personRef: string) =>
    personRef === 'self'
      ? italian
        ? 'Io'
        : 'Me'
      : (people.find((person) => person.personRef === personRef)?.displayLabel ??
        draft.eventParticipants.find((item) => item.personRef === personRef)
          ?.displayLabel ??
        (italian ? 'Persona' : 'Person'));

  const publish = (
    eventParticipants: typeof draft.eventParticipants,
  ) => patch({ eventParticipants: Object.freeze([...eventParticipants]) });

  const addSelected = () => {
    if (draft.eventParticipants.some((item) => item.personRef === selectedPerson)) {
      return;
    }
    publish([
      ...draft.eventParticipants,
      Object.freeze({
        personRef: selectedPerson,
        displayLabel: participantLabel(selectedPerson),
        requirementCode: requirement,
      }),
    ]);
  };

  const updateRequirement = (
    personRef: string,
    requirementCode: ParticipationRequirement,
  ) => {
    publish(
      draft.eventParticipants.map((item) =>
        item.personRef === personRef
          ? Object.freeze({ ...item, requirementCode })
          : item,
      ),
    );
  };

  const remove = (personRef: string) => {
    publish(
      draft.eventParticipants.filter((item) => item.personRef !== personRef),
    );
  };

  const createPerson = () => {
    const label = newPersonLabel.trim();
    if (!label || pending) return;
    setPending(true);
    setMessage(null);
    void source
      .createPersonReferent(operationId(), label)
      .then((created) => {
        setPeople((current) => Object.freeze([...current, created]));
        setSelectedPerson(created.personRef);
        setNewPersonLabel('');
        if (
          !draft.eventParticipants.some(
            (item) => item.personRef === created.personRef,
          )
        ) {
          publish([
            ...draft.eventParticipants,
            Object.freeze({
              personRef: created.personRef,
              displayLabel: created.displayLabel,
              requirementCode: requirement,
            }),
          ]);
        }
      })
      .catch(() =>
        setMessage(
          italian
            ? 'Non è stato possibile aggiungere la persona.'
            : 'The person could not be added.',
        ),
      )
      .finally(() => setPending(false));
  };

  return (
    <section
      className="temporal-create-event-participants"
      data-create-event-participants
      aria-label={italian ? 'Partecipanti evento' : 'Event participants'}
    >
      <div className="temporal-create-event-participants__heading">
        <strong>{italian ? 'Partecipanti' : 'Participants'}</strong>
        <span>
          {italian
            ? 'Attesi per questo evento; non concede accesso alla tua Timeline.'
            : 'Expected for this event; this does not grant access to your Timeline.'}
        </span>
      </div>

      {draft.eventParticipants.length > 0 ? (
        <div className="temporal-create-event-participants__list">
          {draft.eventParticipants.map((item) => (
            <div
              className="temporal-create-event-participants__row"
              key={item.personRef}
            >
              <span>{item.displayLabel}</span>
              <select
                aria-label={
                  italian
                    ? `Partecipazione di ${item.displayLabel}`
                    : `Participation for ${item.displayLabel}`
                }
                value={item.requirementCode}
                onChange={(event) =>
                  updateRequirement(
                    item.personRef,
                    event.currentTarget.value as ParticipationRequirement,
                  )
                }
              >
                <option value="required">
                  {italian ? 'Richiesto' : 'Required'}
                </option>
                <option value="optional">
                  {italian ? 'Opzionale' : 'Optional'}
                </option>
              </select>
              <button
                type="button"
                onClick={() => remove(item.personRef)}
                aria-label={
                  italian
                    ? `Rimuovi ${item.displayLabel}`
                    : `Remove ${item.displayLabel}`
                }
              >
                ×
              </button>
            </div>
          ))}
        </div>
      ) : null}

      <div className="temporal-create-event-participants__add">
        <select
          aria-label={italian ? 'Persona' : 'Person'}
          value={selectedPerson}
          disabled={pending}
          onChange={(event) => setSelectedPerson(event.currentTarget.value)}
        >
          <option value="self">{italian ? 'Io' : 'Me'}</option>
          {people.map((person) => (
            <option key={person.personRef} value={person.personRef}>
              {person.displayLabel}
            </option>
          ))}
        </select>
        <select
          aria-label={italian ? 'Tipo partecipazione' : 'Participation type'}
          value={requirement}
          disabled={pending}
          onChange={(event) =>
            setRequirement(event.currentTarget.value as ParticipationRequirement)
          }
        >
          <option value="required">{italian ? 'Richiesto' : 'Required'}</option>
          <option value="optional">{italian ? 'Opzionale' : 'Optional'}</option>
        </select>
        <button
          type="button"
          disabled={
            pending ||
            draft.eventParticipants.some(
              (item) => item.personRef === selectedPerson,
            )
          }
          onClick={addSelected}
        >
          ＋ {italian ? 'Aggiungi' : 'Add'}
        </button>
      </div>

      <div className="temporal-create-event-participants__new-person">
        <input
          type="text"
          maxLength={100}
          value={newPersonLabel}
          disabled={pending}
          aria-label={italian ? 'Nuova persona locale' : 'New local person'}
          placeholder={italian ? 'Nuova persona' : 'New person'}
          onChange={(event) => setNewPersonLabel(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              event.preventDefault();
              createPerson();
            }
          }}
        />
        <button
          type="button"
          disabled={pending || !newPersonLabel.trim()}
          onClick={createPerson}
        >
          ＋ {italian ? 'Persona' : 'Person'}
        </button>
      </div>

      {message ? <span role="alert">{message}</span> : null}
    </section>
  );
}

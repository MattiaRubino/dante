// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type {
  TemporalAuthorActivityRequest,
  TemporalAuthorEventRequest,
  TemporalAuthoringDataSource,
  TemporalAuthoredActivityResult,
  TemporalAuthoredEventResult,
} from '../../temporal';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function activityResult(title: string): TemporalAuthoredActivityResult {
  return Object.freeze({
    item: Object.freeze({
      subjectRef: '0199a111-1111-7111-8111-111111111111',
      title,
      createdAt: Temporal.Instant.from('2026-09-30T19:00:00Z'),
      description: null,
      location: null,
      colorCode: null,
      lifeAreaRef: null,
      lifeAreaAssignmentRevision: null,
      lifeAreaColorCode: null,
      lifeAreaRevision: null,
    }),
    schedule: null,
    replayed: false,
  });
}

function eventResult(title: string): TemporalAuthoredEventResult {
  return Object.freeze({
    ...activityResult(title),
    agendaRevision: 0,
    agendaParts: Object.freeze([]),
  });
}

function renderEntry(contexts: readonly {
  id: string;
  label: string;
  tone: 'personal';
  revision?: number;
  colorCode?: string | null;
}[] = []) {
  const activityRequests: TemporalAuthorActivityRequest[] = [];
  const eventRequests: TemporalAuthorEventRequest[] = [];
  const source: TemporalAuthoringDataSource = {
    authorActivity: vi.fn(async (request) => {
      activityRequests.push(request);
      return activityResult(request.title);
    }),
    authorEvent: vi.fn(async (request) => {
      eventRequests.push(request);
      return eventResult(request.title);
    }),
  };
  const rendered = render(
    <>
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from('2026-09-30')}
        contexts={contexts}
        authoringDataSource={source}
        onPreview={() => undefined}
        onApplied={() => false}
        creationEnabled={false}
      />
    </>,
  );
  const quickAdd = rendered.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!quickAdd) throw new Error('Expected Create trigger.');
  fireEvent.click(quickAdd);
  return { ...rendered, activityRequests, eventRequests };
}

describe('Temporal Create U2 entry', () => {
  it('creates an Activity without requiring any Life Area', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Passeggiata' },
    });
    fireEvent.change(screen.getByLabelText('Località'), {
      target: { value: 'Lungofiume' },
    });
    fireEvent.change(screen.getByLabelText('Descrizione'), {
      target: { value: 'Lungo il fiume' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.lifeArea).toBeUndefined();
    expect(activityRequests[0]?.location).toBe('Lungofiume');
    expect(activityRequests[0]?.description).toBe('Lungo il fiume');
  });

  it('stages a new Life Area locally and sends it only with the accepted Add', async () => {
    const { activityRequests } = renderEntry();

    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Studio' },
    });
    fireEvent.change(screen.getByLabelText('Life Area (opzionale)'), {
      target: { value: 'Formazione' },
    });

    expect(activityRequests).toHaveLength(0);
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(activityRequests).toHaveLength(1));
    expect(activityRequests[0]?.lifeArea).toEqual({ newName: 'Formazione' });
  });

  it('routes Event through the U2 Event endpoint', async () => {
    const { eventRequests } = renderEntry();

    fireEvent.click(screen.getByRole('radio', { name: 'Evento' }));
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Workshop' },
    });
    fireEvent.change(screen.getByLabelText('Località'), {
      target: { value: 'Sala A' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi' }));

    await waitFor(() => expect(eventRequests).toHaveLength(1));
    expect(eventRequests[0]?.title).toBe('Workshop');
    expect(eventRequests[0]?.location).toBe('Sala A');
  });
});

import { domElement } from '../../../test-support/dom-element';
// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomeCreateInteractionBridge } from '../../home/ui/home-create-interaction-bridge';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { TemporalCreateEntry } from './temporal-create-entry';

const mocks = vi.hoisted(() => ({
  save: vi.fn(),
  remove: vi.fn(),
  list: vi.fn(),
}));
vi.mock('../application/remote-draft-vault', () => ({
  createRemoteDraftVault: () => mocks,
  DRAFT_VAULT_UPDATED: 'dante:draft-vault-updated',
  notifyDraftVaultUpdated: () => undefined,
}));

beforeAll(async () => {
  await i18n.changeLanguage('it');
});
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

function entry(draftRequest?: {
  id: number;
  item: {
    draftRef: string;
    subjectKind: 'activity' | 'event';
    title: string;
    payload: {
      version: 1;
      fields: ReturnType<typeof createTemporalCreateFields>;
      advanced: ReturnType<typeof createTemporalCreateU2AuthoringDraft>;
      surface: 'quick' | 'expanded' | 'full';
    };
    revision: number;
    createdAt: string;
    updatedAt: string;
  };
  duplicate: boolean;
}) {
  return render(
    <>
      <HomeCreateInteractionBridge />
      <div data-home-context-create-host />
      <TemporalCreateEntry
        defaultDate={Temporal.PlainDate.from('2026-10-09')}
        contexts={[]}
        draftRequest={draftRequest ?? null}
        authoringDataSource={{
          authorActivity: vi.fn(),
          authorEvent: vi.fn(),
        }}
        onPreview={() => undefined}
        onApplied={() => false}
      />
    </>,
  );
}

describe('Create + Draft Vault', () => {
  it('saves the quick editor as a snapshot without creating an Activity', async () => {
    const saved = {
      draftRef: 'vault-1',
      subjectKind: 'activity',
      title: 'Allenamento',
      payload: null,
      revision: 1,
      createdAt: '',
      updatedAt: '',
    };
    mocks.save.mockResolvedValueOnce(saved);
    const view = entry();
    const trigger = view.container.querySelector<HTMLButtonElement>(
      '.dante-timeline-quick-add',
    );
    if (!trigger) throw new Error('No create trigger');
    fireEvent.click(trigger);
    fireEvent.change(screen.getByPlaceholderText('Titolo'), {
      target: { value: 'Allenamento' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Salva bozza' }));
    await waitFor(() => expect(mocks.save).toHaveBeenCalledOnce());
    expect(mocks.save.mock.calls[0]?.[0]).toMatchObject({
      version: 1,
      fields: { kind: 'activity', title: 'Allenamento' },
      advanced: { activityStructure: { plannedSlices: [] } },
    });
    await waitFor(() =>
      expect(screen.queryByPlaceholderText('Titolo')).toBeNull(),
    );
  });

  it.each([
    { kind: 'activity' as const, duplicate: false },
    { kind: 'activity' as const, duplicate: true },
    { kind: 'event' as const, duplicate: false },
    { kind: 'event' as const, duplicate: true },
  ])(
    'opens the real Advanced Create for a quick-saved $kind draft (duplicate=$duplicate)',
    async ({ kind, duplicate }) => {
      const fields = createTemporalCreateFields({
        kind,
        title: kind === 'activity' ? 'Preparazione' : 'Riunione',
      });
      const advanced = createTemporalCreateU2AuthoringDraft(fields);
      entry({
        id: 21,
        item: {
          draftRef: 'vault-quick',
          subjectKind: kind,
          title: fields.title,
          revision: 2,
          createdAt: '',
          updatedAt: '',
          payload: { version: 1, fields, advanced, surface: 'quick' },
        },
        duplicate,
      });
      const title = domElement(
        await screen.findByPlaceholderText('Titolo'),
        HTMLInputElement,
      );
      expect(title.value).toBe(fields.title);
      const advancedToggle = document.querySelector<HTMLButtonElement>(
        '.temporal-create-advanced-toggle',
      );
      expect(advancedToggle?.getAttribute('aria-expanded')).toBe('true');
      expect(screen.getByRole('button', { name: 'Salva bozza' })).toBeTruthy();
      expect(screen.getByRole('button', { name: 'Aggiungi' })).toBeTruthy();
      expect(mocks.save).not.toHaveBeenCalled();
    },
  );

  it('reopens a saved advanced draft without creating an operational subject', async () => {
    const fields = { ...createTemporalCreateFields(), title: 'Preparazione' };
    const base = createTemporalCreateU2AuthoringDraft(fields);
    const advanced = {
      ...base,
      activityStructure: {
        ...base.activityStructure,
        plannedSlices: [
          {
            id: 'planned-1',
            title: 'Ricerca fonti',
            timeEnabled: false,
            date: fields.date,
            startTime: fields.startTime,
            endTime: fields.startTime,
          },
        ],
      },
      objectives: [
        {
          id: 'goal-1',
          label: 'Lavoro completato',
          resultKind: 'boolean' as const,
          comparatorCode: null,
          targetValue: '',
          targetMin: '',
          targetMax: '',
          unitCode: '',
          verificationMode: 'none' as const,
        },
      ],
    };
    entry({
      id: 1,
      item: {
        draftRef: 'vault-2',
        subjectKind: 'activity',
        title: fields.title,
        revision: 3,
        createdAt: '',
        updatedAt: '',
        payload: { version: 1, fields, advanced, surface: 'full' },
      },
      duplicate: false,
    });
    expect(
      domElement(await screen.findByPlaceholderText('Titolo'), HTMLInputElement)
        .value,
    ).toBe('Preparazione');
    expect(screen.getByRole('button', { name: 'Salva bozza' })).toBeTruthy();
    // Resume is the full advanced Create editor, not a read-only mockup.
    expect(screen.getByDisplayValue('Ricerca fonti')).toBeTruthy();
    expect(screen.getByDisplayValue('Lavoro completato')).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Aggiungi' })).toBeTruthy();
    expect(mocks.save).not.toHaveBeenCalled();
  });
});

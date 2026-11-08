import { domElement } from '../../../test-support/dom-element';
// @vitest-environment jsdom

import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { temporalValidationIssue } from '../../temporal/model';
import {
  createTemporalCreateFields,
  createTemporalCreateSession,
  requestTemporalCreateClose,
  setTemporalCreateSurface,
  updateTemporalCreateFields,
} from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { TemporalCreateComposer } from './temporal-create-composer';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  vi.unstubAllGlobals();
  cleanup();
});

const context = Object.freeze([
  { id: 'personale', label: 'Personale', tone: 'personal' as const },
]);

function renderComposer(options?: { dirty?: boolean }) {
  const base = createTemporalCreateSession(
    createTemporalCreateFields({
      date: '2026-09-30',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    }),
  );
  const session = options?.dirty
    ? requestTemporalCreateClose(
        updateTemporalCreateFields(base, { title: 'Preparare il piano' }),
      ).session
    : base;
  const onRequestClose = vi.fn();
  const onContinueEditing = vi.fn();
  const onDiscard = vi.fn();
  const onMoveToUnplaced = vi.fn();

  const view = render(
    <TemporalCreateComposer
      session={session}
      contexts={context}
      issues={[]}
      lifecycle="idle"
      failureMessage=""
      postCreateRetry={false}
      u2Draft={createTemporalCreateU2AuthoringDraft(session.draft.current)}
      onPatch={vi.fn()}
      onSurfaceChange={vi.fn()}
      onRequestClose={onRequestClose}
      onContinueEditing={onContinueEditing}
      onDiscard={onDiscard}
      onMoveToUnplaced={onMoveToUnplaced}
      onSubmit={vi.fn()}
    />,
  );

  return {
    ...view,
    onRequestClose,
    onContinueEditing,
    onDiscard,
    onMoveToUnplaced,
  };
}

describe('TemporalCreateComposer', () => {
  it('marks the visible date and recurrence controls at the failing field', () => {
    const fields = createTemporalCreateFields({
      date: '2026-10-06',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const session = setTemporalCreateSurface(
      createTemporalCreateSession(fields),
      'full',
    );
    render(
      <TemporalCreateComposer
        session={session}
        contexts={context}
        issues={[
          temporalValidationIssue('temporal.create.date.invalid', ['date']),
        ]}
        lifecycle="failed"
        failureTarget="eventRecurrence"
        failureMessage="Controlla la ripetizione."
        postCreateRetry={false}
        u2Draft={createTemporalCreateU2AuthoringDraft(fields)}
        onPatch={vi.fn()}
        onSurfaceChange={vi.fn()}
        onRequestClose={vi.fn()}
        onContinueEditing={vi.fn()}
        onDiscard={vi.fn()}
        onMoveToUnplaced={vi.fn()}
        onSubmit={vi.fn()}
      />,
    );
    const titleRow = document.querySelector(
      '.temporal-authoring-title-row--activity',
    );
    expect(titleRow?.getAttribute('data-authoring-title-kind')).toBe('activity');
    expect(titleRow?.firstElementChild?.textContent).toBe('◇');
    expect(titleRow?.children).toHaveLength(3);
    expect(titleRow?.children[1]?.classList.contains('temporal-create-title-row__name')).toBe(
      true,
    );
    expect(
      titleRow?.children[2]?.classList.contains('temporal-create-title-row__tools'),
    ).toBe(true);
    const activityActions = titleRow?.children[2];
    expect(activityActions?.children).toHaveLength(2);
    expect(activityActions?.children[0]?.getAttribute('data-placement-protection')).toBe(
      'activity',
    );
    expect(
      activityActions?.children[1]?.getAttribute('data-session-capability'),
    ).toBe('activity');
    const date = document.querySelector('[data-create-path="date"]');
    expect(date?.classList.contains('temporal-create-u2-date-field')).toBe(
      true,
    );
    expect(date?.getAttribute('aria-invalid')).toBe('true');
    expect(
      date?.querySelector('.temporal-create-date-picker__trigger'),
    ).toBeTruthy();
    expect(
      document
        .querySelector('[data-create-path="eventRecurrence"]')
        ?.getAttribute('aria-invalid'),
    ).toBe('true');
  });

  it.each(['activity', 'event'] as const)(
    'keeps the %s recurrence selector inside one expandable panel',
    (kind) => {
      const baseFields = createTemporalCreateFields({
        kind,
        date: '2026-11-08',
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      });
      const repeatFields = {
        ...baseFields,
        eventRecurrence: {
          ...baseFields.eventRecurrence,
          owner: kind === 'event' ? ('event' as const) : ('routine' as const),
          patternKind: 'calendar-wall-clock' as const,
          calendarFrequency: 'daily' as const,
        },
      };
      const renderWith = (fields: typeof baseFields) =>
        render(
          <TemporalCreateComposer
            session={setTemporalCreateSurface(
              createTemporalCreateSession(fields),
              'full',
            )}
            contexts={context}
            issues={[]}
            lifecycle="idle"
            failureMessage=""
            postCreateRetry={false}
            u2Draft={createTemporalCreateU2AuthoringDraft(fields)}
            onPatch={vi.fn()}
            onSurfaceChange={vi.fn()}
            onRequestClose={vi.fn()}
            onContinueEditing={vi.fn()}
            onDiscard={vi.fn()}
            onMoveToUnplaced={vi.fn()}
            onSubmit={vi.fn()}
          />,
        );
      const view = renderWith(baseFields);
      let panel = screen.getByRole('region', { name: 'Ripetizione' });
      expect(panel.getAttribute('data-recurrence-owner')).toBe(kind);
      expect(panel.getAttribute('data-recurrence-expanded')).toBe('false');
      expect(within(panel).getAllByRole('heading', { name: 'Ripetizione' }))
        .toHaveLength(1);
      expect(
        panel.querySelector('.temporal-recurrence-panel__choice')
          ?.contains(within(panel).getByRole('combobox', { name: 'Ripeti' })),
      ).toBe(true);
      expect(panel.querySelector('.temporal-recurrence-panel__details')).toBeNull();

      view.unmount();
      renderWith(repeatFields);
      panel = screen.getByRole('region', { name: 'Ripetizione' });
      expect(panel.getAttribute('data-recurrence-expanded')).toBe('true');
      expect(within(panel).getAllByRole('heading', { name: 'Ripetizione' }))
        .toHaveLength(1);
      expect(panel.querySelector('.temporal-recurrence-panel__details')).not.toBeNull();
      expect(
        within(panel).getByRole('combobox', { name: 'Ripeti' }),
      ).toHaveProperty('value', 'daily');
      const details = panel.querySelector(
        '.temporal-recurrence-panel__details',
      ) as HTMLElement;
      expect(
        details.querySelectorAll('.temporal-create-repeat'),
      ).toHaveLength(1);
      expect(
        details.querySelector('.temporal-create-repeat__end-choices'),
      ).not.toBeNull();
    },
  );

  it('marks the affected planned Session and renders only one advanced description', () => {
    const fields = createTemporalCreateFields({
      date: '2026-10-06',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const session = setTemporalCreateSurface(
      createTemporalCreateSession(fields),
      'full',
    );
    const draft = createTemporalCreateU2AuthoringDraft(fields);
    render(
      <TemporalCreateComposer
        session={session}
        contexts={context}
        issues={[]}
        lifecycle="failed"
        failureTarget="plannedSession:affected"
        failureMessage="Controlla questa Sessione."
        postCreateRetry={false}
        u2Draft={{
          ...draft,
          activityStructure: {
            ...draft.activityStructure,
            plannedSlices: [
              {
                id: 'affected',
                title: 'Prima',
                date: fields.date,
                startTime: '09:00',
                endTime: '09:30',
              },
              {
                id: 'other',
                title: 'Seconda',
                date: fields.date,
                startTime: '09:30',
                endTime: '10:00',
              },
            ],
          },
        }}
        onPatch={vi.fn()}
        onSurfaceChange={vi.fn()}
        onRequestClose={vi.fn()}
        onContinueEditing={vi.fn()}
        onDiscard={vi.fn()}
        onMoveToUnplaced={vi.fn()}
        onSubmit={vi.fn()}
      />,
    );

    const affected = document.querySelector(
      '[data-create-path="plannedSession:affected"]',
    );
    const other = document.querySelector(
      '[data-create-path="plannedSession:other"]',
    );
    expect(
      affected?.querySelector('[data-create-invalid="true"]'),
    ).toBeTruthy();
    expect(other?.querySelector('[data-create-invalid="true"]')).toBeNull();
    expect(within(affected as HTMLElement).getByRole('alert').textContent).toBe(
      'Controlla questa Sessione.',
    );
    expect(
      screen.getAllByRole('textbox', { name: /Descrizione/ }),
    ).toHaveLength(1);
  });

  it('uses the shared rounded footer action for Aggiungi', () => {
    renderComposer();
    const add = screen.getByRole('button', { name: 'Aggiungi' });
    expect(
      add.parentElement?.classList.contains('dante-temporal-panel-actions'),
    ).toBe(true);
    expect(add.classList.contains('is-primary')).toBe(true);
  });
  it('presents Event Scaletta and B09 participant staging while hiding prototype-only fields', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve(
          new Response(JSON.stringify([]), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          }),
        ),
      ),
    );

    const fields = createTemporalCreateFields({
      kind: 'event',
      date: '2026-10-06',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const session = setTemporalCreateSurface(
      createTemporalCreateSession(fields),
      'full',
    );
    const onPatch = vi.fn();
    const onU2DraftChange = vi.fn();

    render(
      <TemporalCreateComposer
        session={session}
        contexts={context}
        issues={[]}
        lifecycle="idle"
        failureMessage=""
        postCreateRetry={false}
        u2Draft={createTemporalCreateU2AuthoringDraft(session.draft.current)}
        onPatch={onPatch}
        onU2DraftChange={onU2DraftChange}
        onSurfaceChange={vi.fn()}
        onRequestClose={vi.fn()}
        onContinueEditing={vi.fn()}
        onDiscard={vi.fn()}
        onMoveToUnplaced={vi.fn()}
        onSubmit={vi.fn()}
      />,
    );

    const lifeArea = screen.getByRole('textbox', {
      name: 'Life Area (opzionale)',
    });
    expect(lifeArea.getAttribute('title')).toBeNull();
    expect(lifeArea.getAttribute('maxlength')).toBe('100');
    const eventTitleRow = document.querySelector('.temporal-event-title-row');
    expect(eventTitleRow).not.toBeNull();
    expect(eventTitleRow?.querySelector('[data-create-path="title"]')).toBeTruthy();
    expect(eventTitleRow?.getAttribute('data-authoring-title-kind')).toBe('event');
    expect(
      [...(eventTitleRow?.children ?? [])].map((child) =>
        child.classList.contains('temporal-authoring-title-row__marker')
          ? 'marker'
          : child.classList.contains('temporal-create-title-row__name')
            ? 'name'
            : child.classList.contains('temporal-create-title-row__tools')
              ? 'actions'
              : 'unexpected',
      ),
    ).toEqual(['marker', 'name', 'actions']);
    expect(eventTitleRow?.firstElementChild?.textContent).toBe('○');
    const eventLock = screen.getByRole('button', { name: 'Blocca spostamenti' });
    expect(eventTitleRow?.contains(eventLock)).toBe(true);
    expect(eventLock.getAttribute('data-placement-protection')).toBe('event');
    expect(eventLock.getAttribute('aria-pressed')).toBe('false');
    fireEvent.click(eventLock);
    expect(
      screen.getByRole('button', { name: 'Sblocca spostamenti' })
        .getAttribute('aria-pressed'),
    ).toBe('true');
    expect(onU2DraftChange).toHaveBeenCalledWith(
      expect.objectContaining({ eventPlacementProtected: true }),
      'user',
    );
    fireEvent.click(screen.getByRole('button', { name: 'Sblocca spostamenti' }));
    expect(eventLock.getAttribute('aria-pressed')).toBe('false');
    expect(onU2DraftChange).toHaveBeenCalledWith(
      expect.objectContaining({ eventPlacementProtected: false }),
      'user',
    );

    expect(
      screen
        .getByRole('button', { name: 'Aggiungi punto alla scaletta' })
        .classList.contains('temporal-create-tree-add'),
    ).toBe(true);
    const agenda = screen.getByRole('region', { name: 'Scaletta evento' });
    expect(agenda.classList.contains('is-edit')).toBe(true);
    expect(
      agenda.querySelector('.temporal-create-activity-tree__spine'),
    ).not.toBeNull();
    const eventObjectives = screen.getByRole('region', {
      name: 'Configurazione obiettivi',
    });
    expect(
      within(eventObjectives).getByRole('button', {
        name: 'Aggiungi obiettivo',
      }),
    ).toBeTruthy();
    expect(eventObjectives.querySelector('[data-reality-policy]')).toBeNull();
    expect(screen.queryByText('Svolgimento e obiettivi')).toBeNull();
    expect(screen.queryByText('Disponibilità')).toBeNull();
    expect(screen.queryByText('Visibilità')).toBeNull();
    expect(screen.queryByText('Risorse')).toBeNull();
    expect(screen.queryByText('Videocall')).toBeNull();

    expect(
      await screen.findByRole('button', { name: '＋ Aggiungi' }),
    ).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: '＋ Aggiungi' }));
    const selfParticipation = domElement(
      screen.getByRole('combobox', { name: 'Partecipazione di Io' }),
      HTMLSelectElement,
    );
    expect(selfParticipation.value).toBe('required');
    expect(
      selfParticipation.closest('.temporal-create-event-participants__row')
        ?.textContent,
    ).toContain('Io');

    fireEvent.click(
      screen.getByRole('button', { name: 'Aggiungi punto alla scaletta' }),
    );

    expect(onPatch).toHaveBeenCalledTimes(1);
    const patch: unknown = onPatch.mock.calls[0]?.[0];
    if (typeof patch !== 'object' || patch === null || !('event' in patch)) {
      throw new Error('Expected an Event agenda patch.');
    }
    expect(Object.keys(patch)).toEqual(['event']);
    expect(patch.event).toMatchObject({ agendaParts: [''] });
  });

  it('locks background scrolling while Advanced Create owns the viewport', () => {
    const fields = createTemporalCreateFields({
      kind: 'activity',
      date: '2026-10-06',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const session = setTemporalCreateSurface(
      createTemporalCreateSession(fields),
      'full',
    );

    const view = render(
      <TemporalCreateComposer
        session={session}
        contexts={context}
        issues={[]}
        lifecycle="idle"
        failureMessage=""
        postCreateRetry={false}
        u2Draft={createTemporalCreateU2AuthoringDraft(session.draft.current)}
        onPatch={vi.fn()}
        onSurfaceChange={vi.fn()}
        onRequestClose={vi.fn()}
        onContinueEditing={vi.fn()}
        onDiscard={vi.fn()}
        onMoveToUnplaced={vi.fn()}
        onSubmit={vi.fn()}
      />,
    );

    const backdrop = view.container.querySelector<HTMLElement>(
      '[data-temporal-create="backdrop"]',
    );
    const composer = view.container.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );

    expect(backdrop?.classList.contains('is-advanced')).toBe(true);
    expect(backdrop?.classList.contains('is-modal')).toBe(false);
    expect(composer?.getAttribute('aria-modal')).toBe('true');
    expect(document.documentElement.style.overflow).toBe('hidden');
    expect(document.body.style.overflow).toBe('hidden');
    expect(document.documentElement.dataset.temporalCreateScrollLock).toBe(
      'true',
    );

    view.unmount();

    expect(document.documentElement.style.overflow).toBe('');
    expect(document.body.style.overflow).toBe('');
    expect(
      document.documentElement.dataset.temporalCreateScrollLock,
    ).toBeUndefined();
  });

  it('asks the entry to close when an untouched draft is clicked outside', () => {
    const { container, onRequestClose } = renderComposer();
    const backdrop = container.querySelector<HTMLElement>(
      '[data-temporal-create="backdrop"]',
    );
    if (!backdrop) {
      throw new Error('Expected Create backdrop.');
    }

    fireEvent.pointerDown(backdrop);

    expect(onRequestClose).toHaveBeenCalledOnce();
  });

  it('offers cancel, discard and move to unplaced for a changed Activity', () => {
    const { onContinueEditing, onDiscard, onMoveToUnplaced } = renderComposer({
      dirty: true,
    });
    const decision = screen.getByRole('alertdialog');

    fireEvent.click(within(decision).getByRole('button', { name: 'Annulla' }));
    fireEvent.click(
      within(decision).getByRole('button', {
        name: 'Salva bozza',
      }),
    );
    fireEvent.click(within(decision).getByRole('button', { name: 'Scarta' }));

    expect(onContinueEditing).toHaveBeenCalledOnce();
    expect(onMoveToUnplaced).toHaveBeenCalledOnce();
    expect(onDiscard).toHaveBeenCalledOnce();
  });
});

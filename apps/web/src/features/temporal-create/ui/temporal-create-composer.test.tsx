// @vitest-environment jsdom

import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import {
  createTemporalCreateFields,
  createTemporalCreateSession,
  requestTemporalCreateClose,
  updateTemporalCreateFields,
} from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { TemporalCreateComposer } from './temporal-create-composer';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
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
      reminderRetry={false}
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
        name: 'Sposta in Da collocare',
      }),
    );
    fireEvent.click(
      within(decision).getByRole('button', { name: 'Scarta' }),
    );

    expect(onContinueEditing).toHaveBeenCalledOnce();
    expect(onMoveToUnplaced).toHaveBeenCalledOnce();
    expect(onDiscard).toHaveBeenCalledOnce();
  });
});

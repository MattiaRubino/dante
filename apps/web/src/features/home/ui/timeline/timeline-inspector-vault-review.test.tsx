// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { useState } from 'react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { EventDetailDialog } from './timeline-overlays';

vi.mock('./activity-inspector-actions', () => ({
  ActivityInspectorActions: ({
    onVaultReviewChange,
  }: {
    onVaultReviewChange?: (active: boolean) => void;
  }) => {
    function ActivityReviewStub() {
      const [active, setActive] = useState(false);
      return (
        <>
          {!active ? (
            <button type="button" onClick={() => {
              setActive(true);
              onVaultReviewChange?.(true);
            }}>
              Sposta in Bozze
            </button>
          ) : (
            <section role="region" aria-label="Sposta attività in Bozze"
              className="timeline-vault-move-confirmation">
              <button type="button" onClick={() => {
                setActive(false);
                onVaultReviewChange?.(false);
              }}>
                Annulla
              </button>
            </section>
          )}
        </>
      );
    }
    return <ActivityReviewStub />;
  },
}));

vi.mock('../../../temporal/activity-session-card-controls', () => ({
  ActivitySessionCardControls: () => (
    <div data-testid="session-controls">Play / Stop</div>
  ),
}));

vi.mock('../../../temporal/activity-planned-sessions-card-detail', () => ({
  ActivityPlannedSessionsCardDetail: () => (
    <section data-testid="session-details">Sessioni operative</section>
  ),
}));

afterEach(cleanup);

describe('Inspector Vault mode', () => {
  it('switches the parent Inspector into a focused review without unmounting its original details', () => {
    const onClose = vi.fn();
    render(
      <EventDetailDialog
        detail={{
          title: 'Allenamento',
          dateKey: '2026-11-23',
          startMinute: 960,
          endMinute: 990,
          groupLabel: 'Salute',
          ownerKind: 'activity',
        }}
        sessionSubject={{ kind: 'activity', ref: 'activity-1' }}
        opener={null}
        onActivitySaved={vi.fn()}
        onActivityDeleted={vi.fn()}
        onClose={onClose}
      />,
    );
    const inspector = screen.getByRole('dialog');
    expect(inspector.className).not.toContain('timeline-event-modal--vault-review');
    expect(screen.getByTestId('session-details')).toBeTruthy();
    expect(screen.getByTestId('session-controls')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Sposta in Bozze' }));
    expect(inspector.className).toContain('timeline-event-modal--vault-review');
    const review = screen.getByRole('region', { name: 'Sposta attività in Bozze' });
    expect(review.parentElement).toBe(inspector);
    // Original details remain mounted so Cancel restores exactly the same
    // Inspector state; the Vault mode CSS removes them from layout and A11y.
    expect(screen.getByTestId('session-details')).toBeTruthy();
    fireEvent.click(within(review).getByRole('button', { name: 'Annulla' }));
    expect(inspector.className).not.toContain('timeline-event-modal--vault-review');
    expect(screen.getByTestId('session-details')).toBeTruthy();
    expect(onClose).not.toHaveBeenCalled();
  });
});

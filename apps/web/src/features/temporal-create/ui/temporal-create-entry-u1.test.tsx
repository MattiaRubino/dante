// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

describe('Temporal Create U1 entry', () => {
  it('keeps the + entry interactive while canonical Life Area readiness is pending', () => {
    const onPreview = vi.fn();
    const { container } = render(
      <>
        <div data-home-context-create-host />
        <TemporalCreateEntry
          defaultDate={Temporal.PlainDate.from('2026-09-30')}
          contexts={[
            {
              id: 'pending-area',
              label: 'Area in caricamento',
              tone: 'personal',
            },
          ]}
          onPreview={onPreview}
          onApplied={() => false}
          creationEnabled={false}
        />
      </>,
    );

    const quickAdd = container.querySelector<HTMLButtonElement>(
      '.dante-timeline-quick-add',
    );
    if (!quickAdd) {
      throw new Error('Expected Create trigger.');
    }

    expect(quickAdd.disabled).toBe(false);
    expect(quickAdd.dataset.createReady).toBe('false');
    fireEvent.click(quickAdd);

    const host = container.querySelector('[data-home-context-create-host]');
    expect(host?.querySelector('[data-temporal-create="composer"]')).not.toBeNull();
    expect(quickAdd.getAttribute('aria-expanded')).toBe('true');
  });
});

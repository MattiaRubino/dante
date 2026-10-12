// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { TemporalCreateEntry } from './temporal-create-entry';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function renderEntry() {
  const onPreview = vi.fn();
  const rendered = render(
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
  const quickAdd = rendered.container.querySelector<HTMLButtonElement>(
    '.dante-timeline-quick-add',
  );
  if (!quickAdd) {
    throw new Error('Expected Create trigger.');
  }
  const host = rendered.container.querySelector<HTMLElement>(
    '[data-home-context-create-host]',
  );
  if (!host) {
    throw new Error('Expected Create host.');
  }
  return { ...rendered, quickAdd, host };
}

describe('Temporal Create U1 entry', () => {
  it('keeps the + entry interactive while canonical Life Area readiness is pending', () => {
    const { quickAdd, host } = renderEntry();

    expect(quickAdd.disabled).toBe(false);
    expect(quickAdd.dataset.createReady).toBe('false');
    fireEvent.click(quickAdd);

    expect(host.querySelector('[data-temporal-create="composer"]')).not.toBeNull();
    expect(quickAdd.getAttribute('aria-expanded')).toBe('true');
  });

  it('dismisses an unnamed draft even after provisional time edits', () => {
    const { quickAdd, host } = renderEntry();
    fireEvent.click(quickAdd);

    const composer = host.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    const time = host.querySelector<HTMLInputElement>(
      '[data-create-path="startTime"]',
    );
    if (!composer || !time) {
      throw new Error('Expected open Create composer and time field.');
    }

    fireEvent.change(time, { target: { value: '11:15' } });
    fireEvent.keyDown(composer, { key: 'Escape' });

    expect(host.querySelector('[data-temporal-create="composer"]')).toBeNull();
    expect(
      document.body.querySelector('[data-temporal-create="discard-modal"]'),
    ).toBeNull();
  });

  it('protects a titled draft with a discard dialog portaled to the viewport', () => {
    const { quickAdd, host } = renderEntry();
    fireEvent.click(quickAdd);

    const composer = host.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    const title = host.querySelector<HTMLInputElement>(
      '[data-create-path="title"]',
    );
    if (!composer || !title) {
      throw new Error('Expected open Create composer and title field.');
    }

    fireEvent.change(title, { target: { value: 'Allenamento' } });
    fireEvent.keyDown(composer, { key: 'Escape' });

    const modal = document.body.querySelector<HTMLElement>(
      '[data-temporal-create="discard-modal"]',
    );
    expect(modal).not.toBeNull();
    expect(host.contains(modal)).toBe(false);
    expect(screen.getByText('Scartare questa bozza?')).toBeTruthy();
  });
});

// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TemporalLifeAreaSelect } from './temporal-life-area-select';

const areas = [
  { id: 'area-studio', label: 'Studio', colorCode: '#4285F4' },
  { id: 'area-projects', label: 'Progetti', colorCode: '#FFCB00' },
  { id: 'area-home', label: 'Casa', colorCode: '#00AA77' },
] as const;

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('Life Area selector in Event and Activity Edit', () => {
  // Regression 2026-11-09: opening an editor for an already-assigned item
  // filtered the catalog down to its own Life Area. Users could not see
  // other existing areas without manually deleting the selected label.
  it('shows the full catalog when focusing an already-selected Life Area', () => {
    const choose = vi.fn();
    render(
      <TemporalLifeAreaSelect
        query="Studio"
        options={areas}
        selectedId="area-studio"
        onQueryChange={vi.fn()}
        onChoose={choose}
        onClear={vi.fn()}
      />,
    );

    fireEvent.focus(screen.getByRole('textbox', { name: 'Life Area (opzionale)' }));
    expect(screen.getAllByRole('option')).toHaveLength(3);
    fireEvent.click(screen.getByRole('option', { name: 'Progetti' }));
    expect(choose).toHaveBeenCalledWith(areas[1]);
  });

  // Regression safeguard: once the user really types a different query,
  // filtering must still work; displaying every area must not break search.
  it('filters by a new typed name while retaining the existing selection ID', () => {
    render(
      <TemporalLifeAreaSelect
        query="Pro"
        options={areas}
        selectedId="area-studio"
        onQueryChange={vi.fn()}
        onChoose={vi.fn()}
        onClear={vi.fn()}
      />,
    );

    fireEvent.focus(screen.getByRole('textbox', { name: 'Life Area (opzionale)' }));
    expect(screen.getAllByRole('option')).toHaveLength(1);
    expect(screen.getByRole('option', { name: 'Progetti' })).toBeTruthy();
  });
});

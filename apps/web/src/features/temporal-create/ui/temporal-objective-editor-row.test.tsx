// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';

import type { TemporalCreateObjectiveDraft } from '../model/temporal-create-u2-authoring';
import { TemporalObjectiveEditorRow } from './temporal-objective-editor-row';

const objective: TemporalCreateObjectiveDraft = {
  id: 'local-objective',
  label: 'Corsa',
  resultKind: 'quantity',
  comparatorCode: 'gte',
  targetValue: '5',
  targetMin: '',
  targetMax: '',
  unitCode: 'km',
};

function show(variant: 'create' | 'edit', disabled = false) {
  const update = vi.fn();
  const changeKind = vi.fn();
  const move = vi.fn();
  const remove = vi.fn();
  const result = render(
    <TemporalObjectiveEditorRow
      objective={objective}
      index={0}
      total={2}
      variant={variant}
      italian
      disabled={disabled}
      update={update}
      changeKind={changeKind}
      move={move}
      remove={remove}
    />,
  );
  return { ...result, update, changeKind, move, remove };
}

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('shared Objective row presentation', () => {
  it('uses one identical structure for Advanced Create and Activity Edit', () => {
    const create = show('create');
    const structure = (root: HTMLElement) =>
      Array.from(
        root.querySelectorAll(
          '.temporal-create-objective__row, .temporal-create-objective__definition, .temporal-create-objective__actions',
        ),
      ).map((element) => element.className);
    const createStructure = structure(create.container);
    const labels = create.container.querySelectorAll(
      '.temporal-create-objective__definition label',
    ).length;
    create.unmount();

    const edit = show('edit');
    expect(structure(edit.container)).toEqual(createStructure);
    expect(
      edit.container.querySelectorAll(
        '.temporal-create-objective__definition label',
      ),
    ).toHaveLength(labels);
    expect(screen.getByRole('textbox', { name: 'Nome obiettivo' })).toBeTruthy();
    expect(screen.getByRole('combobox', { name: 'Tipo obiettivo' })).toBeTruthy();
    expect(screen.getByRole('spinbutton', { name: 'Valore obiettivo' })).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Rimuovi obiettivo Corsa' }),
    ).toBeTruthy();
  });

  it('leaves create editing, kind changes, order and removal to owner callbacks', () => {
    const control = show('create');
    fireEvent.change(screen.getByRole('textbox', { name: 'Obiettivo 1' }), {
      target: { value: 'Camminare' },
    });
    expect(control.update).toHaveBeenCalledWith('local-objective', {
      label: 'Camminare',
    });
    fireEvent.change(
      screen.getByRole('combobox', { name: 'Tipo risultato obiettivo 1' }),
      { target: { value: 'range' } },
    );
    expect(control.changeKind).toHaveBeenCalledWith('local-objective', 'range');
    fireEvent.click(screen.getByRole('button', { name: 'Sposta obiettivo giù' }));
    expect(control.move).toHaveBeenCalledWith(0, 1);
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi obiettivo' }));
    expect(control.remove).toHaveBeenCalledWith('local-objective');
  });

  it('renders without i18next context for Activity Edit', () => {
    const view = show('edit');
    expect(
      screen.getByRole('textbox', { name: 'Nome obiettivo' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Rimuovi obiettivo Corsa' }),
    ).toBeTruthy();
    view.unmount();
  });

  it('disables edit controls during a pending Activity mutation', () => {
    const result = show('edit', true);
    const row = result.container.querySelector<HTMLElement>(
      '[data-objective-id="local-objective"]',
    );
    expect(row).not.toBeNull();
    if (!row) return;
    for (const element of within(row).getAllByRole('button')) {
      expect((element as HTMLButtonElement).disabled).toBe(true);
    }
    expect(
      (screen.getByRole('textbox', { name: 'Nome obiettivo' }) as HTMLInputElement)
        .disabled,
    ).toBe(true);
    expect(
      (screen.getByRole('combobox', { name: 'Tipo obiettivo' }) as HTMLSelectElement)
        .disabled,
    ).toBe(true);
  });
});

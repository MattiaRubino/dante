// @vitest-environment jsdom
import {
  cleanup,
  fireEvent,
  render,
  screen,
  within,
} from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { TemporalCreateObjectiveDraft } from '../model/temporal-create-u2-authoring';
import { objectiveFieldIssue, objectiveFieldIssues } from '../model/temporal-objective-validation';
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

afterEach(cleanup);

describe('shared Objective row presentation', () => {
  it.each(['create', 'edit'] as const)(
    'marks only the missing name in the %s Objective row',
    (variant) => {
      const missing = { ...objective, label: '' };
      const view = render(
        <TemporalObjectiveEditorRow
          objective={missing}
          index={0}
          total={1}
          variant={variant}
          italian
          issue={objectiveFieldIssue(missing)}
          update={vi.fn()}
          changeKind={vi.fn()}
          move={vi.fn()}
          remove={vi.fn()}
        />,
      );
      const name = view.container.querySelector<HTMLInputElement>(
        '.temporal-create-objective__title',
      );
      expect(name?.getAttribute('aria-invalid')).toBe('true');
      expect(name?.closest('[data-field-invalid]')).not.toBeNull();
      expect(view.container.querySelectorAll('[data-field-invalid="true"]')).toHaveLength(1);
      expect(view.container.querySelector('[role="alert"]')).toBeNull();
    },
  );

  it.each(['create', 'edit'] as const)(
    'keeps Min intact and identifies Max for an equal %s interval',
    (variant) => {
      const equal = {
        ...objective,
        resultKind: 'range' as const,
        comparatorCode: 'between' as const,
        targetMin: '2.5',
        targetMax: '2.5',
      };
      const view = render(
        <TemporalObjectiveEditorRow
          objective={equal}
          index={0}
          total={1}
          variant={variant}
          italian
          issue={objectiveFieldIssue(equal)}
          update={vi.fn()}
          changeKind={vi.fn()}
          move={vi.fn()}
          remove={vi.fn()}
        />,
      );
      const min = screen.getByRole('spinbutton', { name: 'Minimo obiettivo' });
      const max = screen.getByRole('spinbutton', { name: 'Massimo obiettivo' });
      expect(min.getAttribute('aria-invalid')).toBeNull();
      expect(max.getAttribute('aria-invalid')).toBe('true');
      expect((max as HTMLInputElement).value).toBe('2.5');
      expect(screen.getByRole('alert').textContent).toBe('Max deve superare Min.');
      expect(view.container.querySelectorAll('[data-field-invalid="true"]')).toHaveLength(1);
    },
  );

  it('identifies both missing name and numeric target without extra visible messages', () => {
    const incomplete = { ...objective, label: '', targetValue: '' };
    const view = render(
      <TemporalObjectiveEditorRow
        objective={incomplete}
        index={0}
        total={1}
        italian
        issues={objectiveFieldIssues(incomplete)}
        update={vi.fn()}
        changeKind={vi.fn()}
        move={vi.fn()}
        remove={vi.fn()}
      />,
    );
    expect(view.container.querySelectorAll('[data-field-invalid="true"]')).toHaveLength(2);
    expect(view.container.querySelectorAll('[role="alert"]')).toHaveLength(0);
  });

  it('explains an invalid numeric target at that field only', () => {
    expect(objectiveFieldIssues({ ...objective, targetValue: 'parole' })).toEqual([
      { field: 'targetValue', message: 'Inserisci un numero.' },
    ]);
    expect(objectiveFieldIssues({
      ...objective,
      resultKind: 'range',
      comparatorCode: 'between',
      targetMin: '5',
      targetMax: '4',
    })).toEqual([{ field: 'targetMax', message: 'Max deve superare Min.' }]);
  });
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
    expect(
      screen.getByRole('textbox', { name: 'Nome obiettivo' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('combobox', { name: 'Tipo obiettivo' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('spinbutton', { name: 'Valore obiettivo' }),
    ).toBeTruthy();
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
    fireEvent.click(
      screen.getByRole('button', { name: 'Sposta obiettivo giù' }),
    );
    expect(control.move).toHaveBeenCalledWith(0, 1);
    fireEvent.click(screen.getByRole('button', { name: 'Rimuovi obiettivo' }));
    expect(control.remove).toHaveBeenCalledWith('local-objective');
  });

  it.each(['create', 'edit'] as const)(
    'exposes one Objective-specific verification selector in %s',
    (variant) => {
      const control = show(variant);
      const chooser = screen.getByRole('combobox', {
        name: 'Verifica obiettivo 1',
      });
      expect(chooser).toHaveProperty('value', 'none');
      expect(
        within(chooser).getByRole('option', {
          name: 'Valutazione automatica · non disponibile',
        }),
      ).toHaveProperty('disabled', true);
      fireEvent.change(chooser, { target: { value: 'review_on_end' } });
      expect(control.update).toHaveBeenCalledWith('local-objective', {
        verificationMode: 'review_on_end',
      });
    },
  );

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
      expect(element.hasAttribute('disabled')).toBe(true);
    }
    expect(
      screen.getByRole('textbox', { name: 'Nome obiettivo' }),
    ).toHaveProperty('disabled', true);
    expect(
      screen.getByRole('combobox', { name: 'Tipo obiettivo' }),
    ).toHaveProperty('disabled', true);
  });
});

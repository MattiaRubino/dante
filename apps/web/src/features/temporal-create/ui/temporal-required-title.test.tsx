// @vitest-environment jsdom
import { act, renderHook } from '@testing-library/react';
import { expect, it } from 'vitest';

import { useTemporalRequiredTitle } from './temporal-required-title';

it('only marks an empty title after an attempted save and resets after a valid edit', () => {
  const view = renderHook(
    ({ value }: { value: string }) => useTemporalRequiredTitle(value),
    { initialProps: { value: '' } },
  );
  expect(view.result.current.invalid).toBe(false);
  act(() => expect(view.result.current.validate()).toBe(false));
  expect(view.result.current.invalid).toBe(true);
  expect(view.result.current.shakeAttempt).toBe(1);
  act(() => expect(view.result.current.validate()).toBe(false));
  expect(view.result.current.shakeAttempt).toBe(2);

  act(() => view.result.current.changed('Nuovo titolo'));
  view.rerender({ value: 'Nuovo titolo' });
  expect(view.result.current.invalid).toBe(false);
  expect(view.result.current.validate()).toBe(true);
  view.rerender({ value: '' });
  expect(view.result.current.invalid).toBe(false);
  act(() => expect(view.result.current.validate()).toBe(false));
  expect(view.result.current.invalid).toBe(true);
});

it('rejects whitespace-only titles without treating them as saved content', () => {
  const { result } = renderHook(() => useTemporalRequiredTitle('   '));
  act(() => expect(result.current.validate()).toBe(false));
  expect(result.current.invalid).toBe(true);
});

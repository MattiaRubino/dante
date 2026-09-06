import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import {
  WorldFocusQualifier,
  WorldFocusQualifierGroup,
} from './world-focus-qualifiers';

afterEach(cleanup);

describe('World Focus M2 qualifier grammar', () => {
  it('communicates axis and state with visible text rather than color alone', () => {
    render(
      <WorldFocusQualifierGroup aria-label="Qualificazioni">
        <WorldFocusQualifier axis="freshness" state="stale">
          Non aggiornato
        </WorldFocusQualifier>
      </WorldFocusQualifierGroup>,
    );

    const qualifier = screen.getByText('Non aggiornato');
    expect(qualifier.getAttribute('data-world-focus-qualifier-axis')).toBe(
      'freshness',
    );
    expect(qualifier.getAttribute('data-world-focus-qualifier-state')).toBe(
      'stale',
    );
  });
});

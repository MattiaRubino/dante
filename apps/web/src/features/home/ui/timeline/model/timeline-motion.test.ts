import { describe, expect, it } from 'vitest';

import { timelineEffectiveScrollBehavior } from './timeline-motion';

describe('timeline motion policy', () => {
  it('downgrades requested smooth scrolling when reduced motion is enabled', () => {
    expect(timelineEffectiveScrollBehavior('smooth', true)).toBe('auto');
  });

  it('keeps smooth scrolling when reduced motion is not requested', () => {
    expect(timelineEffectiveScrollBehavior('smooth', false)).toBe('smooth');
  });

  it('preserves already non-animated scrolling', () => {
    expect(timelineEffectiveScrollBehavior('auto', true)).toBe('auto');
    expect(timelineEffectiveScrollBehavior('auto', false)).toBe('auto');
  });
});

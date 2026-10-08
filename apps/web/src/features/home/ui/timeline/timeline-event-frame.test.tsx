// @vitest-environment jsdom
import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { eventFrameGeometry, TimelineEventFrame } from './timeline-event-frame';

describe('Event frame geometry', () => {
  it('uses the original uncut artwork for a short card', () => {
    const { container } = render(<TimelineEventFrame />);
    const frame = container.querySelector('.timeline-event-frame');
    expect(frame?.querySelectorAll('svg')).toHaveLength(1);
    expect(frame?.querySelector('svg')?.getAttribute('viewBox')).toBe('0 0 772 305');
    expect(frame?.querySelectorAll('path')).toHaveLength(1);
  });

  it('changes only the straight middle when the height grows', () => {
    const standard = eventFrameGeometry(280, 300);
    const tall = eventFrameGeometry(280, 900);
    expect(standard.topHeight).toBe(tall.topHeight);
    expect(standard.bottomHeight).toBe(tall.bottomHeight);
    expect(tall.addedHeight - standard.addedHeight).toBe(600);
    expect(tall.topHeight + tall.addedHeight + tall.bottomHeight).toBeCloseTo(900);
  });
});

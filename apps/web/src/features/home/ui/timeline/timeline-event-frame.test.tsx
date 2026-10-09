// @vitest-environment jsdom
import { render } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import { eventFrameGeometry, TimelineEventFrame } from './timeline-event-frame';

describe('Event frame geometry', () => {
  it('renders the two full, mirrored ribbons without clipped segments', () => {
    const { container } = render(<TimelineEventFrame />);
    const frame = container.querySelector('.timeline-event-frame');
    expect(frame?.querySelectorAll('svg')).toHaveLength(0);
    expect(frame?.querySelectorAll('use')).toHaveLength(2);
    expect(frame?.querySelectorAll('path')).toHaveLength(1);
  });

  it('keeps both horizontal rims two pixels inside compact and tall cards', () => {
    for (const [width, height] of [[280, 48], [280, 305], [280, 900]] as const) {
      const frame = eventFrameGeometry(width, height);
      expect(frame.ribbon).toContain(' 2 L');
      expect(frame.mirrorTransform).toBe(`translate(${width} ${height}) scale(-1 -1)`);
      expect(frame.ribbon).not.toMatch(/NaN|Infinity/);
    }
    expect(eventFrameGeometry(280, 900).ribbon).toContain('M 2.9 788');
  });

  it('keeps the approved reference shape while mapping its canvas margin into the card', () => {
    const reference = eventFrameGeometry(772, 305);
    expect(reference.ribbon).toContain('M 8 193 L 66 36');
    expect(reference.ribbon).toContain('L 727 2');
    expect(reference.mirrorTransform).toBe('translate(772 305) scale(-1 -1)');
  });
});

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

  it('extends just the straight sides and mirrors the bottom within card height', () => {
    const short = eventFrameGeometry(280, 305);
    const tall = eventFrameGeometry(280, 900);
    expect(short.ribbon).toContain('L 23.94 61');
    expect(tall.ribbon).toContain('L 23.94 61');
    expect(short.ribbon).toContain('M 2.9 218');
    expect(tall.ribbon).toContain('M 2.9 813');
    expect(tall.mirrorTransform).toBe('translate(280 876) scale(-1 -1)');
  });

  it('keeps the approved reference coordinates at its native size', () => {
    const reference = eventFrameGeometry(772, 305);
    expect(reference.ribbon).toContain('M 8 218 L 66 61');
    expect(reference.ribbon).toContain('L 727 27');
    expect(reference.mirrorTransform).toBe('translate(772 281) scale(-1 -1)');
  });
});

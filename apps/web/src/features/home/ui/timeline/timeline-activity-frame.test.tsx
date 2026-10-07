// @vitest-environment jsdom

import { cleanup, render } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import { TimelineActivityFrame } from './timeline-activity-frame';

afterEach(cleanup);

describe('Activity Timeline corner', () => {
  it('renders one decorative lower-right reinforcement', () => {
    const { container } = render(<TimelineActivityFrame />);
    const frame = container.querySelector('svg.timeline-activity-frame');

    expect(frame?.getAttribute('aria-hidden')).toBe('true');
    expect(frame?.querySelectorAll('path')).toHaveLength(1);
    expect(frame?.querySelector('path')?.getAttribute('d')).toContain('C52');
  });
});

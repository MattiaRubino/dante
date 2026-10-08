// @vitest-environment jsdom

import { cleanup, render } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import {
  activityFramePath,
  TimelineActivityFrame,
} from './timeline-activity-frame';

afterEach(cleanup);

describe('Activity Timeline frame', () => {
  it('keeps one continuous rim at prototype and compact card sizes', () => {
    for (const [width, height] of [
      [626, 198],
      [160, 48],
      [55, 28],
    ] as const) {
      const { d, radius } = activityFramePath(width, height);
      expect(d.match(/M/g)).toHaveLength(2); // outside and inside of one ring
      expect(d).not.toMatch(/NaN|Infinity/);
      expect(radius).toBeLessThan(Math.min(width, height) / 2);
    }
    expect(activityFramePath(626, 198).radius).toBe(30);
    expect(activityFramePath(260, 460).radius).toBe(30);
  });

  it('gives each card its own gradient and keeps the frame out of the accessibility tree', () => {
    const { container } = render(
      <>
        <article>
          <TimelineActivityFrame />
        </article>
        <article>
          <TimelineActivityFrame />
        </article>
      </>,
    );
    const frames = [
      ...container.querySelectorAll('svg.timeline-activity-frame'),
    ];
    const gradients = frames.map(
      (frame) => frame.querySelector('linearGradient')?.id,
    );
    expect(gradients[0]).toBeTruthy();
    expect(gradients[0]).not.toBe(gradients[1]);
    frames.forEach((frame, index) => {
      expect(frame.getAttribute('aria-hidden')).toBe('true');
      expect(frame.querySelector('path')?.getAttribute('fill')).toBe(
        `url(#${gradients[index]})`,
      );
    });
  });
});

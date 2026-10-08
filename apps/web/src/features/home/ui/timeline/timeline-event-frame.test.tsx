import { describe, expect, it } from 'vitest';

import { eventFrameGeometry } from './timeline-event-frame';

describe('Event frame at different schedule heights', () => {
  it('keeps the corner geometry fixed and connects both side ribbons on tall cards', () => {
    const medium = eventFrameGeometry(280, 300);
    const tall = eventFrameGeometry(280, 900);
    expect(medium.topTransform).toBe(tall.topTransform);
    expect(tall.bridge).toContain('830');
    const bottomOffset = Number(tall.bottomTransform.match(/ 280 ([^)]+)\)/)?.[1]);
    expect(bottomOffset).toBeGreaterThan(900);
    expect(tall.bridge).not.toBe('');
  });

  it('does not stretch a short card corner into a thick diagonal', () => {
    const short = eventFrameGeometry(280, 100);
    const medium = eventFrameGeometry(280, 300);
    const shortScale = Number(short.topTransform.match(/matrix\([^ ]+ 0 0 ([^ ]+)/)?.[1]);
    const mediumScale = Number(medium.topTransform.match(/matrix\([^ ]+ 0 0 ([^ ]+)/)?.[1]);
    expect(shortScale).toBeGreaterThan(0);
    expect(shortScale).toBeLessThan(mediumScale);
    expect(short.bridge).not.toBe('');
  });
});

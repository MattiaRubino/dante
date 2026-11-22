import { describe, expect, it } from 'vitest';

import { positionDateLaneInspector } from './timeline-inspector-position';

const viewport = { width: 1200, height: 850 };
const panel = { width: 540, height: 590 };
const wideBar = { left: 100, right: 1170, top: 90, bottom: 130 };

describe('date-lane Inspector anchored at the clicked point', () => {
  it('uses click position, not the right edge of a full-width bar', () => {
    expect(
      positionDateLaneInspector(wideBar, viewport, panel, {
        clientX: 180,
        clientY: 111,
      }),
    ).toEqual({ left: 192, top: 142 });
  });

  it('flips to the left without clipping near the far right', () => {
    expect(
      positionDateLaneInspector(wideBar, viewport, panel, {
        clientX: 1030,
        clientY: 111,
      }),
    ).toEqual({ left: 478, top: 142 });
  });

  it('chooses a clamped position for tall inspectors and limited space', () => {
    const position = positionDateLaneInspector(
      { left: 10, right: 900, top: 460, bottom: 500 },
      { width: 980, height: 620 },
      { width: 540, height: 530 },
      { clientX: 390, clientY: 478 },
    );
    expect(position).toEqual({ left: 402, top: 78 });
  });

  it('uses the title end for keyboard activation and bounds narrow viewports', () => {
    const keyboard = positionDateLaneInspector(wideBar, viewport, panel);
    expect(keyboard.left).toBe(184);
    const mobile = positionDateLaneInspector(
      { left: 20, right: 350, top: 60, bottom: 102 },
      { width: 375, height: 600 },
      { width: 351, height: 504 },
      { clientX: 340, clientY: 90 },
    );
    expect(mobile.left).toBe(12);
    expect(mobile.top).toBeGreaterThanOrEqual(12);
    expect(mobile.top).toBeLessThanOrEqual(84);
  });

  it('never places an overflow-list item Inspector outside the viewport', () => {
    const result = positionDateLaneInspector(
      { left: 90, right: 1150, top: 765, bottom: 807 },
      viewport,
      panel,
      { clientX: 1110, clientY: 781 },
    );
    expect(result.left).toBeGreaterThanOrEqual(12);
    expect(result.left + panel.width).toBeLessThanOrEqual(viewport.width - 12);
    expect(result.top).toBeGreaterThanOrEqual(12);
    expect(result.top + panel.height).toBeLessThanOrEqual(viewport.height - 12);
  });
});

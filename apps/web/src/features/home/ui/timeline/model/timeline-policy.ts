export const TIMELINE_MINUTES_PER_DAY = 24 * 60;

export const TIMELINE_POLICY = {
  density: {
    slotMinutes: 15,
    baseScale: 0.72,
    minScale: 0.72,
    maxScale: 2.85,
    maxLocalScale: 6.2,
    smoothingRadiusMinutes: 7,
    burstWindowMinutes: 60,
    eventPressureBaselineCount: 5,
    concurrencyPressureBaselineCount: 1,
    burstPressureBaselineCount: 3,
    activeOverlapBaselineCount: 1,
    nearbyStartBaselineCount: 2,
    eventPressurePerItem: 0.045,
    concurrencyPressurePerItem: 0.15,
    overlapPressureFactor: 0.28,
    shortEventPressurePerItem: 0.032,
    burstPressurePerItem: 0.085,
    activeOverlapFactor: 0.24,
    nearbyStartFactor: 0.095,
    shortActiveFactor: 0.1,
    nearbyStartWindowMinutes: 30,
    shortEventThresholdMinutes: 30,
    readableHeightShoulderMinutes: 4,
    readableHeightShoulderEasePadding: 2,
  },
  zoom: {
    min: 0.75,
    max: 2.1,
    precisionThreshold: 1.75,
    wheelStepFactor: 1.12,
    controlStepFactor: 1.18,
  },
  drag: {
    defaultSnapMinutes: 5,
    precisionSnapMinutes: 1,
    activationDistancePx: 7,
    autoScrollEdgePx: 56,
    autoScrollMinPxPerSecond: 100,
    autoScrollMaxPxPerSecond: 700,
    autoScrollMaxFrameSeconds: 0.05,
  },
  event: {
    readableHeightThresholdMinutes: {
      upTo5Minutes: 5,
      upTo15Minutes: 15,
      upTo30Minutes: 30,
      upTo45Minutes: 45,
      upTo60Minutes: 60,
      upTo90Minutes: 90,
    },
    readableHeightPx: {
      upTo5Minutes: 50,
      upTo15Minutes: 68,
      upTo30Minutes: 78,
      upTo45Minutes: 84,
      upTo60Minutes: 90,
      upTo90Minutes: 96,
      longer: 102,
    },
    subitemsMinimumHeightPx: 98,
    expandedSubitemsBaseExtraHeightPx: 18,
    expandedSubitemExtraHeightPx: 27,
    longTitleThreshold: 34,
    longTitleMaxDurationMinutes: 30,
    longTitleExtraHeightPx: 6,
  },
  window: {
    initialPastDays: 1,
    initialFutureDays: 3,
    extendByDays: 3,
    maxPastDays: 14,
    maxFutureDays: 14,
    extendPastTriggerPx: 420,
    extendFutureTriggerPx: 500,
  },
  viewport: {
    expandedMinWidthPx: 1121,
    contextProbeRatio: 0.34,
    nowOffsetRatio: 0.34,
    nowOffsetMinPx: 80,
    defaultGridHeightPx: 570,
    initialExternalMinute: 8 * 60,
    initialExternalOffsetPx: 70,
    horizontalSyncTolerancePx: 0.5,
    eventRevealInsetPx: 16,
  },
  feedback: {
    toastDurationMs: 5000,
  },
  expansion: {
    groupOpacityStart: 0.16,
    groupOpacityRange: 0.52,
    cardMinWidthPx: 24,
    cardLaneGapPx: 8,
    cardInsetPx: 4,
    settledProgress: 0.98,
    dragActivationDistancePx: 4,
    settleThreshold: 0.5,
    defaultContextRailWidthPx: 190,
    minDragDistancePx: 110,
  },
  grid: {
    minorLineIntervalMinutes: 30,
    majorLineIntervalMinutes: 60,
    milestoneMinutes: [9 * 60, 18 * 60],
    marginLabelCutoffMinute: 20 * 60,
    marginLabelOffsetPx: 4,
  },
  layout: {
    rulerWidthPx: 84,
    expansionHandleGutterPx: 14,
    groupMinWidthPx: 260,

    /*
     * The group header and the event layer share these exact horizontal insets.
     * Runtime expansion derives its chrome width from their sum, so header,
     * group columns, scroll range and event columns cannot drift independently.
     */
    eventsLeftInsetPx: 44,
    eventsRightInsetPx: 16,

    compactLeftInsetPercent: 1.4,
    compactLaneRegionPercent: 91.6,
    compactTargetLaneWidthPercent: 18,
    compactMaxLeftPercent: 64,
    compactMaxRightPercent: 94,
    compactMultiLaneGapPercent: 1,

    /*
     * Isolated cards are measured from the actual rendered content at runtime.
     * These bounds are presentation policy, not fixture heuristics: they work
     * for arbitrary titles/locales while preventing both postage-stamp cards
     * and giant empty slabs on wide timelines.
     */
    compactIntrinsicMinWidthPx: 190,
    compactIntrinsicMaxWidthPx: 480,
    compactIntrinsicResponsiveMaxFloorPx: 280,
    compactIntrinsicMaxViewportRatio: 0.42,
    compactIntrinsicHorizontalBreathingPx: 32,
  },
} as const;

export function clampTimelineZoom(value: number): number {
  return Math.max(
    TIMELINE_POLICY.zoom.min,
    Math.min(TIMELINE_POLICY.zoom.max, value),
  );
}

export function timelineDragSnapMinutes(zoom: number): number {
  return zoom >= TIMELINE_POLICY.zoom.precisionThreshold
    ? TIMELINE_POLICY.drag.precisionSnapMinutes
    : TIMELINE_POLICY.drag.defaultSnapMinutes;
}

export function timelineSupportsExpandedLayout(viewportWidth: number): boolean {
  return viewportWidth >= TIMELINE_POLICY.viewport.expandedMinWidthPx;
}

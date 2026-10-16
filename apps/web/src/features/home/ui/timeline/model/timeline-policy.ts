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
    defaultSnapMinutes: 1,
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
    activityMinimumHeightPx: 116,
    eventMinimumHeightPx: 88,
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
    pastBufferDays: 1,
    futureBufferDays: 3,
    shiftByDays: 2,
    recyclePastTriggerPx: 420,
    recycleFutureTriggerPx: 500,
    recycleAnchorViewportOffsetPx: 1,
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
  scrubber: {
    edgeInsetPx: 26,
    deadZoneRatio: 0.07,
    minPxPerSecond: 180,
    maxPxPerSecond: 4200,
    velocityExponent: 1.65,
    maxFrameSeconds: 0.05,
    keyboardStepPx: 72,
    keyboardPageRatio: 0.82,
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
    defaultContextRailWidthPx: 475,
    minDragDistancePx: 110,
  },
  grid: {
    minorLineIntervalMinutes: 15,
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
    compactTargetLaneWidthPercent: 24,
    compactMaxLeftPercent: 64,
    compactMaxRightPercent: 94,
    compactMultiLaneGapPercent: 1,

    /*
     * Isolated cards are measured from the actual rendered content at runtime.
     * These bounds are presentation policy, not fixture heuristics: they work
     * for arbitrary titles/locales while preventing both postage-stamp cards
     * and giant empty slabs on wide timelines.
     */
    compactIntrinsicMinWidthPx: 280,
    compactIntrinsicMaxWidthPx: 520,
    compactIntrinsicResponsiveMaxFloorPx: 280,
    compactIntrinsicMaxViewportRatio: 0.42,
    compactIntrinsicHorizontalBreathingPx: 32,

    // Identity-only card sizing. Time changes, Play/Pause/Stop, lane count and
    // Timeline expansion must NEVER change an individual card's width.
    activityCardMinimumWidthPx: 352,
    eventCardMinimumWidthPx: 292,
    cardMaximumWidthPx: 456,
    cardLongTitleThreshold: 44,
    cardLongTitleGrowthPerCharacterPx: 3,
    cardLaneGapPx: 12,
    weekCardMinimumWidthPx: 172,
  },
} as const;

export function clampTimelineZoom(value: number): number {
  return Math.max(
    TIMELINE_POLICY.zoom.min,
    Math.min(TIMELINE_POLICY.zoom.max, value),
  );
}

export function stepTimelineZoom(current: number, factor: number): number {
  if (!Number.isFinite(factor) || factor <= 0) return current;
  return clampTimelineZoom(current * factor);
}

export function timelineDragSnapMinutes(zoom: number): number {
  return zoom >= TIMELINE_POLICY.zoom.precisionThreshold
    ? TIMELINE_POLICY.drag.precisionSnapMinutes
    : TIMELINE_POLICY.drag.defaultSnapMinutes;
}

export function timelineSupportsExpandedLayout(viewportWidth: number): boolean {
  return viewportWidth >= TIMELINE_POLICY.viewport.expandedMinWidthPx;
}


/**
 * Immutable presentation width for one Activity/Event. The title is permitted
 * to enlarge a card within a hard cap; excessively long titles are ellipsized
 * by CSS. Session state, Schedule position and overlap lanes are not inputs.
 */
export function timelineStableCardWidth(
  title: string,
  activity: boolean,
): number {
  const policy = TIMELINE_POLICY.layout;
  const minimum = activity
    ? policy.activityCardMinimumWidthPx
    : policy.eventCardMinimumWidthPx;
  const additional = Math.max(
    0,
    title.length - policy.cardLongTitleThreshold,
  ) * policy.cardLongTitleGrowthPerCharacterPx;
  return Math.min(policy.cardMaximumWidthPx, minimum + additional);
}

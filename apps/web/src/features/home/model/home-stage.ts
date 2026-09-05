export const HOME_STAGE_CONTRACT_VERSION = '0.2.0' as const;

export type HomeStageMode = 'home.stage.continuity' | 'home.stage.signals';

export type HomeStageStatus =
  | 'loading'
  | 'ready'
  | 'empty'
  | 'partial'
  | 'full'
  | 'overflow'
  | 'error'
  | 'unavailable';

export type HomeStageTrend = 'up' | 'down' | 'stable' | 'unknown';

export type HomeStageSourceKind = 'mock' | 'backend' | 'derived';

export interface HomeStageProvenance {
  sourceKind: HomeStageSourceKind;
  updatedAt: string | null;
  confidence?: number | null;
}

export interface HomeContinuityItemViewModel {
  id: string;
  label: string;
  accentRole: string;
  iconKey?: string | null;
  provenance: HomeStageProvenance;
}

export type HomeSignalVisualizationKind =
  'sparkline' | 'bars' | 'dots' | 'progress' | 'range' | 'number_delta';

export interface HomeSignalVisualizationViewModel {
  kind: HomeSignalVisualizationKind;
  points: readonly number[];
  target?: number | null;
  unit?: string | null;
}

export interface HomeSignalItemViewModel {
  id: string;
  label: string;
  primaryValue: string;
  secondaryValue?: string | null;
  trend?: HomeStageTrend;
  visualization: HomeSignalVisualizationViewModel;
  provenance: HomeStageProvenance;
}

export interface HomeStageViewModel {
  contractVersion: typeof HOME_STAGE_CONTRACT_VERSION;
  mode: HomeStageMode;
  status: HomeStageStatus;
  continuity: {
    activeIndex: number | null;
    items: readonly HomeContinuityItemViewModel[];
  };
  signals: {
    activeIndex: number | null;
    items: readonly HomeSignalItemViewModel[];
  };
}

export type HomeStageIntent =
  | { type: 'MODE_PREVIOUS' }
  | { type: 'MODE_NEXT' }
  | { type: 'ITEM_PREVIOUS' }
  | { type: 'ITEM_NEXT' }
  | { type: 'ITEM_SELECT'; index: number }
  | { type: 'DRAG_START' }
  | { type: 'DRAG_MOVE'; delta: number }
  | { type: 'DRAG_END' }
  | { type: 'OPEN_MANAGEMENT'; mode: HomeStageMode };

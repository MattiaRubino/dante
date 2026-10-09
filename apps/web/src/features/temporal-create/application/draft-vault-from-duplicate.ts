import type { ActivityDuplicateSeed } from './activity-duplicate-seed';
import type { DraftVaultSnapshot } from './remote-draft-vault';
import { applyTemporalCreateFieldSeed } from './temporal-create-seed';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  type TemporalCreateU2LifeAreaDraft,
} from '../model/temporal-create-u2-authoring';

export function draftVaultSnapshotFromDuplicate(
  seed: ActivityDuplicateSeed,
  selectedArea?: TemporalCreateU2LifeAreaDraft,
): DraftVaultSnapshot {
  const fields = applyTemporalCreateFieldSeed(
    createTemporalCreateFields({ kind: seed.fields.kind ?? 'activity' }),
    seed.fields,
  );
  const original = createTemporalCreateU2AuthoringDraft(fields);
  return Object.freeze({
    version: 1 as const,
    fields,
    advanced: Object.freeze({
      ...original, ...seed.advanced,
      ...(selectedArea ? { lifeArea: selectedArea } : {}),
    }),
    surface: 'full' as const,
  });
}

export type TemporalCreateComposerPosition = Readonly<{
  top: number;
  left: number;
}>;

/**
 * Presentation-only tone shared with the Timeline visual grammar. This is not a
 * Domain classification and must not be promoted into canonical ontology.
 */
export type TemporalCreateContextTone =
  | 'focus'
  | 'meeting'
  | 'health'
  | 'creative'
  | 'personal'
  | 'urgent';

/**
 * Actor-local Life Area projection used by Quick Create.
 *
 * `revision` and `colorCode` are accepted catalog state, not UI-owned truth.
 * They let U2 issue a revision-guarded appearance mutation only when the user
 * explicitly changes the selected Life Area colour at submit time.
 */
export type TemporalCreateContextOption = Readonly<{
  id: string;
  label: string;
  tone: TemporalCreateContextTone;
  revision?: number;
  colorCode?: string | null;
  local?: boolean;
}>;

/**
 * Draft-only request for a new Life Area. It must not be materialized until
 * the whole Quick Create command is accepted.
 */
export type TemporalCreateContextInput = Readonly<{
  label: string;
  tone: TemporalCreateContextTone;
  colorCode?: string | null;
}>;

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

export type TemporalCreateContextOption = Readonly<{
  id: string;
  label: string;
  tone: TemporalCreateContextTone;
  local?: boolean;
}>;

export type TemporalCreateContextInput = Readonly<{
  label: string;
  tone: TemporalCreateContextTone;
}>;

/** Materialize unnamed agenda rows at Save, preserving their visible order. */
export function namedEventAgendaParts(parts: readonly string[]): readonly string[] {
  return parts.map((part, index) => part.trim() || `Scaletta ${index + 1}`);
}

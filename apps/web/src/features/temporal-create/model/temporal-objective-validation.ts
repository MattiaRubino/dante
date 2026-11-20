import type { TemporalCreateObjectiveDraft } from './temporal-create-u2-authoring';

export type ObjectiveInvalidField =
  | 'label'
  | 'targetValue'
  | 'targetMin'
  | 'targetMax'
  | 'unitCode'
  | 'comparatorCode';

export type ObjectiveFieldIssue = Readonly<{
  field: ObjectiveInvalidField;
  /** Empty required fields use the field border and accessible label. */
  message: string | null;
}>;

/** One rule for Create, standalone Edit, occurrence Edit and series Edit. */
export function objectiveFieldIssues(
  objective: Pick<
    TemporalCreateObjectiveDraft,
    | 'label'
    | 'resultKind'
    | 'comparatorCode'
    | 'targetValue'
    | 'targetMin'
    | 'targetMax'
    | 'unitCode'
  >,
): readonly ObjectiveFieldIssue[] {
  const issues: ObjectiveFieldIssue[] = [];
  const label = objective.label.trim();
  if (!label) issues.push({ field: 'label', message: null });
  else if (label.length > 300)
    issues.push({ field: 'label', message: 'Nome troppo lungo.' });

  const unit = objective.unitCode.trim();
  if (['quantity', 'range'].includes(objective.resultKind) && unit.length > 40)
    issues.push({ field: 'unitCode', message: 'Unità troppo lunga.' });

  const numberIssue = (
    value: string,
    field: 'targetValue' | 'targetMin' | 'targetMax',
  ): ObjectiveFieldIssue | null =>
    !value.trim()
      ? { field, message: null }
      : !Number.isFinite(Number(value))
        ? { field, message: 'Inserisci un numero.' }
        : null;

  if (objective.resultKind === 'quantity') {
    const issue = numberIssue(objective.targetValue, 'targetValue');
    if (issue) issues.push(issue);
    if (!['eq', 'gte', 'lte'].includes(objective.comparatorCode ?? ''))
      issues.push({ field: 'comparatorCode', message: 'Scegli una regola.' });
  }

  if (objective.resultKind === 'range') {
    const minimumIssue = numberIssue(objective.targetMin, 'targetMin');
    if (minimumIssue) issues.push(minimumIssue);
    const maximumIssue = numberIssue(objective.targetMax, 'targetMax');
    if (maximumIssue) issues.push(maximumIssue);
    if (!minimumIssue && !maximumIssue &&
      Number(objective.targetMax) <= Number(objective.targetMin))
      issues.push({ field: 'targetMax', message: 'Max deve superare Min.' });
  }
  return issues;
}

export function objectiveFieldIssue(
  objective: Parameters<typeof objectiveFieldIssues>[0],
): ObjectiveFieldIssue | null {
  return objectiveFieldIssues(objective)[0] ?? null;
}

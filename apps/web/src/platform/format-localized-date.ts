/** Capitalize the month token in a localized date without changing the other parts. */
export function formatDateWithCapitalizedMonth(
  formatter: Intl.DateTimeFormat,
  date: Date,
): string {
  const locale = formatter.resolvedOptions().locale;
  return formatter
    .formatToParts(date)
    .map((part) =>
      part.type === 'month'
        ? part.value.replace(/\p{L}/u, (letter) =>
            letter.toLocaleUpperCase(locale),
          )
        : part.value,
    )
    .join('');
}

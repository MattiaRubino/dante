import { expect, type Locator } from '@playwright/test';

/** Exercise the visible start/end controls: Duration select was retired. */
export async function setTimedDuration(
  dialog: Locator,
  minutes: number,
): Promise<void> {
  const startHour = dialog.getByRole('textbox', { name: 'Inizio: ore' });
  const startMinute = dialog.getByRole('textbox', { name: 'Inizio: minuti' });
  const start =
    Number(await startHour.inputValue()) * 60 +
    Number(await startMinute.inputValue());
  if (
    !Number.isFinite(start) ||
    start < 0 ||
    start >= 1440 ||
    !Number.isInteger(minutes) ||
    minutes <= 0 ||
    start + minutes >= 1440
  ) {
    throw new Error(
      'This browser duration helper expects an intraday interval',
    );
  }
  const end = start + minutes;
  const hours = String(Math.floor(end / 60)).padStart(2, '0');
  const mins = String(end % 60).padStart(2, '0');
  await dialog.getByRole('textbox', { name: 'Fine: ore' }).fill(hours);
  await dialog.getByRole('textbox', { name: 'Fine: minuti' }).fill(mins);
  await expect(dialog.getByRole('textbox', { name: 'Fine: ore' })).toHaveValue(
    hours,
  );
  await expect(
    dialog.getByRole('textbox', { name: 'Fine: minuti' }),
  ).toHaveValue(mins);
}

export async function timedDurationMinutes(dialog: Locator): Promise<number> {
  const startHour = Number(
    await dialog.getByRole('textbox', { name: 'Inizio: ore' }).inputValue(),
  );
  const startMinute = Number(
    await dialog.getByRole('textbox', { name: 'Inizio: minuti' }).inputValue(),
  );
  const endHour = Number(
    await dialog.getByRole('textbox', { name: 'Fine: ore' }).inputValue(),
  );
  const endMinute = Number(
    await dialog.getByRole('textbox', { name: 'Fine: minuti' }).inputValue(),
  );
  return endHour * 60 + endMinute - (startHour * 60 + startMinute);
}

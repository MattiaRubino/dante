import { Temporal } from '@dante/time';
import { useEffect, useState } from 'react';

function millisecondsToNextMinute(now: Temporal.ZonedDateTime): number {
  const elapsed =
    now.second * 1_000 + now.millisecond + now.microsecond / 1_000;
  return Math.max(50, 60_000 - elapsed + 20);
}

export function useMinuteClock(timeZone: string): Temporal.ZonedDateTime {
  const [now, setNow] = useState(() => Temporal.Now.zonedDateTimeISO(timeZone));

  useEffect(() => {
    let timeoutId: number | undefined;
    let active = true;

    const schedule = () => {
      const current = Temporal.Now.zonedDateTimeISO(timeZone);
      timeoutId = window.setTimeout(() => {
        if (!active) {
          return;
        }
        setNow(Temporal.Now.zonedDateTimeISO(timeZone));
        schedule();
      }, millisecondsToNextMinute(current));
    };

    const syncAfterVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        setNow(Temporal.Now.zonedDateTimeISO(timeZone));
        if (timeoutId !== undefined) {
          window.clearTimeout(timeoutId);
        }
        schedule();
      }
    };

    schedule();
    document.addEventListener('visibilitychange', syncAfterVisibilityChange);

    return () => {
      active = false;
      document.removeEventListener(
        'visibilitychange',
        syncAfterVisibilityChange,
      );
      if (timeoutId !== undefined) {
        window.clearTimeout(timeoutId);
      }
    };
  }, [timeZone]);

  return now;
}

import { useCallback, useState } from 'react';

/** A blank title is an attempted-submit error, never an eager form error.
 * Keep the control actionable so the user can request validation feedback.
 * One counter alternates two equivalent CSS animations for repeated attempts.
 */
export function useTemporalRequiredTitle(value: string) {
  const [submittedBlank, setSubmittedBlank] = useState(false);
  const [shakeAttempt, setShakeAttempt] = useState(0);
  const invalid = submittedBlank && value.trim().length === 0;

  const validate = useCallback(() => {
    if (value.trim().length > 0) return true;
    setSubmittedBlank(true);
    setShakeAttempt((current) => current + 1);
    return false;
  }, [value]);

  const changed = useCallback((next: string) => {
    if (next.trim().length > 0) setSubmittedBlank(false);
  }, []);

  return { invalid, shakeAttempt, validate, changed };
}

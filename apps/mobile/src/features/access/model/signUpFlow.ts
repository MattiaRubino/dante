export type SignUpStep = 'email' | 'password' | 'verify';

export type SignUpFlowState = Readonly<{
  step: SignUpStep;
  email: string;
}>;

export type SignUpFlowEvent =
  | { type: 'EDIT_EMAIL'; email: string }
  | { type: 'SIGN_UP_EMAIL_ACCEPTED'; email: string }
  | { type: 'CHANGE_SIGN_UP_EMAIL' }
  | { type: 'SERVER_SIGN_UP_CREATED' };

export type SignUpEmailError = 'email';
export type SignUpPasswordError = 'passwordMinimum';
export type SignUpVerificationError = 'verificationCode';

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
export const SIGN_UP_PASSWORD_MIN_LENGTH = 15;
export const VERIFICATION_CODE_LENGTH = 6;

export const initialSignUpFlowState: SignUpFlowState = {
  step: 'email',
  email: '',
};

export function normalizeSignUpEmail(value: string) {
  return value.trim();
}

export function validateSignUpEmail(value: string): SignUpEmailError | null {
  return EMAIL_PATTERN.test(normalizeSignUpEmail(value)) ? null : 'email';
}

export function validateSignUpPassword(
  value: string,
): SignUpPasswordError | null {
  return Array.from(value).length >= SIGN_UP_PASSWORD_MIN_LENGTH
    ? null
    : 'passwordMinimum';
}

export function normalizeVerificationCode(value: string) {
  return value.replace(/\D/g, '').slice(0, VERIFICATION_CODE_LENGTH);
}

export function validateVerificationCode(
  value: string,
): SignUpVerificationError | null {
  return new RegExp(`^\\d{${VERIFICATION_CODE_LENGTH}}$`).test(value)
    ? null
    : 'verificationCode';
}

export function signUpFlowReducer(
  state: SignUpFlowState,
  event: SignUpFlowEvent,
): SignUpFlowState {
  switch (event.type) {
    case 'EDIT_EMAIL':
      return { ...state, email: event.email };
    case 'SIGN_UP_EMAIL_ACCEPTED':
      return { step: 'password', email: event.email };
    case 'CHANGE_SIGN_UP_EMAIL':
      return { step: 'email', email: state.email };
    case 'SERVER_SIGN_UP_CREATED':
      return state.step === 'password'
        ? { step: 'verify', email: state.email }
        : state;
  }
}

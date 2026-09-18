export type SignInEmailError = 'email';
export type SignInPasswordError = 'passwordRequired';

export type SignInFormErrors = Readonly<{
  email: SignInEmailError | null;
  password: SignInPasswordError | null;
}>;

export type SignInCredentials = Readonly<{
  email: string;
  password: string;
}>;

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const EMPTY_SIGN_IN_FORM_ERRORS: SignInFormErrors = {
  email: null,
  password: null,
};

export function normalizeSignInEmail(value: string) {
  return value.trim();
}

export function validateSignInEmail(value: string): SignInEmailError | null {
  const normalized = normalizeSignInEmail(value);
  return EMAIL_PATTERN.test(normalized) ? null : 'email';
}

export function validateSignInPassword(
  value: string,
): SignInPasswordError | null {
  return value.length > 0 ? null : 'passwordRequired';
}

export function validateSignInForm(
  email: string,
  password: string,
): SignInFormErrors {
  return {
    email: validateSignInEmail(email),
    password: validateSignInPassword(password),
  };
}

export function hasSignInFormErrors(errors: SignInFormErrors) {
  return errors.email !== null || errors.password !== null;
}

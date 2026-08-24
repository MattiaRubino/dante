import type { access as itAccess } from '../it/access';

type AccessResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: AccessResource<T[K]> };

export const access = {
  stage: {
    titleFirst: 'Understand life.',
    titleSecond: 'Shape what comes next.',
    body: 'A personal space to understand what is happening, preserve continuity over time, and decide what comes next.',
    foot: 'One reality. More than one way to understand it.',
  },
  kicker: {
    access: 'Access',
  },
  signin: {
    title: 'Sign in to DANTE',
    body: 'Continue with your account or use email and password.',
    forgot: 'Forgot password?',
    new: 'New to DANTE?',
  },
  provider: {
    google: 'Continue with Google',
    apple: 'Continue with Apple',
  },
  common: {
    or: 'or',
  },
  field: {
    email: 'Email',
    password: 'Password',
  },
  action: {
    signin: 'Sign in',
    createAccount: 'Create account',
  },
  legal: {
    prefix: 'By continuing, you agree to the',
    terms: 'Terms',
    privacy: 'Privacy',
  },
} as const satisfies AccessResource<typeof itAccess>;

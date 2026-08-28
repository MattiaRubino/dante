import { describe, expect, it } from 'vitest';

import { authGetSession, authLogOut, authSignIn } from '../src/index';

describe('@dante/api-client generated Auth surface', () => {
  it('exports the three M3 application-intent operations', () => {
    expect(authSignIn).toBeTypeOf('function');
    expect(authGetSession).toBeTypeOf('function');
    expect(authLogOut).toBeTypeOf('function');
  });
});

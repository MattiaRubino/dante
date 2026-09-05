import part00 from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part00?raw';
import part01 from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part01?raw';
import part02 from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part02?raw';
import part03a from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part03a?raw';
import part03b from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part03b?raw';
import part04a from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part04a?raw';
import part04b from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part04b?raw';
import part05a from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part05a?raw';
import part05b from './cosmos/dante-home-cosmos-mirrored-v1.webp.b64.part05b?raw';

const HOME_COSMOS_BASE64 = [
  part00,
  part01,
  part02,
  part03a,
  part03b,
  part04a,
  part04b,
  part05a,
  part05b,
]
  .map((part) => part.replace(/\s+/g, ''))
  .join('');

export const HOME_COSMOS_DATA_URL = `data:image/webp;base64,${HOME_COSMOS_BASE64}`;

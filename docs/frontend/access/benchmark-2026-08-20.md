# DANTE Access — benchmark and authority notes — 2026-08-20

Status: **RESEARCH / DESIGN EVIDENCE**. Competitor examples inform structure; they do not become DANTE requirements by default.

## Official/provider/security authorities

### Google Identity Services

Official guidance: <https://developers.google.com/identity/gsi/web/guides/display-button>

Use the official Google Identity Services rendering/integration path in production rather than drawing a substitute `G` or inventing provider-owned chooser/consent UI.

### Sign in with Apple

Official resources: <https://developer.apple.com/design/resources/> and Sign in with Apple web documentation under Apple Developer.

Production uses Apple's current approved component/assets and rules rather than a CSS recreation of the Apple mark.

### NIST SP 800-63B

Current digital-identity authentication guidance: <https://pages.nist.gov/800-63-4/sp800-63b.html>

Relevant review principles include long-password support, password-manager compatibility, paste support and avoiding arbitrary composition-rule checklists. A3.4's `15+` display is a reviewed prototype choice, not a backend contract.

### OWASP Authentication / Forgot Password guidance

- <https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html>
- <https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html>

Relevant principles: avoid revealing account existence through recovery/registration behavior; treat recovery links/tokens as security-sensitive backend concerns.

## Mature-product pattern observations

The A3/A3.1 redesign compared current entry/auth patterns from mature products including ChatGPT/OpenAI, Notion, Linear, Slack and Figma. The useful common pattern was not their visual skin; it was disciplined hierarchy:

- low-noise entry;
- clear provider options;
- email-first or staged credential flow where useful;
- short explicit verification states;
- lightweight first-run progression rather than one large questionnaire;
- language/account-recovery states that look like part of the same product.

DANTE intentionally does not clone any one product. A3.4 combines those structural lessons with DANTE's own brand and product boundaries.

## DANTE-specific conclusions

- one coherent Access system, not isolated login/signup mockups;
- provider sign-in and provider integration permissions stay separate;
- account creation stays fast;
- profile enrichment is progressive;
- first-run guides toward one useful first action/import/demo/skip;
- locked DANTE vector assets are used directly;
- the selected A3.4 corner mark adds brand presence without turning the screen into a marketing landing page.

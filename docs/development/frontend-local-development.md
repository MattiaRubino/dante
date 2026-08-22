# Frontend Local Development and Workstation Runbook

- Status: **CURRENT FOR `feature/frontend-materialization`**
- Purpose: reproducible frontend workstation setup, installation guidance and LOCAL topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Current execution state: **FM-05A SHARED DESIGN TOKENS PASS**

## 1. Core posture

DANTE uses one authoritative Git repository/history with working directories under WSL/Linux semantics. Purpose-specific linked Git worktrees inside WSL are allowed when backend/frontend or other bounded workstreams run concurrently.

```text
Windows 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / emulator
└── Docker Desktop

WSL2 / Linux
├── linked DANTE Git worktree(s)
├── Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
├── Python / uv where applicable
└── Docker CLI
```

Docker is used for real stateful/local infrastructure, not as a blanket wrapper around every development process.

Normal LOCAL ownership:

```text
Git worktrees            WSL filesystem
Node/pnpm/Turbo          WSL
Vite                     WSL
Metro/Expo CLI           WSL
PyCharm/JetBrains UI     Windows using WSL project/tooling
browser                  Windows
Android Studio/emulator  Windows
Docker daemon            Docker Desktop / WSL integration
PostgreSQL               Docker when backend LOCAL infra is active
```

## 2. Filesystem and worktree invariant

Preferred paths live inside the Linux filesystem, for example:

```text
/home/<user>/projects/dante
/home/<user>/projects/dante-frontend
```

Observed current topology:

```text
/home/mattia/projects/dante
feature/backend-scaffold

/home/mattia/projects/dante-frontend
feature/frontend-materialization
```

Avoid a Windows-backed authoritative path such as `/mnt/c/...` unless concrete evidence forces a different choice.

Hard rules:

```text
one authoritative Git repository/history
linked purpose-specific worktrees inside WSL are allowed
no divergent independent Windows + WSL clones for active development
no shared cross-OS node_modules
no manual file copying between Windows and WSL source trees
```

## 3. Python analogy for frontend dependency management

| Backend/Python | Frontend/TypeScript |
| --- | --- |
| Python runtime | Node runtime |
| `uv` | `pnpm` |
| `pyproject.toml` | `package.json` |
| `uv.lock` | `pnpm-lock.yaml` |
| `.venv` | project dependency graph exposed through `node_modules` |
| `uv sync` | `pnpm install` |

The analogy is useful but not exact. A Python virtual environment carries an isolated interpreter environment. Frontend `node_modules` governs project dependencies while Node itself is a WSL runtime whose required version is declared by the repository.

The repository governs both:

```text
runtime expectation
Node exact accepted patch

project dependency graph
package.json + pnpm-lock.yaml
```

## 4. Machine-level versus repository-managed tooling

Machine/WSL level:

- Git;
- Node runtime/version manager;
- pnpm activation mechanism;
- Docker CLI integration;
- Android platform tooling on Windows.

Repository-managed dependencies now include:

```text
Root engineering
TypeScript                    6.0.3
Turborepo                     2.10.11
ESLint                        10.8.1
@eslint/js                    10.0.1
typescript-eslint             8.67.0
Prettier                      3.9.0

Minimal Web
React                         19.2.8
React DOM                     19.2.8
Vite                          8.2.1
@vitejs/plugin-react          6.1.0
@tanstack/react-router        1.170.31
@tanstack/router-plugin       1.168.34
@types/node                   24.13.3
@types/react                  19.2.18
@types/react-dom              19.2.4

Minimal Mobile
Expo                          57.0.9
React Native                  0.86.2
React                         19.2.3
Expo Router                   57.0.9
Gesture Handler               2.32.0
Reanimated                    4.5.1
Safe Area Context             5.7.0
Screens                       4.26.2
Worklets                      0.10.1

Shared design tokens
@terrazzo/cli                 2.7.1
@terrazzo/parser              2.7.1
@terrazzo/plugin-css          2.7.1
```

Future repository-managed dependencies include, when materialized:

- additional TanStack libraries;
- Zod;
- test tooling;
- generation tooling;
- PowerSync/native SQLite integrations when their scope activates.

Project libraries are not installed globally for convenience.

Avoid:

```text
npm install -g vite
npm install -g typescript
npm install -g expo
sudo npm ...
```

unless a future tool explicitly requires a documented global exception.

## 5. Current version governance

Current materialized pins:

```text
Node                        24.19.0
pnpm                        11.22.0
TypeScript                  6.0.3
Turborepo                   2.10.11
ESLint                      10.8.1
@eslint/js                  10.0.1
typescript-eslint           8.67.0
Prettier                    3.9.0
React                       19.2.8
React DOM                   19.2.8
Vite                        8.2.1
@vitejs/plugin-react        6.1.0
@tanstack/react-router      1.170.31
@tanstack/router-plugin     1.168.34
@types/node                 24.13.3
@types/react                19.2.18
@types/react-dom            19.2.4
Expo                       57.0.9
React Native                0.86.2
Mobile React                19.2.3
Expo Router                 57.0.9
Gesture Handler             2.32.0
Reanimated                  4.5.1
Safe Area Context           5.7.0
Screens                     4.26.2
Worklets                    0.10.1
@terrazzo/cli                2.7.1
@terrazzo/parser             2.7.1
@terrazzo/plugin-css         2.7.1
```

Current root authorities:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
turbo.json
tsconfig.base.json
eslint.config.mjs
prettier.config.mjs
.prettierignore
```

Current Web authorities:

```text
apps/web/package.json
apps/web/index.html
apps/web/tsconfig.json
apps/web/vite.config.ts
apps/web/src/main.tsx
apps/web/src/routes/__root.tsx
apps/web/src/routes/index.tsx
apps/web/src/styles.css
apps/web/src/routeTree.gen.ts
```

Current Mobile authorities:

```text
apps/mobile/package.json
apps/mobile/app.config.ts
apps/mobile/tsconfig.json
apps/mobile/app/_layout.tsx
apps/mobile/app/index.tsx
apps/mobile/.gitignore
```

Current shared design-token authorities:

```text
packages/design-tokens/package.json
packages/design-tokens/tsconfig.json
packages/design-tokens/terrazzo.config.ts
packages/design-tokens/tokens/primitives.json
packages/design-tokens/tokens/semantic.json
packages/design-tokens/tooling/native-plugin.ts
packages/design-tokens/generated/web.css
packages/design-tokens/generated/native.ts
```

`tokens/*.json` is semantic source authority. `generated/*` is deterministic committed output and must not be hand edited.

`package.json` declares Node `24.19.0`, pnpm `11.22.0`, exact root engineering devDependency pins, and the standard root scripts. `.node-version` declares Node `24.19.0`. `apps/web/package.json` and `apps/mobile/package.json` declare their exact application dependency baselines. `packages/design-tokens/package.json` declares the first genuine shared workspace package and its Terrazzo `2.7.1` toolchain. The shared lockfile is committed and was generated by pnpm from the real WSL installation.

Do not perform broad blind upgrades such as `pnpm update --latest` on the production workspace without an explicit dependency-upgrade scope and validation.

Native-sensitive upgrades such as Expo, React Native, PowerSync or OP-SQLite require compatibility-aware validation.

## 6. Docker boundary

Use Docker where it provides reproducible service/infrastructure semantics.

Expected examples when activated:

```text
PostgreSQL
PowerSync service
other real stateful LOCAL dependencies
```

Normal frontend dev servers stay direct in WSL:

```text
Vite
Metro / Expo CLI
```

Docker container lifecycle and persistent data lifecycle are separate. Stateful services use explicit persistent volumes/storage where required.

## 7. Browser and Mobile networking

### Web — directly validated

Observed LOCAL path:

```text
Vite 8.2.1 in WSL
http://localhost:5173/
↓
Windows localhost forwarding
↓
Firefox on Windows
↓
DANTE Web diagnostic route /
```

This path is **PASS** on the observed Windows 11 + WSL2 workstation.

The accepted normal command is:

```bash
pnpm --filter @dante/web dev
```

Observed Vite output:

```text
VITE v8.2.1
Local: http://localhost:5173/
```

No `--host` flag, manual proxy, Windows Node process, alternate clone, or custom network bridge was required for the observed workstation. Do not add one pre-emptively; troubleshoot only if a future environment produces contrary evidence.

### Mobile — directly validated

Observed LOCAL Android path:

```text
Metro / Expo CLI in WSL
exp://127.0.0.1:8081
↓
Windows ADB platform-tools invoked through WSL interoperability
adb reverse tcp:8081 tcp:8081
↓
Windows Android emulator
Expo Go 57.0.9
↓
DANTE Mobile diagnostic route /
```

This path is **PASS** on the observed Windows 11 + WSL2 workstation.

Start Metro from WSL:

```bash
cd ~/projects/dante-frontend/apps/mobile
pnpm exec expo start --localhost
```

With the Windows emulator running, establish the bounded ADB reverse adapter from WSL:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'
```

Useful verification:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse --list'
```

Then launch the local Expo URL when needed:

```bash
powershell.exe -NoProfile -Command '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" shell am start -a android.intent.action.VIEW -d "exp://127.0.0.1:8081"'
```

Do not introduce `--host` changes, tunnels, Metro overrides, hoisting, Windows Node, a second clone or project `updates.url` merely because the emulator cannot initially render. Diagnose the chain in order: ADB device → reverse mapping → Metro → manifest → bundle → Expo Go/client runtime.

For the directly observed FM-04 run, the Android manifest returned HTTP 200, the Hermes bundle returned HTTP 200 with 9,162,793 bytes, Expo Go reported Metro reachable and loaded the JS bundle, and DANTE rendered successfully.

### FM-05A Metro workspace-package resolution

The first real shared-package Mobile import exposed one bounded resolution failure:

```text
@dante/design-tokens/native could not be found within the project
```

Before changing configuration, verify the chain:

```bash
cd ~/projects/dante-frontend/apps/mobile

ls -l node_modules/@dante/design-tokens

node --input-type=module -e   "console.log(import.meta.resolve('@dante/design-tokens/native'))"

cat node_modules/@dante/design-tokens/package.json
```

The accepted FM-05A evidence was:

```text
workspace symlink exists
Node resolves @dante/design-tokens/native
resolved file = packages/design-tokens/generated/native.ts
```

Expo/Metro default-config inspection also proved that the observed SDK 57 configuration already included the workspace package in `watchFolders`, included app/root `node_modules`, enabled package exports and included TypeScript source extensions.

Do **not** respond to this symptom by immediately adding a custom `metro.config.js`, hoisting pnpm dependencies, changing `nodeLinker`, installing unrelated Metro packages or switching runtime ownership.

A `--clear` Metro restart did not repair the observed failure.

The decisive diagnostic probe temporarily replaced the bare import with:

```text
../../../packages/design-tokens/generated/native
```

That relative path rendered DANTE Mobile, proving Metro could see and execute the external generated TypeScript file. The temporary probe must then be restored; it is diagnostic evidence, not an accepted production import.

The durable package public surface is:

```json
{
  ".": {
    "react-native": "./generated/native.ts",
    "default": "./generated/native.ts"
  },
  "./native": "./generated/native.ts",
  "./web.css": "./generated/web.css"
}
```

After restoring:

```ts
import { radii } from '@dante/design-tokens/native';
```

the Android runtime rendered successfully. No Metro override or pnpm linker fallback is part of the accepted configuration.

After a workstation reboot, the proven LOCAL sequence remains:

```text
1. start Windows Android emulator
2. WSL: cd ~/projects/dante-frontend/apps/mobile
3. WSL: pnpm exec expo start --localhost
4. second WSL terminal: verify adb device
5. second WSL terminal: adb reverse tcp:8081 tcp:8081
6. open exp://127.0.0.1:8081 in Expo Go
```

Windows ADB commands from WSL:

```bash
powershell.exe -NoProfile -Command   '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" devices'

powershell.exe -NoProfile -Command   '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" reverse tcp:8081 tcp:8081'

powershell.exe -NoProfile -Command   '& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" shell am start -a android.intent.action.VIEW -d "exp://127.0.0.1:8081"'
```

During the successful FM-05A run, Expo Go briefly displayed `Cannot connect to Expo CLI` after the bundle had already loaded. Dismissing the warning exposed the successfully rendered DANTE Mobile application. Treat such a warning as client/dev-tooling noise only when the application runtime is independently proven; do not use it to justify product configuration changes.

## 8. Command policy

Repository scripts are the normal root entry point for materialized tooling:

```text
pnpm install
pnpm dev
pnpm lint
pnpm lint:fix
pnpm format
pnpm format:check
pnpm typecheck
pnpm test
pnpm build
```

The workspace now contains real Web, Mobile and shared design-token consumers. Root Turbo `typecheck` directly executes `@dante/design-tokens`, `@dante/web` and `@dante/mobile`; root Turbo `build` directly executes token generation before the Web production build. This is the first directly proven multi-workspace graph.

Useful direct app commands when isolating a runtime:

```bash
pnpm --filter @dante/web dev
cd apps/mobile && pnpm exec expo start --localhost
```

Prefer project-local execution through pnpm rather than unrelated global binaries.

## 9. FM-00 observed preflight — PASS

Observed on 2026-08-21:

```text
frontend worktree
/home/mattia/projects/dante-frontend
feature/frontend-materialization

WSL
Ubuntu 24.04.4 LTS
Linux / WSL2

Git
2.43.0
/usr/bin/git

Docker
29.7.2
/usr/bin/docker
Docker Compose 5.4.0
```

The preflight found no Linux Node/npm/pnpm/Corepack installation. Windows paths are present in WSL interoperability PATH, so every frontend runtime executable must be checked to resolve Linux-side.

## 10. FM-01 installation path — PASS

### Machine prerequisites observed

For the chosen installation path:

```bash
sudo apt-get install -y unzip libatomic1
```

`unzip` is required by the fnm installation path used here.

`libatomic1` was required by the pnpm standalone Linux executable on this Ubuntu 24.04 WSL installation. The missing library manifested as:

```text
error while loading shared libraries: libatomic.so.1
```

The repair is to install `libatomic1`, verify it through `ldconfig`, then rerun the pinned pnpm installer. Do not switch package-manager strategy merely because this prerequisite is missing.

### Node version manager

Observed:

```text
fnm 1.39.0
```

Bash integration:

```bash
FNM_PATH="$HOME/.local/share/fnm"
if [ -d "$FNM_PATH" ]; then
  export PATH="$FNM_PATH:$PATH"
  eval "$(fnm env --use-on-cd --shell bash)"
fi
```

The repository `.node-version` is authoritative for the current Node patch:

```text
24.19.0
```

### pnpm

Observed standalone installation:

```text
PNPM_HOME=/home/mattia/.local/share/pnpm
pnpm 11.22.0
```

Observed shell setup:

```bash
export PNPM_HOME="/home/mattia/.local/share/pnpm"
case ":$PATH:" in
  *":$PNPM_HOME/bin:"*) ;;
  *) export PATH="$PNPM_HOME/bin:$PATH" ;;
esac
```

## 11. Runtime direct checks — PASS

Observed normal shell:

```text
fnm        1.39.0
Node       24.19.0
npm        11.17.0
pnpm       11.22.0
```

Observed executable ownership:

```text
node       Linux-side fnm multishell path
npm        Linux-side fnm multishell path
pnpm       /home/mattia/.local/share/pnpm/bin/pnpm
```

An isolated login-shell test with a minimal inherited environment directly proved:

```text
node=v24.19.0
npm=11.17.0
pnpm=11.22.0
fnm=fnm 1.39.0
fnm-current=v24.19.0
```

No `/mnt/c/...` runtime executable leakage was observed.

## 12. FM-02A root workspace — PASS

Current root workspace files:

```text
.node-version
package.json
pnpm-workspace.yaml
pnpm-lock.yaml
```

Workspace reservation:

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
```

No empty `apps/` or `packages/` directory is created merely to match the architecture diagram.

Direct checks at FM-02A:

```text
pnpm install                       PASS
pnpm install --frozen-lockfile     PASS
lockfile generation                PASS
unexpected apps/                   0
unexpected packages/               0
unexpected node_modules/           0 in empty-workspace baseline
```

Remote baseline commit:

```text
c3f7945da7137b2bdd9e9f8922af452f1a79770f
build: establish frontend workspace runtime baseline
```

## 13. FM-02B root engineering tooling — PASS

Materialized root files:

```text
turbo.json
tsconfig.base.json
eslint.config.mjs
prettier.config.mjs
.prettierignore
```

Exact installed versions:

```text
TypeScript          6.0.3
Turborepo           2.10.11
ESLint              10.8.1
@eslint/js          10.0.1
typescript-eslint   8.67.0
Prettier            3.9.0
```

Direct WSL validation:

```text
pnpm install                                  PASS
pnpm exec tsc --version                       6.0.3
pnpm exec turbo --version                     2.10.11
pnpm exec eslint --version                    10.8.1
pnpm exec prettier --version                  3.9.0
pnpm lint                                     PASS
pnpm format:check                             PASS
TypeScript base-config temporary probe        PASS
Turbo configuration dry-run                   PASS
pnpm install --frozen-lockfile                PASS
```

### TypeScript base-config validation

`tsconfig.base.json` intentionally has no repository source inputs. Do not treat a direct root invocation that reports no inputs as a broken configuration.

The accepted direct probe is a temporary project that extends the repository base config and includes a trivial `.ts` source. The observed probe compiled successfully and was removed afterwards. No test artifact is committed.

Cross-workspace strict typechecking remains `NOT RUN` until multiple real app/package consumers exist.

### ESLint scope

The root flat config is installed and `pnpm lint` directly passes on the repository. Typed TypeScript configuration is active for real `.ts/.tsx` consumers.

This is not yet a PASS for architecture/import/boundary/cycle enforcement; those checks activate and are directly tested when the relevant real boundaries exist.

### Prettier scope

The first FM-02B `pnpm format:check` identified quote-style drift in `pnpm-workspace.yaml`. The file was repaired to repository style and a subsequent `pnpm format:check` passed.

Do not hide format failures through blanket ignores merely to obtain a green check.

### Lockfile authority

The root engineering dependency graph was generated by pnpm `11.22.0` on the WSL environment and committed at:

```text
7ad88e2fbba1e8140149be05f9a3fe3005ad0488
build: lock frontend engineering toolchain
```

## 14. FM-03 minimal Web application — PASS

### Materialized Web scaffold

```text
apps/web/package.json
apps/web/index.html
apps/web/tsconfig.json
apps/web/vite.config.ts
apps/web/src/main.tsx
apps/web/src/routes/__root.tsx
apps/web/src/routes/index.tsx
apps/web/src/styles.css
apps/web/src/routeTree.gen.ts
```

This is a diagnostic production scaffold only. It intentionally does not implement Access, Home, application state, network APIs or authentication contracts.

Exact Web versions:

```text
React                     19.2.8
React DOM                 19.2.8
Vite                      8.2.1
@vitejs/plugin-react      6.1.0
@tanstack/react-router    1.170.31
@tanstack/router-plugin   1.168.34
@types/node               24.13.3
@types/react              19.2.18
@types/react-dom          19.2.4
```

### Generated route tree

TanStack Router generates:

```text
apps/web/src/routeTree.gen.ts
```

Policy:

```text
generated by the real TanStack Router toolchain
committed as deterministic runtime source
never hand-edit
excluded from normal ESLint/Prettier ownership
regenerate from route source when routes change
```

The current generated tree contains only the expected `/` route under `__root__`.

### Direct Web validation

Observed WSL checks:

```text
pnpm install                                  PASS
pnpm build                                    PASS
pnpm typecheck                                PASS
pnpm lint                                     PASS
pnpm format:check                             PASS
pnpm install --frozen-lockfile                PASS
routeTree.gen.ts generation                   PASS
```

Observed build:

```text
Turbo                  2.10.11
workspace              @dante/web
Vite                   8.2.1
modules transformed    106
production build       PASS
```

Observed TypeScript task:

```text
@dante/web:typecheck
tsc --noEmit -p tsconfig.json
PASS
```

The Web app therefore proves a real Vite production build and Web TypeScript baseline. It does not yet prove a future multi-package TypeScript graph.

### Formatting repair evidence

The initial Web `pnpm format:check` exposed a formatting mismatch in `apps/web/src/styles.css`. It was not suppressed or ignored.

After multiple bounded correction attempts, the exact output from the installed Prettier `3.9.0` binary was inspected read-only on WSL and applied. The final command returned:

```text
All matched files use Prettier code style!
```

The durable rule is simple: when formatter output is uncertain, use the repository-pinned formatter as authority rather than manually guessing its canonical output.

### Browser reachability — FM-V09 PASS

Normal development command:

```bash
pnpm --filter @dante/web dev
```

Observed:

```text
VITE v8.2.1
Local: http://localhost:5173/
```

A Windows Firefox browser opened `http://localhost:5173/` successfully while Vite ran in WSL and rendered:

```text
DANTE Web
Frontend runtime ready
Route: /
Purpose: FM-03 diagnostic scaffold
```

No special network flag or workaround was required.

### FM-03 generated closure

The Web lockfile delta and generated route tree were committed from the real WSL environment at:

```text
1568d90091064162da9a438f3555675f1921c226
build: lock minimal web runtime
```

Exact commit scope:

```text
CREATE
apps/web/src/routeTree.gen.ts

UPDATE
pnpm-lock.yaml

DELETE       0
UNEXPECTED   0
```

Remote lockfile readback confirms all exact Web specifiers and resolutions.

## 15. FM-04 minimal Mobile application — PASS

The minimal Mobile scaffold is directly validated on the current workstation.

Exact compatibility baseline:

```text
Expo                         57.0.9
React Native                 0.86.2
React                        19.2.3
Expo Router                  57.0.9
React Native Gesture Handler 2.32.0
React Native Reanimated      4.5.1
React Native Safe Area       5.7.0
React Native Screens         4.26.2
React Native Worklets        0.10.1
```

Direct validation:

```text
pnpm install --frozen-lockfile     PASS
expo install --check               PASS
expo-doctor                        21/21 PASS
mobile typecheck                   PASS
mobile lint                        PASS
Web typecheck/build regression     PASS
root lint/format                   PASS
Android emulator + ADB reverse     PASS
Metro manifest                     HTTP 200
Android Hermes bundle              HTTP 200 / 9,162,793 bytes
Expo Go 57.0.9                     PASS
DANTE route / render               PASS
Gesture Handler/Reanimated probe   PASS
```

Validated implementation commit:

```text
3c150c4806191f0347b64c645d53168123ce0ede
build: lock minimal mobile runtime
```

Two diagnostic observations are intentionally retained:

- Expo Go emitted internal `expo-updates` / app-loader warnings during bootstrap, but continued through `isMetroRunning() = true`, JS bundle loading, `Running "main"` for DANTE and successful render. Do not mutate DANTE update configuration solely to silence those client logs.
- The optional React Native DevTools helper in WSL reported missing `libnspr4.so`, while Metro and the application runtime continued successfully. Treat that as a DevTools/workstation concern only if DevTools functionality is actually required.

Expo Go is a diagnostic convenience for this scope, not the future production delivery/runtime contract.

## 16. FM-05A shared design tokens — PASS

`@dante/design-tokens` is the first real shared package consumed by both frontend applications.

Repository shape:

```text
packages/design-tokens/
├── package.json
├── tsconfig.json
├── terrazzo.config.ts
├── tokens/
│   ├── primitives.json
│   └── semantic.json
├── tooling/
│   └── native-plugin.ts
└── generated/
    ├── web.css
    └── native.ts
```

Toolchain:

```text
DTCG source model            2025.10
@terrazzo/cli                2.7.1
@terrazzo/parser             2.7.1
@terrazzo/plugin-css         2.7.1
```

Normal validation/regeneration commands:

```bash
pnpm --filter @dante/design-tokens tokens:lint
pnpm --filter @dante/design-tokens generate
pnpm typecheck
pnpm lint
pnpm format:check
pnpm build
```

Generated-source rule:

```text
tokens/*.json
    ↓ semantic authority
Terrazzo
    ↓ deterministic generation
generated/web.css
generated/native.ts
    ↓ committed runtime source
Web + Mobile
```

The initial package deliberately shares only already-real duplicated radii. It does not declare the diagnostic colors or typography to be canonical DANTE brand/design semantics.

Direct consumers:

```text
Web
@dante/design-tokens/web.css
→ CSS custom properties
→ diagnostic Web render PASS

Mobile
@dante/design-tokens/native
→ generated radii
→ Android diagnostic render PASS
```

Static closure:

```text
frozen install                         PASS
Terrazzo lint                          PASS
deterministic regeneration             PASS
package exports                        PASS
workspace:* Web dependency             PASS
workspace:* Mobile dependency          PASS
3-package strict typecheck             PASS
root lint / format                     PASS
Turbo multi-workspace graph            PASS
Web production build                   PASS
authorized implementation paths        15
unexpected implementation paths        0
```

Runtime closure:

```text
Windows Firefox ← WSL Vite             PASS
Windows Android ← WSL Metro            PASS
generated Web CSS runtime              PASS
generated Native TypeScript runtime    PASS
```

The Metro package-resolution diagnosis and accepted repair are documented in section 7 above. Preserve that evidence: do not replace the public package import with a permanent relative deep path, and do not add Metro/hoisting overrides without new contrary evidence.

Validated implementation commit:

```text
acd846a06614270fda9d66542a3fdc87fca7202e
feat: materialize shared design tokens
```

## 17. Clean-machine/onboarding acceptance target

A future developer should be able to start from repository documentation and reach a working frontend without chat context:

```text
clone or create linked WSL worktree
→ install documented machine prerequisites
→ install/activate fnm
→ select governed Node runtime
→ activate governed pnpm
→ pnpm install --frozen-lockfile
→ pnpm lint
→ pnpm format:check
→ pnpm typecheck
→ pnpm build
→ start Web
→ open Web from Windows browser
→ start Mobile in WSL → establish ADB reverse → launch on Windows Android emulator
→ diagnose failures from documented ownership boundaries
```

The runtime/root-tooling/Web/minimal-Mobile/shared-design-token portion is directly proven. Genuine shared-package consumption is now proven; the full materialization target is not PASS until the remaining shared-core/enforcement obligations required by FM-05/FM-06/FM-07 are directly exercised.

## 18. Troubleshooting discipline

When a command fails:

```text
capture exact command
capture full output
identify owning layer
change one variable
rerun the smallest relevant validation
record durable fix if it is project-specific
```

Do not respond to dependency/tooling failures with random global installs, blanket cache deletion, force flags or broad version changes unless evidence justifies them.

Examples:

```text
Node executable/version        workstation runtime
pnpm resolution/lockfile       workspace/package layer
TypeScript base config         root engineering tooling
ESLint / Prettier              root engineering tooling
Turbo task graph               workspace orchestration
Vite build                     Web app/toolchain
Vite localhost reachability    WSL↔Windows Web developer adapter
TanStack generated route tree  Web routing generation
Metro resolution               Mobile/toolchain
ADB/emulator communication     WSL↔Windows Mobile developer adapter
PowerSync/SQLite               Mobile sync platform boundary
PostgreSQL                     Docker/backend LOCAL infra
```

## 19. Current next action

Proceed to **FM-05B `@dante/i18n`**.

Materialize a framework-free shared i18n core only with immediate real Web+Mobile consumers. It may own supported locales, shared resources/contracts, fallback semantics and common keys/types. React integration, browser/native locale detection and persistence/storage remain application/platform responsibilities.

After FM-05B, `@dante/time` remains the planned FM-05C shared-core slice under a separate bounded gate.

This does not authorize Access/Home production UI, PowerSync integration, EAS release infrastructure or invented backend contracts.

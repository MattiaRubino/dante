# Frontend Local Development and Workstation Runbook

- Status: **CURRENT FOR `feature/frontend-materialization`**
- Purpose: reproducible frontend workstation setup, installation guidance and LOCAL topology
- Foundation authority: Frontend Engineering Foundation integrated via PR #22
- Current execution state: **FM-00 PREFLIGHT NOT RUN**

## 1. Core posture

DANTE uses one authoritative repository checkout under WSL/Linux semantics.

```text
Windows 11
├── JetBrains / PyCharm UI
├── browser
├── Android Studio / emulator
└── Docker Desktop

WSL2 / Linux
├── Git checkout
├── Node / pnpm / Turbo
├── Vite
├── Metro / Expo CLI
├── Python / uv where applicable
└── Docker CLI
```

Docker is used for real stateful/local infrastructure, not as a blanket wrapper around every development process.

Normal LOCAL ownership:

```text
Git checkout             WSL filesystem
Node/pnpm/Turbo          WSL
Vite                     WSL
Metro/Expo CLI           WSL
PyCharm/JetBrains UI     Windows using WSL project/tooling
browser                  Windows
Android Studio/emulator  Windows
Docker daemon            Docker Desktop / WSL integration
PostgreSQL               Docker when backend LOCAL infra is active
```

## 2. Filesystem invariant

Preferred repository location is inside the Linux filesystem, for example:

```text
/home/<user>/projects/dante
~/projects/dante
```

Avoid using a Windows-backed repository path such as `/mnt/c/...` as the authoritative checkout unless concrete evidence forces a different choice.

Hard rules:

```text
one authoritative checkout
no second Windows clone used for the same active work
no shared cross-OS node_modules
no manual file copying between Windows and WSL source trees
```

## 3. Python analogy for frontend dependency management

Conceptual mapping:

| Backend/Python | Frontend/TypeScript |
| --- | --- |
| Python runtime | Node runtime |
| `uv` | `pnpm` |
| `pyproject.toml` | `package.json` |
| `uv.lock` | `pnpm-lock.yaml` |
| `.venv` | project dependency graph exposed through `node_modules` |
| `uv sync` | `pnpm install` |

The analogy is useful but not exact.

A Python virtual environment carries an isolated interpreter environment. Frontend `node_modules` governs project dependencies while Node itself is normally a machine/runtime-level tool in WSL whose required version is declared by the repository.

The repository therefore governs both:

```text
runtime expectation
Node exact accepted line/patch policy

project dependency graph
package.json + pnpm-lock.yaml
```

## 4. Machine-level versus repository-managed tooling

Machine/WSL level:

- Git;
- Node runtime/version-management mechanism;
- pnpm activation mechanism;
- Docker CLI integration;
- Android platform tooling on Windows.

Repository-managed dependencies include, when materialized:

- TypeScript;
- Turborepo;
- React;
- Vite;
- Expo;
- React Native;
- TanStack libraries;
- Zod;
- ESLint;
- Prettier;
- test tooling;
- generation tooling.

Project libraries are not installed globally for convenience.

Avoid patterns such as:

```text
npm install -g vite
npm install -g typescript
npm install -g expo
```

unless a future tool explicitly requires global installation and that exception is documented.

Do not use `sudo npm ...` to repair project dependency problems.

## 5. Version governance

Accepted design baseline:

```text
Node        24 LTS
pnpm        11
TypeScript  6.0.x strict
Turbo       2.x
```

Exact patches are resolved during materialization using current primary documentation and real compatibility constraints.

Repository authorities will record versions through the appropriate combination of:

- root `package.json`;
- `packageManager` declaration;
- `engines`/runtime policy where useful;
- a Node version file/tooling contract;
- `pnpm-lock.yaml`;
- app/package manifests.

The lockfile is committed. Normal CI will use frozen-lockfile semantics once CI exists.

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

Reasons include faster feedback, simpler IDE/debug integration, fewer filesystem/network indirections and cleaner Android tooling integration.

Docker container lifecycle and persistent data lifecycle are separate. Stateful services use explicit persistent volumes/storage where required.

## 7. Browser and Mobile networking

### Web

The target normal path is:

```text
Vite in WSL
↓
localhost/forwarded dev port
↓
Windows browser
```

This path must be directly validated during FM-03 rather than assumed.

### Mobile

The target normal path is:

```text
Metro / Expo CLI in WSL
↓
WSL↔Windows network + Android tooling bridge
↓
Android emulator/device on Windows
```

The exact networking/ADB adapter is not pre-guessed. Start from the default current WSL posture, observe evidence, then configure only what is actually necessary.

A tooling/network repair may change the adapter without reopening the frontend architecture.

## 8. Command policy

Repository scripts should become the normal entry point once the workspace exists.

Target ergonomic surface, as applicable:

```text
pnpm install
pnpm dev
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Individual app/package commands may exist, but developers should not need undocumented command sequences from chat history.

When invoking repository tools directly, prefer project-local execution through pnpm rather than unrelated global binaries.

## 9. FM-00 — read-only WSL preflight

Run this before installing or repairing frontend tooling.

From the authoritative DANTE checkout in WSL:

```bash
printf '\n=== LOCATION / GIT ===\n'
pwd
git rev-parse --show-toplevel
git status --short --branch
git rev-parse HEAD

printf '\n=== LINUX / WSL ===\n'
uname -a
cat /etc/os-release

printf '\n=== GIT ===\n'
git --version
command -v git

printf '\n=== NODE / NPM / PNPM / COREPACK ===\n'
command -v node || true
node --version 2>/dev/null || true
command -v npm || true
npm --version 2>/dev/null || true
command -v pnpm || true
pnpm --version 2>/dev/null || true
command -v corepack || true
corepack --version 2>/dev/null || true

printf '\n=== DOCKER ===\n'
command -v docker || true
docker --version 2>/dev/null || true
docker compose version 2>/dev/null || true
```

This block is diagnostic only. It must not install, remove or alter packages.

Return the complete output for review.

## 10. Optional Windows-side preflight

Run only when requested after the WSL output is classified.

Likely evidence includes:

```powershell
wsl --version
wsl -l -v
```

Android Studio/SDK/emulator and Docker Desktop integration are inspected when their phase becomes applicable rather than front-loading unrelated configuration.

## 11. FM-00 review criteria

The preflight review classifies:

### Repository

- correct repository;
- authoritative checkout resides in WSL filesystem;
- expected branch;
- expected HEAD relationship;
- no unrelated local changes before setup work.

### Runtime

- whether Node exists;
- exact Node version;
- exact executable path;
- whether it is Linux-native;
- whether npm/pnpm/Corepack already exist and where they resolve.

### Docker

- CLI presence;
- Compose availability;
- whether WSL can reach the Docker daemon when needed.

### Repairs

Every required repair is proposed explicitly before it is executed. Do not layer several package managers/version managers until one path works.

## 12. Installation principles after FM-00

When FM-01 is authorized:

1. verify the currently supported Node 24 LTS patch and pnpm 11 line against current primary sources;
2. choose one clean WSL Node version-management/runtime installation mechanism;
3. install/activate only what is missing;
4. verify executable paths and versions;
5. record repository runtime declarations;
6. do not install React/Vite/Expo globally;
7. create no production app until runtime/package-manager evidence is clean.

If the machine already has an acceptable clean runtime, do not reinstall merely for uniformity.

## 13. Clean-machine/onboarding acceptance target

A future developer should be able to start from repository documentation and reach a working frontend without chat context.

The final materialized runbook must make this path reproducible:

```text
clone/open authoritative WSL checkout
→ select governed Node runtime
→ activate governed pnpm
→ install locked dependencies
→ run lint/typecheck/tests
→ start Web
→ start Mobile on supported local target
→ diagnose failures from documented ownership boundaries
```

## 14. Troubleshooting discipline

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

Examples of owning layers:

```text
Node executable/version        workstation runtime
pnpm resolution/lockfile       workspace/package layer
Vite build                     Web app/toolchain
Metro resolution               Mobile/toolchain
ADB/emulator communication     WSL↔Windows developer adapter
PowerSync/SQLite               Mobile sync platform boundary
PostgreSQL                     Docker/backend LOCAL infra
```

## 15. Current next action

Run **FM-00 read-only WSL preflight** from section 9 and return the complete output.

No installation is authorized by this runbook until that output is reviewed.

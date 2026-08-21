# Local Backend Workstation Bootstrap

- Status: **ACTIVE / VERIFIED THROUGH BACKEND CP2**
- Scope: Windows 11 developer workstation bootstrap for DANTE backend work
- Canonical backend development environment: **WSL2 + Ubuntu 24.04 LTS + Linux filesystem**
- Verified workstation checkpoint date: **2026-08-20**
- Backend CP1: **CLOSED / DIRECT QA PASS**
- Backend CP2 / PostgreSQL LOCAL: **CLOSED / DIRECT QA PASS**
- Next backend checkpoint: **CP3 READ-ONLY DESIGN/RESEARCH**

## 1. Purpose

This guide is the quick, reproducible path for setting up a new DANTE backend development workstation or onboarding another developer without reconstructing the setup from chat history.

It records both:

1. the reusable installation procedure; and
2. the exact verified checkpoint reached on the first DANTE workstation.

The Engineering Foundation and active checkpoint contracts remain authoritative for architectural decisions. This document is an operational bootstrap guide and must not silently redefine those decisions.

## 2. Target workstation model

```text
Windows 11
├── PyCharm on Windows
├── DBeaver or equivalent DB GUI on Windows
├── Docker Desktop on Windows
│   └── WSL2 backend
│
└── WSL2
    └── Ubuntu 24.04 LTS
        ├── Git
        ├── GitHub CLI
        ├── uv
        ├── Python 3.14.7
        ├── Docker CLI / Compose via Docker Desktop integration
        └── /home/<user>/projects/dante
            ├── apps/backend/.venv
            └── infra/compose + infra/local/postgres
```

Rules:

- backend/server semantics are Linux;
- the repository lives in the Linux filesystem, not under `/mnt/c/...` or `/mnt/d/...`;
- Python for DANTE is managed by `uv`, not by replacing Ubuntu's system Python;
- Docker Desktop provides the local container engine through WSL2;
- do not install a second Docker Engine directly inside Ubuntu when using Docker Desktop WSL integration;
- PostgreSQL is not installed directly on Windows or directly into Ubuntu for the DANTE LOCAL baseline;
- the DANTE LOCAL PostgreSQL server runs through the repository-owned Docker Compose definition;
- Windows database GUIs are clients only, not alternate database servers.

## 3. Install WSL without an automatic distribution

Open **PowerShell as Administrator**:

```powershell
wsl --install --no-distribution
```

Restart Windows when requested.

Verify after reboot:

```powershell
wsl --status
wsl --version
wsl --list --online
```

Expected fundamentals:

```text
default WSL version = 2
Ubuntu-24.04 available
```

The first verified workstation reported:

```text
WSL                  2.7.12.0
kernel               6.18.33.2-2
default WSL version  2
```

These exact WSL/kernel versions are evidence of the verified workstation, not permanent project pins.

## 4. Install Ubuntu 24.04 on the secondary drive

The first workstation intentionally stores the WSL distribution on `D:` rather than consuming the Windows system drive.

PowerShell:

```powershell
wsl --install -d Ubuntu-24.04 --location D:\WSL\Ubuntu-24.04
```

Create the Unix username/password when prompted.

Verify from PowerShell:

```powershell
wsl --list --verbose
```

Expected:

```text
Ubuntu-24.04    Running/Stopped    2
```

Verify inside Ubuntu:

```bash
cd ~
pwd
whoami
cat /etc/os-release
```

Expected shape:

```text
/home/<user>
<user>
Ubuntu 24.04.x LTS
```

The first workstation verified **Ubuntu 24.04.4 LTS (Noble Numbat)**.

### Important path rule

Launching WSL from a Windows PowerShell directory may initially place the shell under a path such as:

```text
/mnt/c/WINDOWS/system32
```

That does **not** mean the distro itself is stored on `C:`. Move to the Linux home before development:

```bash
cd ~
```

DANTE source code must live under the Linux filesystem.

## 5. Update Ubuntu and install base tools

Inside Ubuntu:

```bash
sudo apt update
sudo apt upgrade -y

sudo apt install -y \
  git \
  curl \
  ca-certificates \
  build-essential \
  rsync \
  unzip
```

Verify:

```bash
git --version
curl --version | head -n 1
rsync --version | head -n 1
```

First workstation evidence:

```text
git    2.43.0
curl   8.5.0
rsync  3.2.7
```

These package versions come from the then-current Ubuntu installation and are not project-level pins unless a later engineering decision explicitly says otherwise.

## 6. Install and authenticate GitHub CLI

Install:

```bash
sudo apt update
sudo apt install -y gh
```

Authenticate through the browser flow:

```bash
gh auth login --web --git-protocol https
```

When asked:

```text
Authenticate Git with your GitHub credentials? → Yes
```

If WSL cannot automatically launch the Windows browser, leave the terminal running and manually open the GitHub device-login URL shown by `gh`, then enter the one-time code displayed in the terminal.

After successful authorization:

```bash
gh auth setup-git
gh auth status
```

Required result:

```text
account              MattiaRubino or authorized collaborator
Git protocol         https
active account       true
```

Never paste or document the authentication token itself. Do not run `gh auth status --show-token` for evidence.

## 7. Configure Git identity

For the first workstation:

```bash
git config --global user.name "MattiaRubino"
git config --global user.email "132660543+MattiaRubino@users.noreply.github.com"
```

A future collaborator uses their own verified GitHub identity instead.

## 8. Clone DANTE into the Linux filesystem

Create a Linux-native project directory:

```bash
mkdir -p ~/projects
cd ~/projects

gh repo clone MattiaRubino/dante
cd dante
```

Canonical local path shape:

```text
/home/<user>/projects/dante
```

Do not use routine development locations such as:

```text
/mnt/c/...
/mnt/d/...
```

for the repository itself.

Verify:

```bash
pwd
git status
git remote -v
git log -1 --oneline
```

Current repository remote:

```text
https://github.com/MattiaRubino/dante.git
```

At the current backend-scaffold checkpoint, the working branch is:

```text
feature/backend-scaffold
```

Checkout when that branch is the active approved scope:

```bash
git fetch origin
git switch feature/backend-scaffold
```

Do not treat this branch name as a permanent onboarding branch. Future work starts from the current approved `main` and uses the bounded branch defined by that workstream.

## 9. Install `uv`

Use the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Load the installed path in the current shell:

```bash
source "$HOME/.local/bin/env"
```

Verify:

```bash
uv --version
command -v uv
```

First workstation evidence:

```text
uv 0.12.5
/home/mattia/.local/bin/uv
```

The verified version is recorded as evidence. The project scaffold/lock/tool policy remains the authority for future reproducible version control.

## 10. Install DANTE Python with `uv`

DANTE backend baseline:

```text
supported line  Python 3.14.x
initial pin     Python 3.14.7
```

Install exactly the initial pin:

```bash
uv python install 3.14.7
```

Verify:

```bash
uv python list | head -n 20
python3.14 --version
command -v python3.14
```

Expected:

```text
Python 3.14.7
/home/<user>/.local/bin/python3.14
```

Do **not** make this a replacement for Ubuntu's generic system `python3`.

The first workstation intentionally keeps:

```text
Ubuntu system Python  3.12.x
DANTE uv Python       3.14.7
```

separate.

Final interpreter verification:

```bash
python3.14 -c "import sys, platform; print(sys.version); print(sys.executable); print(platform.machine()); print(platform.system())"
```

First workstation verified:

```text
Python               3.14.7
architecture         x86_64
platform             Linux
DANTE interpreter    /home/mattia/.local/bin/python3.14
```

## 11. Bootstrap the DANTE backend environment

After CP1 exists on the active branch:

```bash
cd ~/projects/dante/apps/backend
uv sync --locked
uv lock --check
```

`uv sync --locked` creates the repository-local backend environment:

```text
/home/<user>/projects/dante/apps/backend/.venv
```

The first workstation directly verified:

```text
project Python       3.14.7
project executable   apps/backend/.venv/bin/python3
installed namespace  dante from apps/backend/src/dante
```

The lockfile is repository authority for the exact dependency graph. Do not hand-edit it.

Current CP1 direct graph after final resolver/remote verification:

```text
fastapi             0.141.1
pydantic            2.13.4
pydantic-settings   2.15.0
uvicorn             0.52.4
httpx2               2.12.0
mypy                 2.3.1
pytest               9.1.1
pytest-cov           7.1.0
ruff                 0.16.3
```

## 12. PyCharm usage model

The repository remains inside WSL but is opened from PyCharm running on Windows.

Windows path shape:

```text
\\wsl.localhost\Ubuntu-24.04\home\<user>\projects\dante
```

or the equivalent `\\wsl$\...` path supported by the workstation.

Verified backend interpreter target:

```text
PyCharm on Windows
        ↓
WSL Ubuntu-24.04 project
        ↓
/home/<user>/projects/dante/apps/backend/.venv/bin/python
```

Do not let the IDE manufacture an unrelated Windows Python environment.

IDE convenience must never be required for repository correctness: build/test/lint/type/migration commands remain CLI-capable.

## 13. Install Docker Desktop on Windows

Use Docker Desktop for Windows with the **WSL2 backend**.

For a normal single-user development workstation, use the per-user installation mode unless an explicit machine-administration requirement says otherwise.

Do not enable Windows Containers or Kubernetes for the DANTE backend bootstrap.

After installation, open Docker Desktop and verify:

```text
Settings
→ General
→ WSL 2 based engine enabled / active

Settings
→ Resources
→ WSL Integration
→ Ubuntu-24.04 ON
```

The first workstation explicitly enabled `Ubuntu-24.04` rather than enabling every future/default WSL distribution implicitly.

### Docker data location

Container images, layers, build cache and volumes may become large. Prefer a secondary drive where available, for example:

```text
D:\Docker\DesktopData
```

Use Docker Desktop's own **Disk image location** setting to move/manage that storage. Do not manually move Docker's VHDX files.

The exact disk-image location must be verified separately on each workstation; Docker functionality PASS does not by itself prove the storage location.

The first DANTE workstation was explicitly verified in Docker Desktop under **Settings → Resources → Advanced** with:

```text
WSL 2 backend       ACTIVE
Disk image location D:\Docker\DesktopData\DockerDesktopWSL
```

Therefore Docker images, layers, build cache and Docker-managed volume data for this workstation are anchored on the secondary `D:` drive rather than the Windows system drive.

## 14. Verify Docker inside Ubuntu

With Docker Desktop running and `Ubuntu-24.04` integration enabled, open Ubuntu and run:

```bash
command -v docker
groups
docker --version
docker compose version
docker info --format 'OS={{.OSType}} ARCH={{.Architecture}}'
```

Expected fundamentals:

```text
docker CLI present
Docker daemon reachable without sudo
OS=linux
ARCH=x86_64
```

The first workstation ultimately verified:

```text
Docker Engine/CLI      29.7.2
Docker Compose         v5.4.0
Docker daemon OS       linux
Docker architecture    x86_64
```

These Docker/Compose versions are workstation evidence, not permanent DANTE pins unless later repository-controlled infrastructure declares one.

## 15. Docker socket permission case encountered on the first workstation

The first workstation initially showed:

```text
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

Diagnosis:

```bash
whoami
groups
command -v docker
ls -l /var/run/docker.sock
readlink -f /var/run/docker.sock
docker context ls
env | grep -E '^DOCKER_' || true
ls -ld /mnt/wsl/docker-desktop 2>/dev/null || echo "docker-desktop mount non trovato"
```

Observed state:

```text
socket       /var/run/docker.sock
owner/group  root:docker
mode         srw-rw----
user         not yet a member of docker group
Docker Desktop WSL mount present
```

Fix used:

```bash
sudo usermod -aG docker $USER
getent group docker
```

Then close Ubuntu and from PowerShell terminate the distro so supplementary groups are reloaded:

```powershell
wsl --terminate Ubuntu-24.04
```

Restart Docker Desktop if required, verify `Ubuntu-24.04` remains enabled under **Settings → Resources → WSL Integration**, then reopen Ubuntu.

Verify the group membership:

```bash
groups
```

Expected to include:

```text
docker
```

Do **not** install a second Docker Engine in Ubuntu and do not use permanent `sudo docker ...` as a workaround for a broken Desktop integration.

Membership of the `docker` group provides high privilege over the local Docker daemon and is intentional only for trusted developer accounts on the workstation.

### Integration reset case

After terminating the distro, the first workstation temporarily reported that `docker` could not be found. Docker Desktop's WSL integration was reset by toggling:

```text
Ubuntu-24.04 OFF
Apply
Ubuntu-24.04 ON
Apply & Restart
```

After reopening Ubuntu, the CLI and daemon were available correctly.

## 16. Docker end-to-end smoke test

Run without `sudo`:

```bash
docker run --rm hello-world
```

A valid PASS proves that the WSL CLI can:

1. contact the Docker Desktop daemon;
2. pull an image from Docker Hub;
3. create/run a Linux amd64 container;
4. receive the container output;
5. remove the test container after exit.

The first workstation produced:

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

Therefore the workstation checkpoint is:

```text
Docker Desktop                  PASS
Docker Desktop WSL2 backend     PASS
Ubuntu-24.04 integration        PASS
Docker CLI from Ubuntu          PASS
Docker Compose                  PASS
Docker daemon access no sudo    PASS
linux/x86_64 container engine   PASS
Docker Hub pull                 PASS
hello-world container           PASS
Docker data location on D:      PASS
```

## 17. Verify backend CP1

From `apps/backend`:

```bash
uv lock --check
uv tree --locked --depth 1
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv build
```

The first workstation directly verified all commands above on the final locked environment.

Final CP1 test evidence:

```text
pytest                  25/25 PASS
statement coverage      100.00%
branch coverage         100.00%
```

The 100% value describes the small CP1 surface only and is not a permanent arbitrary threshold.

For real process verification:

```bash
cp .env.example .env.local
uv run --env-file .env.local \
  uvicorn dante.bootstrap.app:create_app \
  --factory \
  --reload
```

In a second WSL terminal:

```bash
curl -sS http://127.0.0.1:8000/health/live; printf '\n'
curl -sS http://127.0.0.1:8000/health/ready; printf '\n'
```

First workstation evidence:

```text
Uvicorn factory startup   PASS
/health/live              {"status":"ok"}
/health/ready             {"status":"ready"}
```

`.env.local`, `.venv`, `.coverage`, build output and tool caches are local/generated state and are not committed as source artifacts; `uv.lock` is committed.

## 18. Bootstrap and operate DANTE LOCAL PostgreSQL — CP2 VERIFIED

PostgreSQL server is **container-only** for the DANTE LOCAL baseline.

Do not install a second PostgreSQL server on Windows or directly into Ubuntu.

Canonical repository-owned components:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/010-extensions.sql
infra/compose/local.yaml
infra/compose/README.md
```

The durable design/acceptance authority is:

`docs/development/backend-cp2-postgres-contract.md`

### 18.1 Create the workstation-local PostgreSQL password

From repository root, create the local secret only if it does not already exist:

```bash
cd ~/projects/dante

python3 - <<'PY'
import os
import secrets
from pathlib import Path

path = Path("infra/compose/secrets/postgres_password.local")

if path.exists():
    raise SystemExit(f"STOP: {path} already exists")

path.parent.mkdir(parents=True, exist_ok=True)
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, "w", encoding="utf-8") as file:
    file.write(secrets.token_urlsafe(32) + "\n")

print(f"created: {path}")
PY
```

Verify without printing the secret:

```bash
stat -c '%a %n' infra/compose/secrets/postgres_password.local
git check-ignore -v infra/compose/secrets/postgres_password.local
git status --short
```

Required fundamentals:

```text
mode                 600
Git ignore           PASS
working tree         unchanged by secret creation
```

Never commit or paste the secret into documentation/chat evidence.

### 18.2 Validate and build

```bash
docker compose -f infra/compose/local.yaml config --quiet
```

For the canonical clean-build proof:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

Routine later builds may use the standard build command documented in `infra/compose/README.md`.

The first workstation directly verified the repaired clean build after discovering that the pinned PostgreSQL base required Debian `ca-certificates` before HTTPS access to the PGDG historical archive. The repository repair preserves TLS certificate verification and PGDG signed-repository verification.

### 18.3 Start/stop

Start and wait for health:

```bash
docker compose -f infra/compose/local.yaml up -d --wait
```

Inspect:

```bash
docker compose -f infra/compose/local.yaml ps
docker compose -f infra/compose/local.yaml logs postgres
```

Normal stop that **preserves data**:

```bash
docker compose -f infra/compose/local.yaml down
```

Destructive LOCAL cluster reset:

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

`down --volumes` destroys the Compose PostgreSQL named volume. Use it only when an explicit reset is intended.

### 18.4 Verified CP2 database envelope

The first workstation directly proved:

```text
PostgreSQL                       18.4
PostGIS                          3.6.4
pgvector                         0.8.6
pg_trgm                          enabled / functional
unaccent                         enabled / functional
pg_stat_statements               enabled / preloaded / collecting
native PostgreSQL FTS            functional
Compose health                   PASS
named-volume persistence         PASS
destructive reset                PASS
fresh reinitialization           PASS
```

The selected extension inventory observed after fresh initialization:

```text
pg_stat_statements  1.12
pg_trgm             1.6
postgis             3.6.4
unaccent            1.1
vector              0.8.6
```

### 18.5 Windows GUI connectivity

The Windows GUI connects to the container; it does not replace it.

Verified DBeaver connection:

```text
Host      127.0.0.1
Port      5432
Database  dante
User      postgres
Password  contents of the ignored workstation-local secret
```

To copy the password to the Windows clipboard without printing it in the terminal:

```bash
clip.exe < infra/compose/secrets/postgres_password.local
```

Direct GUI acceptance query:

```sql
SELECT current_database(), current_user, version();
```

First workstation observed:

```text
current_database = dante
current_user     = postgres
PostgreSQL       = 18.4 line
```

DBeaver therefore directly proved the Windows → loopback published port → Docker PostgreSQL boundary.

CP2 does not yet add SQLAlchemy/psycopg application connectivity, Alembic, application DB settings, runtime/migrator identities or concrete schema mappings. Those return under CP3 or later bounded authority.

## 19. Current verified checkpoint

As of 2026-08-20:

```text
Repository                         MattiaRubino/dante
Working branch                     feature/backend-scaffold
Workspace                          /home/mattia/projects/dante

WSL                                PASS
WSL2                               PASS
Ubuntu 24.04 LTS                   PASS
Linux-native repository path       PASS
base Linux tools                   PASS
GitHub CLI authentication          PASS
HTTPS Git credential integration   PASS
uv                                 PASS
Python 3.14.7                      PASS
Linux x86_64 interpreter           PASS

Docker Desktop                     PASS
Docker WSL2 backend                PASS
Ubuntu-24.04 Docker integration    PASS
Docker CLI                         PASS
Docker Compose                     PASS
Docker daemon access               PASS
Docker hello-world                 PASS
Docker data location on D:         PASS

backend CP1 project                PASS
backend .venv                      PASS
locked dependency graph            PASS / REMOTE
FastAPI factory process            PASS
Ruff                               PASS
mypy strict                        PASS
pytest                             PASS
uv build                           PASS
real HTTP probes                   PASS

backend CP2 PostgreSQL             CLOSED / DIRECT QA PASS
DANTE PostgreSQL image             PASS
PostgreSQL 18.4                    PASS
selected extension envelope        PASS
functional extension probes        PASS
pg_stat_statements                 PASS
named-volume persistence           PASS
destructive reset                  PASS
Windows DBeaver connectivity       PASS

backend CP3                        NEXT / NOT STARTED
```

The current post-reset LOCAL PostgreSQL state is a fresh healthy cluster with the selected extension envelope initialized and no CP2 persistence-probe table retained.

## 20. Resume rule

When continuing on a new machine or after interruption:

1. identify the first section whose verification is not PASS;
2. re-run the verification command for the immediately preceding PASS boundary;
3. continue from there;
4. treat CP1 and CP2 as CLOSED / DIRECT QA PASS unless new direct evidence contradicts them;
5. never infer application persistence, migration, HG/PSV or production PASS from CP2 infrastructure evidence;
6. current next backend checkpoint is CP3 READ-ONLY design/research;
7. before any repository write, follow the current exact Git write gate for the active branch/workstream.

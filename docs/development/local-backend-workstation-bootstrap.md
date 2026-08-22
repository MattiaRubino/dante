# Local Backend Workstation Bootstrap

- Status: **ACTIVE / VERIFIED REUSABLE WORKSTATION BASELINE**
- Scope: Windows 11 developer workstation bootstrap for DANTE backend work
- Canonical backend development environment: **WSL2 + Ubuntu 24.04 LTS + Linux filesystem**
- First verified workstation checkpoint date: **2026-08-20**
- First-workstation CP1/CP2 evidence below: **HISTORICAL / DIRECT QA PASS**
- Production backend scaffold CP1–CP5: **CLOSED / INTEGRATED / DIRECT QA PASS**
- Current backend workstream: `feature/logical-postgresql` — **CP6 ACTIVE / DESIGN-FIRST**
- Current PostgreSQL technical image: **`dante-postgres-local:18.6`**
- PostgreSQL 18.6 technical regression: **DIRECT REMOTE QA PASS — run `32568664940` / HEAD `ec3dc795b5e044daa3a77723c94a1b4b5b92865c`**
- Current CP6 checkpoint: **CP6-02 CLOSED / GATE 02 PASS; CP6-03 NEXT / NOT STARTED**

## 1. Purpose and evidence split

This guide is the quick, reproducible path for setting up a DANTE backend development workstation or onboarding another developer without reconstructing the setup from chat history.

It deliberately separates:

1. the **reusable current installation/operation procedure**; and
2. the **exact first-workstation evidence** recorded when CP1/CP2 were originally proved on PostgreSQL 18.4.

The first-workstation 18.4 observations remain historically exact. Current repository/runtime truth is PostgreSQL major line 18 with maintenance patch 18.6. CP6 directly re-proved the existing technical foundation on 18.6; this does not rewrite CP2/CP3 history or imply business persistence PASS.

The active workstream and current project/status documents remain authoritative for architecture and checkpoint status. This operational guide must not redefine them.

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

First-workstation evidence:

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

First-workstation evidence:

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

Authenticate:

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

## 8. Clone DANTE and select the active bounded workstream

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

Do not use routine development locations such as `/mnt/c/...` or `/mnt/d/...` for the repository itself.

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

The original backend-scaffold implementation used `feature/backend-scaffold`; that branch is now historical and its work is integrated through PR #24.

Current CP6 backend work uses:

```text
feature/logical-postgresql
```

When resuming CP6:

```bash
git fetch origin
git switch feature/logical-postgresql
git pull --ff-only
```

Never treat a workstream branch name as a permanent onboarding branch. Always consume `docs/PROJECT-STATUS.md` and the active durable workstream before writes.

## 9. Install `uv`

Use the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

Verify:

```bash
uv --version
command -v uv
```

First-workstation evidence:

```text
uv 0.12.5
/home/mattia/.local/bin/uv
```

The verified version is evidence; project configuration remains the authority for the exact required version.

## 10. Install DANTE Python with `uv`

DANTE backend baseline:

```text
supported line  Python 3.14.x
initial pin     Python 3.14.7
```

Install:

```bash
uv python install 3.14.7
```

Verify:

```bash
uv python list | head -n 20
python3.14 --version
command -v python3.14
```

Do **not** make this a replacement for Ubuntu's generic system `python3`.

First-workstation evidence intentionally kept:

```text
Ubuntu system Python  3.12.x
DANTE uv Python       3.14.7
```

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

```bash
cd ~/projects/dante/apps/backend
uv sync --locked
uv lock --check
```

The repository-local environment is:

```text
/home/<user>/projects/dante/apps/backend/.venv
```

First-workstation evidence:

```text
project Python       3.14.7
project executable   apps/backend/.venv/bin/python3
installed namespace  dante from apps/backend/src/dante
```

The lockfile is repository authority for the exact dependency graph. Do not hand-edit it.

Current project resolution at the CP6-02 closure includes:

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
SQLAlchemy           2.0.52
psycopg              3.3.4
Alembic              1.19.1
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

Do not let the IDE manufacture an unrelated Windows Python environment. CLI build/test/lint/type/migration commands remain authoritative.

## 13. Install Docker Desktop on Windows

Use Docker Desktop for Windows with the **WSL2 backend**.

For a normal single-user development workstation, use the per-user installation mode unless an explicit machine-administration requirement says otherwise.

Do not enable Windows Containers or Kubernetes for the DANTE backend bootstrap.

Verify:

```text
Settings
→ General
→ WSL 2 based engine enabled / active

Settings
→ Resources
→ WSL Integration
→ Ubuntu-24.04 ON
```

The first workstation explicitly enabled `Ubuntu-24.04` rather than every WSL distribution implicitly.

### Docker data location

Prefer a secondary drive where available, for example:

```text
D:\Docker\DesktopData
```

Use Docker Desktop's own **Disk image location** setting. Do not manually move Docker's VHDX files.

First-workstation direct verification:

```text
WSL 2 backend        ACTIVE
Disk image location D:\Docker\DesktopData\DockerDesktopWSL
```

## 14. Verify Docker inside Ubuntu

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

First-workstation evidence:

```text
Docker Engine/CLI      29.7.2
Docker Compose         v5.4.0
Docker daemon OS       linux
Docker architecture    x86_64
```

These Docker/Compose versions are workstation evidence, not permanent DANTE pins.

## 15. Docker socket permission case from the first workstation

Initial symptom:

```text
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
```

Diagnosis used:

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

Observed:

```text
socket       /var/run/docker.sock
owner/group  root:docker
mode         srw-rw----
user         not yet a member of docker group
Docker Desktop WSL mount present
```

Fix:

```bash
sudo usermod -aG docker $USER
getent group docker
```

Then from PowerShell terminate the distro so supplementary groups reload:

```powershell
wsl --terminate Ubuntu-24.04
```

Restart Docker Desktop if required and verify WSL integration remains enabled. Do not install a second Docker Engine in Ubuntu and do not use permanent `sudo docker ...` as a workaround.

Membership of the `docker` group provides high privilege over the local Docker daemon and is intentional only for trusted developer accounts.

### Integration reset case

After terminating the distro, if `docker` disappears, reset Docker Desktop's WSL integration:

```text
Ubuntu-24.04 OFF
Apply
Ubuntu-24.04 ON
Apply & Restart
```

## 16. Docker end-to-end smoke test

```bash
docker run --rm hello-world
```

A valid PASS proves WSL CLI → Docker Desktop daemon → pull → Linux container execution → cleanup.

First-workstation result:

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

## 17. Verify backend quality foundation

From `apps/backend`:

```bash
uv lock --check
uv tree --locked --depth 1
uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest -m "not postgres"
uv build
```

For real process verification after valid runtime DB configuration:

```bash
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

Historical CP1 evidence:

```text
pytest                  25/25 PASS
statement coverage      100.00%
branch coverage         100.00%
Uvicorn factory startup PASS
/health/live            {"status":"ok"}
/health/ready           {"status":"ready"}
```

The 100% value describes the small CP1 surface only and is not a project threshold.

`.env.local`, `.venv`, `.coverage`, build output and tool caches are local/generated state and are not committed; `uv.lock` is committed.

## 18. Bootstrap and operate DANTE LOCAL PostgreSQL

PostgreSQL server is **container-only** for the DANTE LOCAL baseline.

Do not install a second PostgreSQL server on Windows or directly into Ubuntu.

Canonical repository-owned components:

```text
infra/local/postgres/Dockerfile
infra/local/postgres/initdb/010-extensions.sql
infra/compose/local.yaml
infra/compose/README.md
```

Historical CP2 design/acceptance authority:

`docs/development/backend-cp2-postgres-contract.md`

Closed CP6 reusable database doctrine:

`docs/development/backend-cp6-02-postgresql-persistence-constitution.md`

Gate 02 closure evidence:

`docs/development/backend-cp6-02-postgresql-persistence-constitution-closure.md`

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

Never commit or paste the secret.

### 18.2 Validate and build current PostgreSQL image

```bash
docker compose -f infra/compose/local.yaml config --quiet
docker compose -f infra/compose/local.yaml build postgres
```

For a clean-build proof when explicitly needed:

```bash
docker compose -f infra/compose/local.yaml build --no-cache postgres
```

Current repository-controlled image:

```text
dante-postgres-local:18.6
postgres:18.6-trixie
OCI index digest sha256:ae6c78831cbc35fa3a4aaf4d763ddacf6183d6004774cc2dc28b3920410d1d1a
```

The image keeps exact extension package pins:

```text
PostGIS   3.6.4
pgvector  0.8.6
```

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

Destructive LOCAL reset:

```bash
docker compose -f infra/compose/local.yaml down --volumes
```

`down --volumes` destroys the Compose PostgreSQL named volume. Use it only when an explicit reset is intended.

### 18.4 Historical first-workstation CP2 database envelope — DO NOT REWRITE

The first workstation directly proved on 2026-08-20:

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

Observed extension inventory:

```text
pg_stat_statements  1.12
pg_trgm             1.6
postgis             3.6.4
unaccent            1.1
vector              0.8.6
```

That 18.4 evidence remains exact historical CP2 truth. Current repository image is 18.6 and has separate direct evidence below.

### 18.5 Historical Windows GUI connectivity

Verified first-workstation DBeaver connection:

```text
Host      127.0.0.1
Port      5432
Database  dante
User      postgres
Password  contents of the ignored workstation-local secret
```

Direct query:

```sql
SELECT current_database(), current_user, version();
```

First workstation observed PostgreSQL **18.4**. That observation proves the historical Windows → loopback → Docker boundary; it is not a claim that the current image remains 18.4.

## 19. Current PostgreSQL 18.6 direct evidence

The CP6 maintenance refresh changed only the PostgreSQL 18 patch-level envelope and preserved the CP3 persistence contract.

GitHub Actions directly ran:

```text
Backend CI run                    32568664940
workflow event                    workflow_dispatch
executed HEAD                     ec3dc795b5e044daa3a77723c94a1b4b5b92865c

PostgreSQL base                   18.6-trixie
PostGIS                           3.6.4 PASS
pgvector                          0.8.6 PASS

Backend Quality                   SUCCESS
Ruff format/lint                  PASS
mypy strict                       PASS
fast pytest                       32 / 32 PASS
wheel + sdist                     PASS

Backend PostgreSQL                SUCCESS
PostgreSQL pytest                 18 / 18 PASS
Alembic fresh → head              PASS
Alembic head/base/head            PASS
Alembic no-drift check            PASS
owner/migrator/runtime privileges PASS
runtime/search_path               PASS
stale connection recovery         PASS
DB outage/readiness recovery      PASS
transaction commit/rollback       PASS
savepoint behavior                PASS

Backend CI Gate                   SUCCESS
complete current test corpus      50 / 50 covered across two mandatory lanes
```

This is **DIRECT REMOTE QA PASS for the PostgreSQL 18.6 technical foundation regression**. It is not a business-semantic HG/PSV PASS.

PostgreSQL 18.6 release-note review result:

```text
PASS / NO CURRENT POST-UPGRADE ACTION
```

Current DANTE does not use a custom logical-decoding output plugin, `pgcrypto`, business GIN index, `btree_gist` or `ltree` object requiring an 18.6-specific cleanup action. When PowerSync/logical replication becomes active, review `output_plugin_libraries` and all then-current PostgreSQL maintenance requirements.

## 20. Current repository/workstream checkpoint

Historical 2026-08-20 workstation snapshot:

```text
Working branch                     feature/backend-scaffold
backend CP1                        PASS
backend CP2 PostgreSQL 18.4        CLOSED / DIRECT QA PASS
backend CP3                        NEXT / NOT STARTED at that moment
```

That is phase-time evidence only.

Current repository truth:

```text
Repository                         MattiaRubino/dante
Current backend branch             feature/logical-postgresql
Protected main                     contains CP1–CP5 via merged PR #24
CP1–CP5                            CLOSED / INTEGRATED / DIRECT QA PASS
CP6-00                             COMPLETE
CP6-01                             CLOSED / GATE 01 PASS
CP6-02                             CLOSED / GATE 02 PASS
CP6-03                             NEXT / NOT STARTED
PostgreSQL architecture            major 18
Physical/CP2/CP3 exact patch       18.4 historical
current PostgreSQL patch           18.6
18.6 technical regression          DIRECT REMOTE QA PASS
business persistence schema        NOT IMPLEMENTED
Vertical #1 implementation         POST-CP6 / NOT STARTED
```

## 21. Resume rule

When continuing on a new machine or after interruption:

1. verify WSL/Docker/uv/Python fundamentals from the relevant preceding sections;
2. verify repository remote and fetch current protected `main` plus the explicitly active bounded branch;
3. read `README.md`, `docs/PROJECT-STATUS.md`, `docs/ROADMAP.md` and the active workstream before any write;
4. preserve CP1/CP2/CP3/CP5 historical evidence exactly rather than rewriting old version numbers;
5. treat the current repository-owned PostgreSQL image as `dante-postgres-local:18.6` unless newer gated repository truth supersedes it;
6. use `uv run pytest -m postgres` for the current real PostgreSQL acceptance boundary;
7. never infer business schema, HG/PSV, recovery or production PASS from technical infrastructure evidence;
8. for CP6, current durable authority is `docs/workstreams/logical-postgresql.md`;
9. treat CP6-02 as CLOSED / GATE 02 PASS and consume its closure record plus closed Constitution;
10. current CP6 resume point is CP6-03 read/research/design-first;
11. Vertical #1 implementation begins only after whole CP6 closure;
12. before any repository write, follow the exact Git write gate for the active branch/workstream.

#!/usr/bin/env python3
"""Run real-stack Playwright on a dynamically selected private HTTPS port."""
from __future__ import annotations

import os
import socket
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    env = {**os.environ, "DANTE_E2E_WEB_PORT": str(port)}
    print(f"DANTE_E2E_WEB_PORT={port}; isolated real-stack browser", flush=True)
    return subprocess.run(
        ["pnpm", "exec", "playwright", "test", "--config", "playwright.auth.config.ts"],
        cwd=ROOT / "apps/web", env=env, check=False,
    ).returncode

if __name__ == "__main__":
    raise SystemExit(main())

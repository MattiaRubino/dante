from __future__ import annotations

from pathlib import Path

from materialize_m05_email_phase_a import (
    EXPECTED_BRANCH,
    EXPECTED_HASHES,
    patch_auth_settings,
    patch_lifecycle,
    patch_lifecycle_runtime,
    patch_lifespan,
    patch_multi_lifecycle,
    patch_pyproject,
    run,
)


def validate_repo(root: Path) -> None:
    branch = run("git", "-C", str(root), "branch", "--show-current")
    if branch != EXPECTED_BRANCH:
        raise RuntimeError(f"expected branch {EXPECTED_BRANCH}, found {branch!r}")
    status = run("git", "-C", str(root), "status", "--porcelain")
    if status:
        raise RuntimeError("worktree must be clean before materialization")
    for relative, expected in EXPECTED_HASHES.items():
        actual = run("git", "-C", str(root), "hash-object", relative)
        if actual != expected:
            raise RuntimeError(f"unexpected blob for {relative}: {actual} != {expected}")


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    validate_repo(root)
    patch_auth_settings(root / "apps/backend/src/dante/platform/config/auth.py")
    patch_lifecycle(root / "apps/backend/src/dante/auth/lifecycle.py")
    patch_multi_lifecycle(root / "apps/backend/src/dante/auth/authenticator_lifecycle.py")
    patch_lifecycle_runtime(root / "apps/backend/src/dante/auth/lifecycle_runtime.py")
    patch_lifespan(root / "apps/backend/src/dante/bootstrap/lifespan.py")
    patch_pyproject(root / "apps/backend/pyproject.toml")
    print("M05 Email Platform Phase A materialized successfully.")
    print("No commit was created. Review git diff before any commit.")


if __name__ == "__main__":
    main()

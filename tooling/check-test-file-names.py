#!/usr/bin/env python3
"""Reject milestone identifiers in executable test filenames."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEST_ROOTS = (
    ROOT / "apps/backend/tests",
    ROOT / "apps/web/src",
    ROOT / "apps/web/e2e",
    ROOT / "apps/web/tests-browser",
    ROOT / "packages",
    ROOT / "tooling/ai-evals/tests",
    ROOT / "tooling/observability/tests",
)
STAGE = re.compile(r"(?:^|[-_])(?:b\d{2}|cp\d+|m\d+|u\d+)(?=[-_.]|$)", re.I)
WEB_TEST = re.compile(r"\.(?:test|spec)\.[cm]?[jt]sx?$")


def is_test(path: Path) -> bool:
    return (path.suffix == ".py" and path.name.startswith("test_")) or bool(
        WEB_TEST.search(path.name)
    )


def main() -> int:
    files = sorted(
        path
        for root in TEST_ROOTS
        for path in root.rglob("*")
        if path.is_file() and is_test(path)
    )
    invalid = [path.relative_to(ROOT) for path in files if STAGE.search(path.name)]
    if invalid:
        print("Test filenames must describe behavior, not development milestones:")
        for path in invalid:
            print(f"  {path}")
        return 1
    print(f"PASS: {len(files)} test filenames have no development-stage identifiers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Guard DANTE test registration, cross-test imports and rename references.

This is a structural check, not proof that assertions match product semantics.
"""
from __future__ import annotations

import ast
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/development/test-case-registry.json"
RENAMES = ROOT / "docs/development/test-file-rename-map-2026-10-12.csv"

def discover() -> set[str]:
    found: set[str] = set()
    roots = {
        "apps/backend/tests": ("test_*.py",),
        "apps/web/src": ("*.test.ts", "*.test.tsx"),
        "apps/web/e2e": ("*.spec.ts", "*.spec.tsx"),
        "apps/web/tests-browser": ("*.spec.ts", "*.spec.tsx"),
        "apps/mobile": ("*.test.ts", "*.test.tsx"),
        "packages": ("*.test.ts", "*.test.tsx"),
        "tooling/ai-evals/tests": ("test_*.py",),
        "tooling/observability/tests": ("test_*.py",),
    }
    for folder, patterns in roots.items():
        base = ROOT / folder
        if base.is_dir():
            for pattern in patterns:
                found.update(
                    path.relative_to(ROOT).as_posix()
                    for path in base.rglob(pattern)
                    if "node_modules" not in path.parts
                )
    for name in (
        "tests/prototypes/frontend-preprod-contracts.py",
        "tests/prototypes/world-focus-preprod-contracts.py",
    ):
        if (ROOT / name).is_file():
            found.add(name)
    return found

def main() -> int:
    errors: list[str] = []
    if not REGISTRY.is_file() or not RENAMES.is_file():
        print("FAIL: Missing test registry or rename map")
        return 1
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    records = registry["tests"]
    known = [item["path"] for item in records]
    actual = discover()
    registered = set(known)
    duplicates = sorted(path for path, n in Counter(known).items() if n > 1)
    if duplicates:
        errors.append("Duplicate registry paths: " + ", ".join(duplicates[:20]))
    if actual - registered:
        errors.append("Unregistered test files: " + ", ".join(sorted(actual - registered)[:20]))
    if registered - actual:
        errors.append("Registry files missing in worktree: " + ", ".join(sorted(registered - actual)[:20]))
    allowed_unreviewed = set(registry["grandfathered_unreviewed_paths"])
    contracts = registry["contracts"]
    for item in records:
        path = item["path"]
        if item.get("contract_id") not in contracts:
            errors.append(f"Unknown contract for {path}")
        status = item.get("status")
        if status not in {"UNREVIEWED", "QUALIFIED", "DEPRECATED_PENDING_REPLACEMENT"}:
            errors.append(f"Invalid review status for {path}: {status}")
        if status == "UNREVIEWED" and path not in allowed_unreviewed:
            errors.append(f"New test cannot be unreviewed: {path}")
        if status == "QUALIFIED" and (
            len(item.get("purpose", "").strip()) < 25
            or len(item.get("invariant", "").strip()) < 25
        ):
            errors.append(f"Qualified test has incomplete purpose/invariant: {path}")
    with RENAMES.open(encoding="utf-8", newline="") as file:
        renames = list(csv.DictReader(file))
    legacy_modules = {
        row["old_path"].removeprefix("apps/backend/").removesuffix(".py").replace("/", "."):
        row["new_path"].removeprefix("apps/backend/").removesuffix(".py").replace("/", ".")
        for row in renames
        if row["old_path"].startswith("apps/backend/tests/") and row["old_path"].endswith(".py")
    }
    for file in sorted((ROOT / "apps/backend/tests").rglob("*.py")):
        body = file.read_text(encoding="utf-8")
        path = file.relative_to(ROOT)
        try:
            tree = ast.parse(body, filename=str(path))
        except SyntaxError as exc:
            errors.append(f"Python syntax invalid {path}: {exc}")
            continue
        imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
            elif isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            elif isinstance(node, ast.Assign):
                if any(isinstance(target, ast.Name) and target.id == "pytest_plugins" for target in node.targets):
                    try:
                        value = ast.literal_eval(node.value)
                        imports.update([value] if isinstance(value, str) else value)
                    except (TypeError, ValueError):
                        errors.append(f"Nonliteral pytest_plugins: {path}:{node.lineno}")
        for item in imports:
            if item in legacy_modules:
                errors.append(f"Stale renamed module {item} in {path}; now {legacy_modules[item]}")
            if item.startswith("tests.") and (".test_" in item or ".support." in item):
                target = ROOT / "apps/backend" / (item.replace(".", "/") + ".py")
                if not target.is_file():
                    errors.append(f"Broken cross-test import/plugin {item} in {path}")
        if "tests.integration.temporal.b05_legacy_test_support" in body:
            errors.append(f"Deprecated support import in {path}")
    config = (ROOT / "apps/backend/pyproject.toml").read_text(encoding="utf-8")
    for old, new in legacy_modules.items():
        stem = old.rsplit(".", 1)[-1]
        if re.search(r'(?<!\w)["\'](?:\*\.)?' + re.escape(stem) + r'["\']', config):
            errors.append(f"Stale mypy override {stem}; new module {new}")
    for script in (ROOT / "tooling").rglob("*.sh"):
        body = script.read_text(encoding="utf-8")
        for row in renames:
            if row["old_path"] in body:
                errors.append(f"Old test path {row['old_path']} in {script.relative_to(ROOT)}")
    old_support = ROOT / "apps/backend/tests/integration/temporal/b05_legacy_test_support.py"
    if old_support.exists():
        errors.append("Deprecated phase-named test support helper remains")
    print(f"REGISTERED={len(records)} DISCOVERED={len(actual)} "
          f"UNREVIEWED={sum(item['status'] == 'UNREVIEWED' for item in records)}")
    if errors:
        for issue in errors:
            print("FAIL: " + issue)
        return 1
    print("PASS: registry, cross-test imports/plugins and executable rename references structurally consistent")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

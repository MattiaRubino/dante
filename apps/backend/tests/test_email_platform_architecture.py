"""Architecture guardrails for the shared DANTE Email Platform package."""

from __future__ import annotations

import ast
from pathlib import Path

_PLATFORM_EMAIL_ROOT = Path(__file__).resolve().parents[1] / "src" / "dante" / "platform" / "email"


def test_shared_email_platform_does_not_import_access_auth() -> None:
    """Shared delivery infrastructure must never acquire a back-dependency on Access/Auth."""
    violations: list[str] = []
    for path in sorted(_PLATFORM_EMAIL_ROOT.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported = [node.module or ""]
            else:
                continue
            for module in imported:
                if module == "dante.auth" or module.startswith("dante.auth."):
                    violations.append(f"{path.name}:{node.lineno}:{module}")

    assert violations == []

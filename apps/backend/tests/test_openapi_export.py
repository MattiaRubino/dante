from __future__ import annotations

import json
from pathlib import Path

from dante.bootstrap.openapi_export import openapi_document


def test_committed_openapi_snapshot_matches_governed_export() -> None:
    """Fail CI when backend contract changes without regenerating the client source."""
    repo_root = Path(__file__).resolve().parents[3]
    snapshot_path = (
        repo_root / "packages" / "api-client" / "openapi" / "dante-v1.openapi.json"
    )

    committed = json.loads(snapshot_path.read_text(encoding="utf-8"))

    assert committed == openapi_document()

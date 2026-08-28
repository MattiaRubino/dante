"""Deterministic offline OpenAPI export for governed first-party client generation."""

from __future__ import annotations

import argparse
import json
from base64 import urlsafe_b64encode
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from pydantic import SecretStr

from dante.bootstrap.app import create_app
from dante.platform.config.auth import AuthSettings
from dante.platform.config.database import DatabaseSettings
from dante.platform.config.settings import Environment, Settings

_EXPORT_PEPPER_KEY_ID = "openapi-v1"


def _secret(raw: bytes) -> str:
    return urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _export_settings() -> Settings:
    """Build synthetic validated settings without live services or production secrets."""
    return Settings(
        env=Environment.LOCAL,
        release_sha="openapi",
        build_id="openapi",
        debug=False,
        database=DatabaseSettings(
            host="127.0.0.1",
            name="dante_openapi",
            user="dante_runtime",
            password=SecretStr("openapi-export-does-not-connect"),
        ),
        auth=AuthSettings(
            canonical_web_origin="https://dante.test",
            password_current_pepper_key_id=_EXPORT_PEPPER_KEY_ID,
            password_peppers={
                _EXPORT_PEPPER_KEY_ID: SecretStr(_secret(b"p" * 32)),
            },
            csrf_key=SecretStr(_secret(b"c" * 32)),
            kdf_max_concurrency=1,
            signin_rate_capacity=10,
            signin_rate_window_seconds=60.0,
        ),
    )


def openapi_document() -> dict[str, Any]:
    """Return the product OpenAPI document without running FastAPI lifespan."""
    return create_app(_export_settings()).openapi()


def render_openapi() -> str:
    """Render stable JSON ordering for reviewable generated-source diffs."""
    return json.dumps(
        openapi_document(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def write_openapi(target: Path) -> None:
    """Write one deterministic OpenAPI snapshot to the requested repository path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_openapi(), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path)
    args = parser.parse_args(argv)
    write_openapi(args.target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

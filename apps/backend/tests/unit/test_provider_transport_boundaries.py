"""Executable third-party transport confinement for approved runtime boundaries."""

import ast
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_SOURCE_ROOT = _BACKEND_ROOT / "src"
_DANTE_ROOT = _SOURCE_ROOT / "dante"
_ALLOWED_HTTPX2_PATHS = frozenset(
    {
        _DANTE_ROOT / "auth" / "passwords.py",
        _DANTE_ROOT / "auth" / "provider_runtime.py",
        _DANTE_ROOT / "auth" / "service.py",
        _DANTE_ROOT
        / "modules"
        / "intelligence"
        / "adapters"
        / "outbound"
        / "model"
        / "gemini_http.py",
    }
)


def test_httpx2_import_is_confined_to_approved_runtime_boundaries() -> None:
    violations: list[str] = []
    for path in sorted(_DANTE_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            imported: tuple[str, ...] = ()
            if isinstance(node, ast.Import):
                imported = tuple(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                imported = (node.module,)
            if (
                any(name == "httpx2" or name.startswith("httpx2.") for name in imported)
                and path not in _ALLOWED_HTTPX2_PATHS
            ):
                line_number = node.lineno if isinstance(node, (ast.Import, ast.ImportFrom)) else 0
                violations.append(f"{path.relative_to(_BACKEND_ROOT)}:{line_number}: {imported}")
    assert not violations, "\n".join(violations)

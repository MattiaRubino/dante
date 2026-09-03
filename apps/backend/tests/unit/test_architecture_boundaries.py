"""Executable architecture boundaries for DANTE backend capability modules."""

from __future__ import annotations

import ast
import re
import tomllib
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import cast

_BACKEND_ROOT = Path(__file__).resolve().parents[2]
_SOURCE_ROOT = _BACKEND_ROOT / "src"
_DANTE_ROOT = _SOURCE_ROOT / "dante"
_PYPROJECT = _BACKEND_ROOT / "pyproject.toml"

_SEARCH_ROOT = "dante.modules.search"
_INTELLIGENCE_ROOT = "dante.modules.intelligence"
_SEARCH_PUBLIC_SURFACES = (
    "dante.modules.search.public",
    "dante.modules.search.contracts",
)
_SEARCH_PERSISTENCE_ADAPTER = "dante.modules.search.adapters.outbound.persistence"
_INBOUND_ADAPTER_ROOTS = (
    "dante.modules.search.adapters.inbound",
    "dante.modules.intelligence.adapters.inbound",
)

_RUNTIME_DEPENDENCY_ALLOWLIST = frozenset(
    {
        "alembic",
        "fastapi",
        "psycopg",
        "pydantic",
        "pydantic-settings",
        "sqlalchemy",
        "uvicorn",
    }
)
_DEPENDENCY_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")
_FORBIDDEN_AI_TYPE_NAMES = frozenset({"EntityRef", "Repository", "UnitOfWork"})
_FORBIDDEN_AI_FIELD_NAMES = frozenset({"entity_id"})


@dataclass(frozen=True, slots=True)
class _ImportEdge:
    importer: str
    imported: str
    path: Path
    line: int


@dataclass(frozen=True, slots=True)
class _SemanticNameViolation:
    module: str
    name: str
    path: Path
    line: int


def _is_within(module: str, root: str) -> bool:
    return module == root or module.startswith(f"{root}.")


def _is_within_any(module: str, roots: tuple[str, ...]) -> bool:
    return any(_is_within(module, root) for root in roots)


def _module_and_package(path: Path) -> tuple[str, str]:
    relative = path.relative_to(_SOURCE_ROOT).with_suffix("")
    parts = list(relative.parts)
    if parts[-1] == "__init__":
        parts.pop()
        module = ".".join(parts)
        return module, module

    module = ".".join(parts)
    return module, ".".join(parts[:-1])


def _resolve_from_import(package: str, node: ast.ImportFrom) -> str:
    if node.level == 0:
        return node.module or ""

    package_parts = package.split(".") if package else []
    parents_to_remove = node.level - 1
    if parents_to_remove > len(package_parts):
        return ""

    resolved_parts = package_parts[: len(package_parts) - parents_to_remove]
    if node.module:
        resolved_parts.extend(node.module.split("."))
    return ".".join(resolved_parts)


@cache
def _import_edges() -> tuple[_ImportEdge, ...]:
    edges: list[_ImportEdge] = []

    for path in sorted(_DANTE_ROOT.rglob("*.py")):
        module, package = _module_and_package(path)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                edges.extend(
                    _ImportEdge(
                        importer=module,
                        imported=alias.name,
                        path=path,
                        line=node.lineno,
                    )
                    for alias in node.names
                )
                continue

            if isinstance(node, ast.ImportFrom):
                base = _resolve_from_import(package, node)
                for alias in node.names:
                    imported = (
                        base if alias.name == "*" else ".".join(filter(None, (base, alias.name)))
                    )
                    if imported:
                        edges.append(
                            _ImportEdge(
                                importer=module,
                                imported=imported,
                                path=path,
                                line=node.lineno,
                            )
                        )

    return tuple(edges)


def _forbidden_imports(
    *,
    importer_roots: tuple[str, ...],
    imported_roots: tuple[str, ...],
    allowed_importer_roots: tuple[str, ...] = (),
    allowed_imported_roots: tuple[str, ...] = (),
) -> list[_ImportEdge]:
    return [
        edge
        for edge in _import_edges()
        if _is_within_any(edge.importer, importer_roots)
        and _is_within_any(edge.imported, imported_roots)
        and not _is_within_any(edge.importer, allowed_importer_roots)
        and not _is_within_any(edge.imported, allowed_imported_roots)
    ]


def _format_edges(edges: list[_ImportEdge]) -> str:
    return "\n".join(
        f"{edge.path.relative_to(_BACKEND_ROOT)}:{edge.line}: {edge.importer} -> {edge.imported}"
        for edge in edges
    )


@cache
def _source_modules() -> frozenset[str]:
    return frozenset(_module_and_package(path)[0] for path in _DANTE_ROOT.rglob("*.py"))


def _internal_target(imported: str) -> str | None:
    parts = imported.split(".")
    modules = _source_modules()
    for size in range(len(parts), 0, -1):
        candidate = ".".join(parts[:size])
        if candidate in modules:
            return candidate
    return None


@cache
def _internal_graph() -> dict[str, frozenset[str]]:
    mutable_graph: dict[str, set[str]] = {module: set() for module in _source_modules()}
    for edge in _import_edges():
        target = _internal_target(edge.imported)
        if target is not None:
            mutable_graph.setdefault(edge.importer, set()).add(target)
    return {module: frozenset(targets) for module, targets in mutable_graph.items()}


def _find_internal_paths(
    *,
    importer_root: str,
    forbidden_root: str,
    allowed_forbidden_roots: tuple[str, ...] = (),
) -> list[tuple[str, ...]]:
    graph = _internal_graph()
    violations: list[tuple[str, ...]] = []

    for start in sorted(module for module in graph if _is_within(module, importer_root)):
        queue: list[tuple[str, tuple[str, ...]]] = [(start, (start,))]
        visited = {start}

        while queue:
            current, path = queue.pop(0)
            for target in sorted(graph.get(current, ())):
                if target in visited:
                    continue

                next_path = (*path, target)
                if _is_within(target, forbidden_root) and not _is_within_any(
                    target, allowed_forbidden_roots
                ):
                    violations.append(next_path)
                    break

                visited.add(target)
                queue.append((target, next_path))

    return violations


def _format_paths(paths: list[tuple[str, ...]]) -> str:
    return "\n".join(" -> ".join(path) for path in paths)


@cache
def _runtime_dependency_names() -> frozenset[str]:
    with _PYPROJECT.open("rb") as stream:
        document = tomllib.load(stream)

    project = cast(dict[str, object], document["project"])
    dependencies = cast(list[str], project["dependencies"])

    names: set[str] = set()
    for dependency in dependencies:
        match = _DEPENDENCY_NAME.match(dependency)
        if match is None:
            raise AssertionError(f"Unsupported runtime dependency specifier: {dependency!r}")
        names.add(match.group(0).lower().replace("_", "-"))

    return frozenset(names)


def _semantic_name(
    module: str,
    path: Path,
    name: str,
    line: int,
) -> _SemanticNameViolation | None:
    if name not in _FORBIDDEN_AI_TYPE_NAMES and name not in _FORBIDDEN_AI_FIELD_NAMES:
        return None
    return _SemanticNameViolation(module=module, name=name, path=path, line=line)


@cache
def _semantic_name_violations() -> tuple[_SemanticNameViolation, ...]:
    violations: list[_SemanticNameViolation] = []
    modules_root = _DANTE_ROOT / "modules"

    for path in sorted(modules_root.rglob("*.py")):
        module, _package = _module_and_package(path)
        if not _is_within_any(module, (_SEARCH_ROOT, _INTELLIGENCE_ROOT)):
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            candidates: tuple[tuple[str, int], ...] = ()
            if isinstance(node, ast.ClassDef):
                candidates = ((node.name, node.lineno),)
            elif isinstance(node, ast.arg):
                candidates = ((node.arg, node.lineno),)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                candidates = ((node.target.id, node.lineno),)
            elif isinstance(node, ast.Assign):
                candidates = tuple(
                    (target.id, node.lineno)
                    for target in node.targets
                    if isinstance(target, ast.Name)
                )
            elif isinstance(node, ast.TypeAlias):
                candidates = ((node.name.id, node.lineno),)

            for name, line in candidates:
                violation = _semantic_name(module, path, name, line)
                if violation is not None:
                    violations.append(violation)

    return tuple(violations)


def test_runtime_dependencies_remain_inside_the_pre_provider_allowlist() -> None:
    assert _runtime_dependency_names() == _RUNTIME_DEPENDENCY_ALLOWLIST


def test_search_never_imports_intelligence() -> None:
    violations = _forbidden_imports(
        importer_roots=(_SEARCH_ROOT,),
        imported_roots=(_INTELLIGENCE_ROOT,),
    )
    assert not violations, _format_edges(violations)


def test_search_has_no_indirect_dependency_path_to_intelligence() -> None:
    violations = _find_internal_paths(
        importer_root=_SEARCH_ROOT,
        forbidden_root=_INTELLIGENCE_ROOT,
    )
    assert not violations, _format_paths(violations)


def test_intelligence_consumes_search_only_through_its_public_surface() -> None:
    violations = _forbidden_imports(
        importer_roots=(_INTELLIGENCE_ROOT,),
        imported_roots=(_SEARCH_ROOT,),
        allowed_imported_roots=_SEARCH_PUBLIC_SURFACES,
    )
    assert not violations, _format_edges(violations)


def test_intelligence_has_no_indirect_dependency_path_to_private_search() -> None:
    violations = _find_internal_paths(
        importer_root=_INTELLIGENCE_ROOT,
        forbidden_root=_SEARCH_ROOT,
        allowed_forbidden_roots=_SEARCH_PUBLIC_SURFACES,
    )
    assert not violations, _format_paths(violations)


def test_intelligence_has_no_database_or_sqlalchemy_authority() -> None:
    violations = _forbidden_imports(
        importer_roots=(_INTELLIGENCE_ROOT,),
        imported_roots=("sqlalchemy", "dante.platform.database"),
    )
    assert not violations, _format_edges(violations)


def test_search_database_access_is_confined_to_its_persistence_adapter() -> None:
    violations = _forbidden_imports(
        importer_roots=(_SEARCH_ROOT,),
        imported_roots=("sqlalchemy", "dante.platform.database"),
        allowed_importer_roots=(_SEARCH_PERSISTENCE_ADAPTER,),
    )
    assert not violations, _format_edges(violations)


def test_fastapi_is_confined_to_inbound_adapters_inside_ai_capabilities() -> None:
    violations = _forbidden_imports(
        importer_roots=(_SEARCH_ROOT, _INTELLIGENCE_ROOT),
        imported_roots=("fastapi",),
        allowed_importer_roots=_INBOUND_ADAPTER_ROOTS,
    )
    assert not violations, _format_edges(violations)


def test_production_capability_modules_do_not_import_eval_tooling() -> None:
    violations = _forbidden_imports(
        importer_roots=(_SEARCH_ROOT, _INTELLIGENCE_ROOT),
        imported_roots=("tooling.ai_evals", "ai_evals"),
    )
    assert not violations, _format_edges(violations)


def test_ai_capabilities_do_not_introduce_forbidden_universal_abstractions() -> None:
    violations = list(_semantic_name_violations())
    rendered = "\n".join(
        f"{violation.path.relative_to(_BACKEND_ROOT)}:{violation.line}: "
        f"{violation.module}: forbidden semantic name {violation.name!r}"
        for violation in violations
    )
    assert not violations, rendered

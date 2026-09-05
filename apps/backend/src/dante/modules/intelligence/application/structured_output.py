"""Bounded provider-independent JSON-schema validation for ModelAccess outputs.

DANTE intentionally supports an explicit JSON-schema subset here rather than trusting a
provider's structured-output claim. Unsupported schema keywords fail before provider egress.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import cast

from dante.modules.intelligence.contracts.model_access import StructuredOutputContract

_SUPPORTED_KEYWORDS = frozenset(
    {
        "$schema",
        "type",
        "properties",
        "required",
        "additionalProperties",
        "items",
        "enum",
        "const",
        "description",
        "title",
        "minItems",
        "maxItems",
        "minimum",
        "maximum",
        "minLength",
        "maxLength",
        "pattern",
    }
)
_SUPPORTED_TYPES = frozenset({"object", "array", "string", "integer", "number", "boolean", "null"})


@dataclass(frozen=True, slots=True)
class StructuredOutputValidationError(ValueError):
    code: str
    path: str

    def __str__(self) -> str:
        return f"{self.code} at {self.path}"


def _schema_document(contract: StructuredOutputContract) -> dict[str, object]:
    loaded = json.loads(contract.schema_json)
    if not isinstance(loaded, dict):
        raise StructuredOutputValidationError("schema_root_not_object", "$")
    return cast(dict[str, object], loaded)


def _validate_schema_shape(schema: dict[str, object], *, path: str) -> None:
    unknown = set(schema) - _SUPPORTED_KEYWORDS
    if unknown:
        raise StructuredOutputValidationError(
            f"unsupported_schema_keyword:{sorted(unknown)[0]}", path
        )

    type_value = schema.get("type")
    types: tuple[str, ...]
    if type_value is not None:
        if isinstance(type_value, str):
            types = (type_value,)
        elif isinstance(type_value, list) and all(isinstance(item, str) for item in type_value):
            types = tuple(cast(list[str], type_value))
        else:
            raise StructuredOutputValidationError("invalid_schema_type", path)
        if (
            not types
            or len(types) != len(set(types))
            or any(item not in _SUPPORTED_TYPES for item in types)
        ):
            raise StructuredOutputValidationError("unsupported_schema_type", path)

    properties = schema.get("properties")
    if properties is not None:
        if not isinstance(properties, dict):
            raise StructuredOutputValidationError("properties_not_object", path)
        for name, child in properties.items():
            if not isinstance(name, str) or not name:
                raise StructuredOutputValidationError("invalid_property_name", path)
            if not isinstance(child, dict):
                raise StructuredOutputValidationError(
                    "property_schema_not_object", f"{path}.{name}"
                )
            _validate_schema_shape(cast(dict[str, object], child), path=f"{path}.{name}")

    required = schema.get("required")
    if required is not None:
        if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
            raise StructuredOutputValidationError("required_not_string_array", path)
        required_names = cast(list[str], required)
        if len(required_names) != len(set(required_names)):
            raise StructuredOutputValidationError("duplicate_required_property", path)

    additional = schema.get("additionalProperties")
    if additional is not None and not isinstance(additional, bool):
        raise StructuredOutputValidationError("additional_properties_not_boolean", path)

    items = schema.get("items")
    if items is not None:
        if not isinstance(items, dict):
            raise StructuredOutputValidationError("items_schema_not_object", path)
        _validate_schema_shape(cast(dict[str, object], items), path=f"{path}[]")

    for keyword in ("minItems", "maxItems", "minLength", "maxLength"):
        value = schema.get(keyword)
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, int) or value < 0
        ):
            raise StructuredOutputValidationError(f"invalid_{keyword}", path)

    for keyword in ("minimum", "maximum"):
        value = schema.get(keyword)
        if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
            raise StructuredOutputValidationError(f"invalid_{keyword}", path)

    pattern = schema.get("pattern")
    if pattern is not None:
        if not isinstance(pattern, str):
            raise StructuredOutputValidationError("pattern_not_string", path)
        try:
            re.compile(pattern)
        except re.error as exc:
            raise StructuredOutputValidationError("invalid_pattern", path) from exc


def validate_contract_schema(contract: StructuredOutputContract) -> None:
    """Fail before provider dispatch when DANTE cannot independently validate the contract."""
    _validate_schema_shape(_schema_document(contract), path="$")


def _matches_type(value: object, expected: str) -> bool:
    if expected == "null":
        return value is None
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "string":
        return isinstance(value, str)
    if expected == "array":
        return isinstance(value, list)
    if expected == "object":
        return isinstance(value, dict)
    return False


def _validate_value(value: object, schema: dict[str, object], *, path: str) -> None:
    type_value = schema.get("type")
    accepted_types: tuple[str, ...]
    if isinstance(type_value, str):
        accepted_types = (type_value,)
    elif isinstance(type_value, list):
        accepted_types = tuple(cast(list[str], type_value))
    else:
        accepted_types = ()
    if accepted_types and not any(_matches_type(value, item) for item in accepted_types):
        raise StructuredOutputValidationError("type_mismatch", path)

    enum_values = schema.get("enum")
    if enum_values is not None:
        if not isinstance(enum_values, list):
            raise StructuredOutputValidationError("enum_not_array", path)
        if value not in enum_values:
            raise StructuredOutputValidationError("enum_mismatch", path)
    if "const" in schema and value != schema["const"]:
        raise StructuredOutputValidationError("const_mismatch", path)

    if isinstance(value, dict):
        properties_raw = schema.get("properties", {})
        properties = (
            cast(dict[str, object], properties_raw) if isinstance(properties_raw, dict) else {}
        )
        required_raw = schema.get("required", [])
        required = cast(list[str], required_raw) if isinstance(required_raw, list) else []
        for name in required:
            if name not in value:
                raise StructuredOutputValidationError("required_property_missing", f"{path}.{name}")
        if schema.get("additionalProperties") is False:
            extra = set(value) - set(properties)
            if extra:
                raise StructuredOutputValidationError(
                    "additional_property_forbidden", f"{path}.{sorted(extra)[0]}"
                )
        for name, child_value in value.items():
            child_schema = properties.get(name)
            if isinstance(child_schema, dict):
                _validate_value(
                    child_value,
                    cast(dict[str, object], child_schema),
                    path=f"{path}.{name}",
                )

    if isinstance(value, list):
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if isinstance(min_items, int) and len(value) < min_items:
            raise StructuredOutputValidationError("min_items_violation", path)
        if isinstance(max_items, int) and len(value) > max_items:
            raise StructuredOutputValidationError("max_items_violation", path)
        items = schema.get("items")
        if isinstance(items, dict):
            child_schema = cast(dict[str, object], items)
            for index, child in enumerate(value):
                _validate_value(child, child_schema, path=f"{path}[{index}]")

    if isinstance(value, str):
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        pattern = schema.get("pattern")
        if isinstance(min_length, int) and len(value) < min_length:
            raise StructuredOutputValidationError("min_length_violation", path)
        if isinstance(max_length, int) and len(value) > max_length:
            raise StructuredOutputValidationError("max_length_violation", path)
        if isinstance(pattern, str) and re.search(pattern, value) is None:
            raise StructuredOutputValidationError("pattern_mismatch", path)

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            raise StructuredOutputValidationError("minimum_violation", path)
        if isinstance(maximum, (int, float)) and value > maximum:
            raise StructuredOutputValidationError("maximum_violation", path)


def validate_structured_output(contract: StructuredOutputContract, payload: str) -> None:
    """Validate finalized provider JSON against DANTE's accepted schema subset."""
    validate_contract_schema(contract)
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise StructuredOutputValidationError("invalid_json", "$") from exc
    _validate_value(value, _schema_document(contract), path="$")

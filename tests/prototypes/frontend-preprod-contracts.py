#!/usr/bin/env python3
"""Stdlib-only drift guard for DANTE frontend pre-production contracts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "prototypes" / "frontend" / "shared" / "contracts"
FIXTURES = ROOT / "prototypes" / "frontend" / "shared" / "fixtures"


def load(name: str, base: Path) -> dict:
    with (base / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_ids(items: list[dict], context: str) -> None:
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), f"duplicate ids in {context}"


def validate_projection(projection: dict, context: str) -> None:
    items = projection["items"]
    active_index = projection["activeIndex"]
    assert isinstance(items, list)
    if items:
        assert isinstance(active_index, int)
        assert 0 <= active_index < len(items)
    else:
        assert active_index is None, f"empty {context} requires null activeIndex"


def validate_vm(vm: dict, schema: dict, allowed_states: set[str]) -> None:
    assert vm["contractVersion"] == "0.2.0"
    assert vm["mode"] in {"home.stage.continuity", "home.stage.signals"}
    assert vm["status"] in allowed_states

    validate_projection(vm["continuity"], "continuity")
    validate_projection(vm["signals"], "signals")
    unique_ids(vm["continuity"]["items"], "continuity")
    unique_ids(vm["signals"]["items"], "signals")

    allowed_kinds = set(schema["$defs"]["visualization"]["properties"]["kind"]["enum"])
    for signal in vm["signals"]["items"]:
        assert signal["visualization"]["kind"] in allowed_kinds
        assert signal["provenance"]["sourceKind"] in {"mock", "backend", "derived"}
    for item in vm["continuity"]["items"]:
        assert item["provenance"]["sourceKind"] in {"mock", "backend", "derived"}
        assert item["label"] != "+", "ghost/add slots are not data items"


def main() -> None:
    contract = load("home-stage.contract.json", CONTRACTS)
    schema = load("home-stage.view-model.schema.json", CONTRACTS)
    matrix = load("home-responsive.matrix.json", CONTRACTS)
    fixture = load("home-stage.v0.json", FIXTURES)

    version = contract["contractVersion"]
    assert version == "0.2.0"
    assert version == schema["properties"]["contractVersion"]["const"]
    assert version == matrix["contractVersion"] == fixture["contractVersion"]

    modes = {entry["id"] for entry in contract["modes"]}
    assert modes == set(matrix["modes"]) == {"home.stage.continuity", "home.stage.signals"}

    signals = next(entry for entry in contract["modes"] if entry["id"] == "home.stage.signals")
    continuity = next(entry for entry in contract["modes"] if entry["id"] == "home.stage.continuity")
    assert signals["maxVisibleItems"] == matrix["modeRules"]["home.stage.signals"]["maxVisibleItems"] == 3
    assert continuity["targetVisibleItems"] == matrix["modeRules"]["home.stage.continuity"]["desktopTargetVisibleItems"] == 5

    expected_cases = len(matrix["viewportsPx"]) * len(matrix["aiStates"]) * len(matrix["modes"])
    assert matrix["viewportsPx"] == [1856, 1600, 1366, 1200, 1024, 901]
    assert matrix["expectedCartesianCases"] == expected_cases == 24

    allowed_states = set(contract["uiStates"])
    assert allowed_states == set(schema["properties"]["status"]["enum"])
    assert set(fixture["samples"]) == {"full", "partial", "empty"}
    for sample in fixture["samples"].values():
        validate_vm(sample, schema, allowed_states)

    assert len(fixture["samples"]["full"]["continuity"]["items"]) == 5
    assert len(fixture["samples"]["partial"]["continuity"]["items"]) == 3
    assert fixture["samples"]["empty"]["continuity"] == {"activeIndex": None, "items": []}
    assert fixture["samples"]["empty"]["signals"] == {"activeIndex": None, "items": []}

    assert contract["geometryOwnership"]["owner"] == "home.stage"
    assert contract["geometryOwnership"]["outerGeometryMayBeChangedByModes"] is False
    assert contract["homeRole"]["persistentAddAffordance"] is False
    assert contract["homeRole"]["configurationInHome"] is False
    assert contract["homeRole"]["partialRendersOnlyRealItems"] is True
    assert contract["homeRole"]["emptyStateMayOfferManagementEntry"] is True
    assert contract["managementBoundary"]["directCreateMutationFromStage"] is False
    assert "ADD_REQUEST" not in contract["events"]
    assert "OPEN_MANAGEMENT" in contract["events"]

    continuity_rules = matrix["modeRules"]["home.stage.continuity"]
    signals_rules = matrix["modeRules"]["home.stage.signals"]
    assert continuity_rules["ghostAddSlotsAllowed"] is False
    assert continuity_rules["persistentAddAffordanceAllowed"] is False
    assert signals_rules["persistentAddAffordanceAllowed"] is False
    assert contract["dataBoundary"]["componentMustNotCallHttpDirectly"] is True
    assert contract["dataBoundary"]["componentMustNotConsumeOrmOrDatabaseShape"] is True

    print("frontend pre-production contracts: PASS")
    print(f"contractVersion={version}")
    print(f"responsiveCases={expected_cases}")
    print("signalsMaxVisible=3")
    print("continuityTargetVisible=5")
    print("persistentAdd=false")
    print("partialRealItemsOnly=true")
    print("emptyManagementEntry=true")


if __name__ == "__main__":
    main()

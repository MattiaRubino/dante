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


def validate_whole_home_structure() -> tuple[str, int]:
    structure = load("home-structure.contract.json", CONTRACTS)
    shell_matrix = load("home-shell-responsive.matrix.json", CONTRACTS)

    version = structure["contractVersion"]
    assert version == "1.0.0"
    assert shell_matrix["contractVersion"] == version
    assert structure["status"] == "frozen"

    change_control = structure["changeControl"]
    assert change_control["explicitUserApprovalRequiredForObservableStructuralChange"] is True
    assert change_control["implementationRefactorAllowedWhenContractEquivalent"] is True
    assert change_control["regressionGuardsMayBeWeakenedToAcceptAccidentalDrift"] is False

    app_shell = structure["appShellBoundary"]
    assert app_shell == {
        "owner": "app-shell",
        "insideHomeFeature": False,
        "homeMayRenderOwnGlobalTopbar": False,
    }

    required_regions = {entry["id"] for entry in structure["regions"] if entry["required"]}
    assert required_regions == {
        "home.shell",
        "home.dayContext",
        "home.aiSurface",
        "home.orientation",
        "home.stage",
        "home.timeline",
        "home.contextRail",
    }
    unique_ids(structure["regions"], "whole-home regions")

    parents = {entry["id"]: entry["parent"] for entry in structure["regions"]}
    assert parents["home.shell"] == "app-shell.routeOutlet"
    assert parents["home.dayContext"] == "home.hero"
    assert parents["home.aiSurface"] == "home.heroBody"
    assert parents["home.orientation"] == "home.upperWorkspace"
    assert parents["home.stage"] == "home.upperWorkspace"
    assert parents["home.timeline"] == "home.todayWorkspace"
    assert parents["home.contextRail"] == "home.todayWorkspace"

    composition = structure["composition"]
    assert composition["home.hero"] == ["home.dayContext", "home.heroBody"]
    assert composition["home.heroBody"] == ["home.aiSurface", "home.upperWorkspace"]
    assert composition["home.upperWorkspace"] == ["home.orientation", "home.stage"]
    assert composition["home.todayWorkspace"] == ["home.timeline", "home.contextRail"]

    assert structure["orientationResponsibilities"] == ["now-next", "highlight", "for-you"]
    assert structure["contextRailResponsibilities"] == {
        "captureDirection": "user-to-dante",
        "resolutionDirection": "dante-to-user",
        "independentFloatingHomeRegionsAllowed": False,
    }

    state = structure["stateInvariants"]
    assert state["aiCollapseOwner"] == "home.shell"
    assert state["aiRoundTripMustBeGeometryReversible"] is True
    assert state["stageModeMayChangeStageOuterGeometry"] is False
    assert state["timelineExpansionMayConsumeContextRailWidthOnWide"] is True
    assert state["timelineExpansionMayReauthorHeroGeometry"] is False
    assert state["worldFocusEntryIsRouteTransitionNotHomeOverlay"] is True

    geometry = structure["geometry"]
    assert geometry["macroBreakpointsPx"] == {
        "wideMin": 1121,
        "compressedMin": 901,
        "compressedMax": 1120,
        "compactMax": 900,
    }
    assert geometry["acceptedMacroAnchorsPx"] == {
        "contextRailNominalWidth": 306,
        "todayNominalGap": 16,
        "defaultOuterInset": 34,
        "compressedOuterInset": 24,
        "desktopHeroBaselineHeight": 650,
    }
    assert geometry["secondaryTuningBreakpointsPx"] == [1240, 1180, 1100, 980]
    assert geometry["secondaryTuningMayCreateNewMacroComposition"] is False

    responsive_modes = {entry["id"]: entry for entry in structure["responsiveModes"]}
    assert set(responsive_modes) == {"H0-WIDE", "H0-COMPRESSED", "H0-COMPACT"}
    assert responsive_modes["H0-WIDE"]["minWidthPx"] == 1121
    assert responsive_modes["H0-COMPRESSED"]["minWidthPx"] == 901
    assert responsive_modes["H0-COMPRESSED"]["maxWidthPx"] == 1120
    assert responsive_modes["H0-COMPACT"]["maxWidthPx"] == 900

    matrix_modes = shell_matrix["modes"]
    for mode_id, mode in responsive_modes.items():
        matrix_mode = matrix_modes[mode_id]
        for key in ("minWidthPx", "maxWidthPx"):
            if key in mode:
                assert matrix_mode[key] == mode[key]
        assert matrix_mode["contextRailVisible"] == mode["contextRailVisible"]

    assert shell_matrix["pressureViewportsPx"] == [
        1856,
        1600,
        1366,
        1200,
        1121,
        1120,
        1024,
        901,
        900,
        760,
        390,
    ]
    assert shell_matrix["representativeAiRoundTripViewportsPx"] == [1856, 1366, 1024, 901]
    assert shell_matrix["representativeTimelineExpansionViewportsPx"] == [1856, 1366, 1121]
    assert set(shell_matrix["requiredRegions"]) == {
        "shell",
        "ai-surface",
        "orientation",
        "central-stage",
        "timeline",
        "context-rail",
    }

    forbidden = set(structure["forbiddenDrift"])
    assert {
        "home-owned-global-topbar",
        "required-region-removed",
        "context-rail-reparented-under-timeline",
        "orientation-reparented-under-stage",
        "stage-mode-changes-stage-outer-bounds",
        "timeline-expansion-reauthors-hero",
        "ai-round-trip-leaves-permanent-macro-drift",
        "undocumented-fourth-responsive-macro-mode",
        "stage-add-control-changes-home-outer-geometry",
        "world-focus-mounted-as-home-structural-overlay",
        "unexpected-horizontal-page-overflow",
    } <= forbidden

    return version, len(shell_matrix["pressureViewportsPx"])


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

    home_structure_version, home_pressure_widths = validate_whole_home_structure()

    print("frontend pre-production contracts: PASS")
    print(f"stageContractVersion={version}")
    print(f"stageResponsiveCases={expected_cases}")
    print(f"homeStructureContractVersion={home_structure_version}")
    print(f"homePressureWidths={home_pressure_widths}")
    print("signalsMaxVisible=3")
    print("continuityTargetVisible=5")
    print("persistentAdd=false")
    print("partialRealItemsOnly=true")
    print("emptyManagementEntry=true")
    print("wholeHomeStructureFrozen=true")


if __name__ == "__main__":
    main()

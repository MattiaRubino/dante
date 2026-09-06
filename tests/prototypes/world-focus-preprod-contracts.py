#!/usr/bin/env python3
"""Stdlib-only drift guard for the frozen World Focus structural contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACTS = ROOT / "prototypes" / "frontend" / "shared" / "contracts"


def load(name: str) -> dict:
    with (CONTRACTS / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def unique_ids(items: list[dict], context: str) -> None:
    ids = [item["id"] for item in items]
    assert len(ids) == len(set(ids)), f"duplicate ids in {context}"


def main() -> None:
    structure = load("world-focus-structure.contract.json")
    matrix = load("world-focus-shell-responsive.matrix.json")

    version = structure["contractVersion"]
    assert version == "1.0.0"
    assert matrix["contractVersion"] == version
    assert structure["status"] == "frozen"

    change_control = structure["changeControl"]
    assert change_control == {
        "explicitUserApprovalRequiredForObservableStructuralChange": True,
        "implementationRefactorAllowedWhenContractEquivalent": True,
        "regressionGuardsMayBeWeakenedToAcceptAccidentalDrift": False,
    }

    assert structure["appShellBoundary"] == {
        "owner": "app-shell",
        "insideWorldFocusFeature": False,
        "worldFocusMayRenderOwnGlobalTopbar": False,
        "worldFocusMayModifyGlobalTopbar": False,
    }

    route = structure["routeBoundary"]
    assert route["pathPattern"] == "/worlds/:worldId"
    assert route["worldFocusIsDedicatedRouteSurface"] is True
    assert route["worldFocusMayBeHomeStructuralOverlay"] is False
    assert route["homeMayRemainVisibleAsWorldFocusBackground"] is False
    assert route["entryAnimationRequiredForNavigation"] is False

    unique_ids(structure["regions"], "World Focus regions")
    required_regions = {entry["id"] for entry in structure["regions"] if entry["required"]}
    assert required_regions == {
        "worldFocus.shell",
        "worldFocus.visualFrame",
        "worldFocus.workspace",
        "worldFocus.shellControls",
    }
    parents = {entry["id"]: entry["parent"] for entry in structure["regions"]}
    assert parents == {
        "worldFocus.shell": "app-shell.routeOutlet",
        "worldFocus.visualFrame": "worldFocus.shell",
        "worldFocus.workspace": "worldFocus.shell",
        "worldFocus.shellControls": "worldFocus.shell",
    }

    assert structure["composition"]["worldFocus.shell"] == [
        "worldFocus.visualFrame",
        "worldFocus.workspace",
        "worldFocus.shellControls",
    ]

    visual_frame = structure["geometry"]["visualFrame"]
    assert structure["geometry"]["geometryVersion"] == "wf-g3"
    assert visual_frame["primitive"] == "three-concentric-ellipses"
    assert visual_frame["center"] == {"cx": "50%", "cy": "50%"}
    assert visual_frame["ellipses"] == {
        "outer": {"rx": "52.25%", "ry": "90%"},
        "origin": {"rx": "50%", "ry": "87%"},
        "inner": {"rx": "47.75%", "ry": "84%"},
    }
    assert visual_frame["originTouchesLateralRouteEdgesAtMidHeight"] is True

    workspace = structure["geometry"]["workspace"]
    assert workspace == {
        "standardInlineInset": "clamp(136px, 14vw, 224px)",
        "compactInlineInset": "clamp(76px, 18vw, 112px)",
        "standardBlockInset": "clamp(32px, 5vh, 64px)",
        "compactBlockInset": "20px",
        "compactTuningBreakpointMaxPx": 720,
    }

    state = structure["stateInvariants"]
    assert state["visualFrameMayOwnWorkspaceLayout"] is False
    assert state["visualFrameMayClipWorkspace"] is False
    assert state["workspaceMayBeClippedToEllipse"] is False
    assert state["shellControlsMayReauthorWorkspaceGeometry"] is False
    assert state["overlayLayerMayParticipateInMacroGeometry"] is False
    assert state["worldSpecificSkinMayChangeStructuralGeometry"] is False
    assert state["worldSpecificContentMayChangeStructuralGeometry"] is False
    assert state["entryAnimationMayChangeStableEndGeometry"] is False

    modes = {entry["id"]: entry for entry in structure["responsiveModes"]}
    assert set(modes) == {"WF0-STANDARD", "WF0-COMPACT"}
    assert modes["WF0-STANDARD"]["minWidthPx"] == 721
    assert modes["WF0-COMPACT"]["maxWidthPx"] == 720
    assert modes["WF0-STANDARD"]["composition"] == modes["WF0-COMPACT"]["composition"]

    assert matrix["pressureViewportsPx"] == [
        1856,
        1600,
        1366,
        1200,
        1024,
        901,
        900,
        760,
        721,
        720,
        719,
        390,
    ]
    assert matrix["representativeGeometryViewportsPx"] == [
        1856,
        1600,
        1366,
        1024,
        901,
        721,
        720,
        390,
    ]

    required_matrix_regions = {
        "worldFocus.shell",
        "worldFocus.visualFrame",
        "worldFocus.workspace",
        "worldFocus.shellControls",
    }
    for mode_id, mode in modes.items():
        matrix_mode = matrix["modes"][mode_id]
        for key in ("minWidthPx", "maxWidthPx"):
            if key in mode:
                assert matrix_mode[key] == mode[key]
        assert set(matrix_mode["requiredRegions"]) == required_matrix_regions
        assert matrix_mode["macroComposition"] == "unchanged"

    forbidden = set(structure["forbiddenDrift"])
    assert {
        "world-focus-mounted-as-home-structural-overlay",
        "world-focus-owned-global-topbar",
        "global-topbar-modified-by-world-focus",
        "visual-frame-becomes-layout-container",
        "workspace-clipped-to-ellipse",
        "workspace-replaced-by-circular-layout",
        "shell-control-changes-workspace-geometry",
        "world-specific-skin-changes-macro-geometry",
        "world-specific-content-changes-macro-geometry",
        "overlay-layer-participates-in-macro-layout",
        "undocumented-responsive-macro-mode",
        "unexpected-horizontal-page-overflow",
    } <= forbidden

    print("world focus pre-production contracts: PASS")
    print(f"worldFocusStructureContractVersion={version}")
    print("worldFocusGeometryVersion=wf-g3")
    print(f"worldFocusPressureWidths={len(matrix['pressureViewportsPx'])}")
    print("worldFocusStructureFrozen=true")


if __name__ == "__main__":
    main()

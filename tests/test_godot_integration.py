"""Tests for DoubleHelix.Go: Godot Engine Integration, Custom Editor Suite & AI Gaming Agents.

Verifies:
1. Godot engine binary discovery, 4.7.x Mono/.NET runtime verification.
2. Business and licensing injection (EULA, Commercial Terms, Invariant SHA256 stamps).
3. arkade.new-world-arkitech.dev remote asset loader manifests and PBR shader mappings.
4. Autonomous Gaming Agent headless CLI execution (status, room generation, scene validation).
5. Project scaffolding and export configuration.
"""

import json
from pathlib import Path
import pytest

from doublehelix.godot.manager import GodotEngineManager
from doublehelix.godot.licensing import GodotLicenseInjector
from doublehelix.godot.asset_loader import GodotAssetConfig
from doublehelix.godot.agent_client import GodotAgentClient
from doublehelix.godot.scaffold import GodotProjectScaffold


@pytest.fixture(scope="module")
def engine_manager():
    return GodotEngineManager()


@pytest.fixture(scope="module")
def agent_client(engine_manager):
    return GodotAgentClient(engine_manager=engine_manager)


@pytest.fixture(scope="module")
def template_project_path():
    path = Path(r"C:\Users\evlga\Desktop\DoubleHelix Neural Agent Engine\DoubleHelix.Go\DoubleHelix_Tactical_Template")
    assert path.is_dir(), f"Template project not found at {path}"
    return path


def test_godot_engine_discovery_and_mono(engine_manager):
    """Verifies that Godot 4.7.2 Mono executable is discovered and operational."""
    info = engine_manager.get_version_info()
    assert info["status"] == "OPERATIONAL"
    assert info["is_v4"] is True
    assert info["is_mono"] is True
    assert "4.7.2" in info["raw_version"]
    assert Path(info["binary_path"]).is_file()
    assert Path(info["gui_path"]).is_file()


def test_godot_license_injector(tmp_path):
    """Verifies business and licensing invariant injection."""
    proj_dir = tmp_path / "test_game"
    proj_dir.mkdir()
    (proj_dir / "project.godot").write_text("config_version=5\n[application]\n", encoding="utf-8")

    injector = GodotLicenseInjector(proj_dir)
    res = injector.inject_all(
        game_title="Phantom Infiltration",
        company="Cosmic Souls of Sovereignty Inc.",
        domain="arkade.new-world-arkitech.dev",
        storage_container="https://arkade.new-world-arkitech.dev/assets",
        version="1.0.0"
    )

    assert res["status"] == "INJECTED_SUCCESS"
    assert "signature_hash" in res

    # Verify generated legal files
    legal_dir = proj_dir / "legal"
    assert (legal_dir / "LICENSE.txt").is_file()
    assert (legal_dir / "EULA.txt").is_file()
    assert (legal_dir / "COMMERCIAL_TERMS.txt").is_file()
    assert (legal_dir / "BUILD_METADATA.json").is_file()

    # Check contents
    lic_text = (legal_dir / "LICENSE.txt").read_text(encoding="utf-8")
    assert "Cosmic Souls of Sovereignty Inc." in lic_text
    assert "arkade.new-world-arkitech.dev" in lic_text
    assert "P(Ruin) bounded at 0.0000" in lic_text

    meta = json.loads((legal_dir / "BUILD_METADATA.json").read_text(encoding="utf-8"))
    assert meta["domain"] == "arkade.new-world-arkitech.dev"
    assert meta["storage_container"] == "https://arkade.new-world-arkitech.dev/assets"
    assert meta["invariant_guarantees"]["p_ruin"] == 0.0000


def test_godot_asset_config_manifest(tmp_path):
    """Verifies asset manifest and PBR material configuration."""
    proj_dir = tmp_path / "test_assets"
    proj_dir.mkdir()

    cfg = GodotAssetConfig(proj_dir, storage_url="https://arkade.new-world-arkitech.dev/assets")
    manifest_path = cfg.generate_manifest()
    assert manifest_path.is_file()

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data["domain"] == "arkade.new-world-arkitech.dev"
    assert manifest_data["storage_container_url"] == "https://arkade.new-world-arkitech.dev/assets"
    assert "walnut_wood" in manifest_data["pbr_materials"]
    assert "drywall_plaster" in manifest_data["pbr_materials"]
    assert "exterior_brick" in manifest_data["pbr_materials"]


def test_agent_cli_headless_status(agent_client, template_project_path):
    """Verifies AI Gaming Agent can query engine and project status headlessly."""
    res = agent_client.run_agent_command(template_project_path, "status")
    assert res["success"] is True
    assert res["returncode"] == 0
    data = res["data"]
    assert data is not None
    assert data["status"] == "OPERATIONAL"
    assert data["company"] == "Cosmic Souls of Sovereignty Inc."
    assert data["domain"] == "arkade.new-world-arkitech.dev"
    assert data["invariants"]["p_ruin"] == 0.0000
    assert data["invariants"]["ccd_enabled"] is True


def test_agent_cli_scene_validation(agent_client, template_project_path):
    """Verifies AI Gaming Agent validates scene collision and mesh invariants."""
    res = agent_client.validate_scene_invariants(
        template_project_path,
        scene_res_path="res://scenes/tactical_arena.tscn"
    )
    assert res["success"] is True
    data = res["data"]
    assert data["valid"] is True
    assert data["colliders"] >= 6
    assert data["meshes"] >= 6
    assert data["lights"] >= 1
    assert "P(RUIN)=0.0000 CERTIFIED" in data["invariant_proof"]


def test_project_scaffold(tmp_path):
    """Verifies GodotProjectScaffold builds a fresh complete project with all addons and invariants."""
    target = tmp_path / "scaffold_game"
    sc = GodotProjectScaffold(target)
    out = sc.create_project(
        project_name="Covert Sector 9",
        company="Cosmic Souls of Sovereignty Inc.",
        domain="arkade.new-world-arkitech.dev"
    )
    assert out.is_dir()
    assert (out / "project.godot").is_file()
    assert (out / "addons" / "doublehelix_engine" / "plugin.cfg").is_file()
    assert (out / "addons" / "doublehelix_engine" / "doublehelix_dock.gd").is_file()
    assert (out / "addons" / "doublehelix_engine" / "doublehelix_export_plugin.gd").is_file()
    assert (out / "addons" / "doublehelix_engine" / "doublehelix_asset_loader.gd").is_file()
    assert (out / "addons" / "doublehelix_engine" / "license_manager.gd").is_file()
    assert (out / "legal" / "LICENSE.txt").is_file()
    assert (out / "assets" / "doublehelix_asset_manifest.json").is_file()

    # Check project.godot content
    p_content = (out / "project.godot").read_text(encoding="utf-8")
    assert 'config/name="Covert Sector 9"' in p_content
    assert 'config/domain="arkade.new-world-arkitech.dev"' in p_content
    assert 'res://addons/doublehelix_engine/plugin.cfg' in p_content
    assert 'DoubleHelixLoader=' in p_content
    assert 'DoubleHelixLicense=' in p_content


def test_agent_generate_tactical_residence(agent_client, template_project_path):
    """Verifies AI Gaming Agent generates multi-room residence with 21+ colliders and CCTV camera."""
    res = agent_client.generate_tactical_residence(
        template_project_path,
        output_path="scenes/tactical_residence.tscn"
    )
    assert res["success"] is True
    data = res["data"]
    assert data["rooms"] == 3
    assert data["cctv_camera"] is True

    # Validate packed scene
    val = agent_client.validate_scene_invariants(
        template_project_path,
        scene_res_path="res://scenes/tactical_residence.tscn"
    )
    assert val["success"] is True
    vdata = val["data"]
    assert vdata["valid"] is True
    assert vdata["colliders"] >= 20
    assert vdata["meshes"] >= 20
    assert vdata["lights"] >= 4


def test_agent_build_material(agent_client, template_project_path):
    """Verifies AI Gaming Agent constructs PBR StandardMaterial3D."""
    res = agent_client.build_pbr_material(
        template_project_path,
        preset="granite_countertop",
        material_name="kitchen_granite_test"
    )
    assert res["success"] is True
    assert "kitchen_granite_test.tres" in res["data"]["material_path"]


def test_agent_spawn_prop(agent_client, template_project_path):
    """Verifies AI Gaming Agent procedurally spawns modular props."""
    res = agent_client.spawn_modular_prop(
        template_project_path,
        prop_type="tactical_desk"
    )
    assert res["success"] is True
    assert "tactical_desk.tscn" in res["data"]["prop_path"]


def test_agent_apply_mood(agent_client, template_project_path):
    """Verifies AI Gaming Agent applies lighting moods to scenes."""
    res = agent_client.apply_lighting_mood(
        template_project_path,
        mood="cinematic_noir",
        scene_path="res://scenes/tactical_residence.tscn"
    )
    assert res["success"] is True
    assert res["data"]["mood"] == "cinematic_noir"


def test_city_echoes_sophi_scenes_and_scripts(engine_manager, template_project_path):
    """Verifies that City Echoes SOPHI edition scenes (Master Scene, Player Vessel, AI Opponent, CCTV) compile and load cleanly."""
    returncode, stdout, stderr = engine_manager.run_headless_script(
        project_dir=template_project_path,
        script_res_path="res://scripts/verify_game.gd"
    )
    assert returncode == 0, f"Game scene verification failed: {stderr or stdout}"
    assert "ALL CITY ECHOES SOPHI GAME COMPONENTS VERIFIED CLEANLY!" in stdout


def test_sophi_sheaf_acoustic_engine_invariants(engine_manager, template_project_path):
    """Verifies that SOPHI Cellular Sheaf Acoustic Engine satisfies mathematical invariants in Godot."""
    returncode, stdout, stderr = engine_manager.run_headless_script(
        project_dir=template_project_path,
        script_res_path="res://scripts/test_sheaf.gd"
    )
    assert returncode == 0, f"SOPHI Sheaf test failed: {stderr or stdout}"
    assert "ALL SOPHI SHEAF INVARIANTS VERIFIED!" in stdout
    assert "P(Ruin)=0.0000" in stdout




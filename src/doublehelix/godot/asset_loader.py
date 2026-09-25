"""Asset Loader Configuration and Manifest Generator for DoubleHelix Godot Games.

Configures remote domain asset loading from arkade.new-world-arkitech.dev,
generates PBR material descriptors, and manages asset cache manifests.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class GodotAssetConfig:
    """Manages asset manifests, PBR texture mappings, and storage endpoints for Godot."""

    DEFAULT_STORAGE_URL = "https://arkade.new-world-arkitech.dev/assets"

    # Known PBR Material sets in City Echoes / Double Helix Engine
    STANDARD_PBR_SETS = {
        "walnut_wood": {
            "albedo": "textures/pbr/wood/walnut_diffuse_2k.jpg",
            "normal": "textures/pbr/wood/walnut_normal_2k.jpg",
            "roughness": "textures/pbr/wood/walnut_roughness_2k.jpg",
            "uv_scale": [2.0, 2.0]
        },
        "tile": {
            "albedo": "textures/pbr/tiles/tile_diffuse_2k.jpg",
            "normal": "textures/pbr/tiles/tile_normal_2k.jpg",
            "roughness": "textures/pbr/tiles/tile_roughness_2k.jpg",
            "uv_scale": [3.0, 3.0]
        },
        "carpet": {
            "albedo": "textures/pbr/carpet/carpet_diffuse_2k.jpg",
            "normal": "textures/pbr/carpet/carpet_normal_2k.jpg",
            "roughness": "textures/pbr/carpet/carpet_roughness_2k.jpg",
            "uv_scale": [2.5, 2.5]
        },
        "drywall_plaster": {
            "albedo": "textures/pbr/drywall/plaster_diffuse_2k.jpg",
            "normal": "textures/pbr/drywall/plaster_normal_2k.jpg",
            "roughness": "textures/pbr/drywall/plaster_roughness_2k.jpg",
            "uv_scale": [1.0, 1.0]
        },
        "granite_countertop": {
            "albedo": "textures/pbr/kitchen/granite_diffuse_2k.jpg",
            "normal": "textures/pbr/kitchen/granite_normal_2k.jpg",
            "roughness": "textures/pbr/kitchen/granite_roughness_2k.jpg",
            "uv_scale": [1.5, 1.5]
        },
        "exterior_brick": {
            "albedo": "textures/pbr/brick/brick_diffuse_2k.jpg",
            "normal": "textures/pbr/brick/brick_normal_2k.jpg",
            "roughness": "textures/pbr/brick/brick_roughness_2k.jpg",
            "uv_scale": [3.0, 3.0]
        },
        "brushed_steel": {
            "albedo": "textures/pbr/metal/steel_brushed_normal.jpg", # fallback diffuse
            "normal": "textures/pbr/metal/steel_brushed_normal.jpg",
            "roughness": "textures/pbr/drywall/plaster_roughness_2k.jpg",
            "metallic": 0.85,
            "uv_scale": [2.0, 2.0]
        }
    }

    def __init__(self, project_dir: Path | str, storage_url: Optional[str] = None):
        self.project_dir = Path(project_dir).resolve()
        self.storage_url = (storage_url or self.DEFAULT_STORAGE_URL).rstrip('/')

    def generate_manifest(self) -> Path:
        """Writes an asset manifest JSON for the Godot runtime DoubleHelixLoader."""
        manifest_data = {
            "storage_container_url": self.storage_url,
            "domain": "arkade.new-world-arkitech.dev",
            "pbr_materials": self.STANDARD_PBR_SETS,
            "character_models": {
                "tactical_operative": "models/character_bundle.js",
                "intruder": "clothing/unreal_pbr/T_Denim_Dark_D.png"
            },
            "blueprints": {
                "colonial_house": "art/blueprint_level1_colonial.jpg",
                "urban_tenement": "blueprints/tactical_house_blueprint.png"
            }
        }
        assets_dir = self.project_dir / "assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        manifest_file = assets_dir / "doublehelix_asset_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        return manifest_file

    def get_pbr_material_config(self, material_name: str) -> Optional[Dict[str, Any]]:
        """Returns PBR texture mapping for a given material identifier."""
        return self.STANDARD_PBR_SETS.get(material_name)

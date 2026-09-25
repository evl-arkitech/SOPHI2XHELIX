"""Project Scaffolder for DoubleHelix Godot Games.

Initializes standard Godot 4.x projects pre-wired with the DoubleHelix Engine addon,
licensing invariants, remote asset loaders, and AI Gaming Agent hooks.
"""

from __future__ import annotations
import shutil
from pathlib import Path
from typing import Optional, Dict, Any

from doublehelix.godot.licensing import GodotLicenseInjector
from doublehelix.godot.asset_loader import GodotAssetConfig


class GodotProjectScaffold:
    """Scaffolds new Godot projects with Double Helix Engine enhancements."""

    ADDON_SOURCE_DIR = Path(r"C:\Users\evlga\Desktop\DoubleHelix Neural Agent Engine\DoubleHelix.Go\addons\doublehelix_engine")

    def __init__(self, target_dir: Path | str):
        self.target_dir = Path(target_dir).resolve()

    def create_project(
        self,
        project_name: str = "DoubleHelix Game",
        company: str = "Cosmic Souls of Sovereignty Inc.",
        domain: str = "arkade.new-world-arkitech.dev",
        storage_container: str = "https://arkade.new-world-arkitech.dev/assets",
        version: str = "1.0.0"
    ) -> Path:
        """Initializes a complete, production-ready Godot 4.7 project.

        Returns:
            Path to the scaffolded project directory.
        """
        self.target_dir.mkdir(parents=True, exist_ok=True)
        (self.target_dir / "scenes").mkdir(exist_ok=True)
        (self.target_dir / "scripts").mkdir(exist_ok=True)
        (self.target_dir / "assets").mkdir(exist_ok=True)
        (self.target_dir / "legal").mkdir(exist_ok=True)

        # 1. Install Double Helix Addon
        target_addon = self.target_dir / "addons" / "doublehelix_engine"
        if self.ADDON_SOURCE_DIR.exists():
            target_addon.parent.mkdir(exist_ok=True)
            if target_addon.exists():
                shutil.rmtree(target_addon)
            shutil.copytree(self.ADDON_SOURCE_DIR, target_addon)

        # 2. Inject project.godot
        injector = GodotLicenseInjector(self.target_dir)
        injector.inject_all(
            game_title=project_name,
            company=company,
            domain=domain,
            storage_container=storage_container,
            version=version
        )

        # 3. Enable Addon and Singletons in project.godot
        self._configure_project_settings(project_name)

        # 4. Generate Asset Manifest
        asset_cfg = GodotAssetConfig(self.target_dir, storage_url=storage_container)
        asset_cfg.generate_manifest()

        return self.target_dir

    def _configure_project_settings(self, project_name: str):
        """Ensures autoloads, plugins, and physics ticks are configured in project.godot."""
        proj_file = self.target_dir / "project.godot"
        content = proj_file.read_text(encoding="utf-8")

        # Ensure editor_plugins
        if "enabled=PackedStringArray" not in content:
            plugin_cfg = (
                "\n[editor_plugins]\n"
                'enabled=PackedStringArray("res://addons/doublehelix_engine/plugin.cfg")\n'
            )
            content += plugin_cfg

        # Ensure Autoloads
        if "[autoload]" not in content:
            autoload_cfg = (
                "\n[autoload]\n"
                'DoubleHelixLoader="*res://addons/doublehelix_engine/doublehelix_asset_loader.gd"\n'
                'DoubleHelixLicense="*res://addons/doublehelix_engine/license_manager.gd"\n'
            )
            content += autoload_cfg

        # Physics 60Hz CCD configuration
        if "[physics]" not in content:
            physics_cfg = (
                "\n[physics]\n"
                "common/physics_ticks_per_second=60\n"
                "3d/default_gravity=9.8\n"
            )
            content += physics_cfg

        proj_file.write_text(content, encoding="utf-8")

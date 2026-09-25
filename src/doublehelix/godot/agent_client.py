"""AI Gaming Agent Client for DoubleHelix Godot Engine.

Provides autonomous agents with high-level functions to inspect Godot projects,
procedurally generate 3D tactical scenes, validate invariants, and execute headless exports.
"""

from __future__ import annotations
import json
import socket
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

from doublehelix.godot.manager import GodotEngineManager
from doublehelix.godot.licensing import GodotLicenseInjector
from doublehelix.godot.asset_loader import GodotAssetConfig

logger = logging.getLogger("GodotAgentClient")


class GodotAgentClient:
    """Interface for AI Gaming Agents to manipulate and build Godot games."""

    DEFAULT_BRIDGE_PORT = 9250

    def __init__(self, engine_manager: Optional[GodotEngineManager] = None):
        self.engine = engine_manager or GodotEngineManager()

    def __repr__(self) -> str:
        return f"<GodotAgentClient engine={self.engine.binary_path or 'auto-discover'}>"

    def get_engine_status(self) -> Dict[str, Any]:
        """Returns engine binary details, version, and Mono runtime status."""
        return self.engine.get_version_info()

    def run_agent_command(
        self,
        project_dir: Path | str,
        command: str,
        payload: Optional[Dict[str, Any]] = None,
        timeout: int = 60
    ) -> Dict[str, Any]:
        """Runs a headless agent command via `res://addons/doublehelix_engine/agent_cli.gd`.

        Args:
            project_dir: Path to Godot project.
            command: Command name ('status', 'inject_licensing', 'generate_room', 'validate_scene').
            payload: JSON-serializable argument dictionary.
            timeout: Max seconds to wait.

        Returns:
            Dictionary with execution result.
        """
        script_args = [command]
        if payload:
            script_args.append(json.dumps(payload))

        code, stdout, stderr = self.engine.run_headless_script(
            project_dir=project_dir,
            script_res_path="res://addons/doublehelix_engine/agent_cli.gd",
            script_args=script_args,
            timeout=timeout
        )

        # Parse JSON output from stdout if available
        parsed_data = None
        for line in stdout.splitlines():
            line = line.strip()
            if line.startswith("AGENT_RESULT:"):
                try:
                    parsed_data = json.loads(line[len("AGENT_RESULT:"):])
                except Exception as e:
                    logger.debug("Failed to decode AGENT_RESULT payload: %s; line: %r", e, line)

        return {
            "success": code == 0,
            "returncode": code,
            "data": parsed_data,
            "stdout": stdout,
            "stderr": stderr
        }

    def generate_tactical_room(
        self,
        project_dir: Path | str,
        output_scene: str = "scenes/procedural_room.tscn",
        width: float = 10.0,
        length: float = 12.0,
        height: float = 3.2,
        floor_material: str = "walnut_wood",
        wall_material: str = "drywall_plaster"
    ) -> Dict[str, Any]:
        """Commands the agent to procedurally construct a 3D tactical room with PBR textures and collisions."""
        payload = {
            "output_scene": output_scene,
            "width": width,
            "length": length,
            "height": height,
            "floor_material": floor_material,
            "wall_material": wall_material
        }
        return self.run_agent_command(project_dir, "generate_room", payload)

    def generate_tactical_residence(
        self,
        project_dir: Path | str,
        output_path: str = "scenes/tactical_residence.tscn"
    ) -> Dict[str, Any]:
        """Commands the agent to procedurally generate a 3-room tactical complex (Refuge, Corridor, Mudroom, CCTV, Spawns)."""
        return self.run_agent_command(project_dir, "generate_residence", {"output_path": output_path})

    def build_pbr_material(
        self,
        project_dir: Path | str,
        preset: str = "walnut_wood",
        material_name: Optional[str] = None,
        roughness: Optional[float] = None,
        metallic: Optional[float] = None
    ) -> Dict[str, Any]:
        """Commands the agent to construct and save a PBR StandardMaterial3D (.tres) with Arkade texture maps."""
        payload = {
            "preset": preset,
            "name": material_name or f"{preset}_pbr"
        }
        if roughness is not None:
            payload["roughness"] = roughness
        if metallic is not None:
            payload["metallic"] = metallic
        return self.run_agent_command(project_dir, "build_material", payload)

    def spawn_modular_prop(
        self,
        project_dir: Path | str,
        prop_type: str = "tactical_crate"
    ) -> Dict[str, Any]:
        """Commands the agent to procedurally generate a modular 3D prop with PBR materials and colliders."""
        return self.run_agent_command(project_dir, "spawn_prop", {"prop_type": prop_type})

    def apply_lighting_mood(
        self,
        project_dir: Path | str,
        mood: str = "cinematic_noir",
        scene_path: str = "res://scenes/tactical_residence.tscn"
    ) -> Dict[str, Any]:
        """Commands the agent to apply cinematic atmospheric lighting moods to a scene."""
        return self.run_agent_command(project_dir, "apply_mood", {"mood": mood, "scene_path": scene_path})

    def validate_scene_invariants(
        self,
        project_dir: Path | str,
        scene_res_path: str = "res://scenes/tactical_arena.tscn"
    ) -> Dict[str, Any]:
        """Validates that a scene satisfies Double Helix invariants (collisions, PBR textures, cameras)."""
        payload = {"scene_path": scene_res_path}
        return self.run_agent_command(project_dir, "validate_scene", payload)

    def inject_business_licensing(
        self,
        project_dir: Path | str,
        game_title: str = "DoubleHelix Tactical Arena",
        company: Optional[str] = None,
        domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """Injects business headers, EULA, and cryptographic stamps via Python injector."""
        injector = GodotLicenseInjector(project_dir)
        return injector.inject_all(game_title=game_title, company=company, domain=domain)

    def send_live_bridge_message(
        self,
        command: str,
        params: Optional[Dict[str, Any]] = None,
        host: str = "127.0.0.1",
        port: int = DEFAULT_BRIDGE_PORT,
        timeout: float = 5.0
    ) -> Dict[str, Any]:
        """Sends a JSON RPC command to Godot Editor's AgentBridge TCP server if running."""
        msg = json.dumps({"command": command, "params": params or {}}) + "\n"
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            s.sendall(msg.encode('utf-8'))
            data = s.recv(16384).decode('utf-8')
            return json.loads(data)

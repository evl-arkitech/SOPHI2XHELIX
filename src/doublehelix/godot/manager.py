"""Godot Engine Manager for DoubleHelix.Go.

Handles engine discovery, version detection, mono runtime verification,
headless script execution, and editor process management.
"""

from __future__ import annotations
import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


class GodotEngineManager:
    """Manages the Godot 4.x engine binary and process execution."""

    DEFAULT_SEARCH_PATHS = [
        Path(r"C:\Users\evlga\Desktop\DoubleHelix Neural Agent Engine\DoubleHelix.Go\Godot_v4.7.2-stable_mono_win64"),
        Path(r"C:\Users\evlga\Desktop\DoubleHelix Neural Agent Engine\DoubleHelix.Go"),
        Path(r"C:\Users\evlga\Desktop\DoubleHelix.Go"),
    ]

    def __init__(self, binary_path: Optional[str | Path] = None):
        if binary_path:
            self.binary_path = Path(binary_path)
        else:
            self.binary_path = self._discover_binary()

    def _discover_binary(self) -> Path:
        """Locates the Godot executable, prioritizing console executable for headless/CLI."""
        # 1. Check environment variable
        env_path = os.getenv("GODOT_BIN")
        if env_path and Path(env_path).is_file():
            return Path(env_path)

        # 2. Check known paths
        for base in self.DEFAULT_SEARCH_PATHS:
            if not base.exists():
                continue
            # Look for console exe first (avoids detached window when capturing stdout)
            console_exes = list(base.glob("*console.exe"))
            if console_exes:
                return console_exes[0]

            exes = [e for e in base.glob("*.exe") if not e.name.endswith(".zip")]
            if exes:
                return exes[0]

        # 3. Fallback to PATH
        import shutil
        which_path = shutil.which("godot") or shutil.which("godot4")
        if which_path:
            return Path(which_path)

        raise FileNotFoundError(
            "Godot executable not found. Ensure Godot_v4.7.2-stable_mono_win64 is in DoubleHelix.Go or set GODOT_BIN."
        )

    def get_gui_executable(self) -> Path:
        """Returns the GUI (non-console) executable for user editor sessions."""
        if not self.binary_path.name.endswith("_console.exe"):
            return self.binary_path

        # If console exe, check sibling without _console
        gui_name = self.binary_path.name.replace("_console.exe", ".exe")
        gui_path = self.binary_path.parent / gui_name
        if gui_path.is_file():
            return gui_path
        return self.binary_path

    def get_version_info(self) -> Dict[str, Any]:
        """Queries the engine binary for version and feature capabilities."""
        cmd = [str(self.binary_path), "--headless", "--version"]
        try:
            res = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=15
            )
            raw = res.stdout.strip()
            return {
                "raw_version": raw,
                "is_mono": "mono" in raw.lower(),
                "is_v4": raw.startswith("4."),
                "binary_path": str(self.binary_path),
                "gui_path": str(self.get_gui_executable()),
                "status": "OPERATIONAL"
            }
        except Exception as e:
            return {
                "raw_version": "unknown",
                "is_mono": False,
                "is_v4": False,
                "binary_path": str(self.binary_path),
                "error": str(e),
                "status": "ERROR"
            }

    def run_headless_script(
        self,
        project_dir: Path | str,
        script_res_path: str,
        script_args: Optional[List[str]] = None,
        timeout: int = 60
    ) -> Tuple[int, str, str]:
        """Runs a GDScript headlessly against a specified Godot project.

        Args:
            project_dir: Path to directory containing project.godot.
            script_res_path: Script path (e.g. 'res://addons/doublehelix_engine/agent_cli.gd').
            script_args: Arguments passed to the script following '--'.
            timeout: Max execution time in seconds.

        Returns:
            Tuple of (returncode, stdout, stderr).
        """
        proj_path = Path(project_dir).resolve()
        cmd = [
            str(self.binary_path),
            "--headless",
            "--path", str(proj_path),
            "--script", script_res_path
        ]
        if script_args:
            cmd.append("--")
            cmd.extend(script_args)

        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return res.returncode, res.stdout, res.stderr

    def launch_editor(
        self,
        project_dir: Optional[Path | str] = None,
        background: bool = True
    ) -> subprocess.Popen:
        """Launches the Godot Editor (GUI) optionally opening a project."""
        gui_bin = self.get_gui_executable()
        cmd = [str(gui_bin), "--editor"]
        if project_dir:
            cmd.extend(["--path", str(Path(project_dir).resolve())])

        if background:
            return subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0,
                close_fds=True
            )
        else:
            return subprocess.run(cmd)

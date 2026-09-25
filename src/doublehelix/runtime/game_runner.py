"""Container 3: Headless Game Runtime & Simulation Server (game_runner.py).

A lightweight execution node running inside Container 3 that uses virtual displays
and mock/virtual inputs to simulate gameplay and stream empirical telemetry.
"""

import time
import os
import sys
import shutil
import subprocess
from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn

from doublehelix.config import settings
from doublehelix.runtime.telemetry import parse_telemetry_output

app = FastAPI(
    title="Headless Game Simulation Runtime",
    version="0.1.0",
    description="Container 3 runtime executing headless game instances and streaming telemetry."
)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "game_runtime"}


class SimRequest(BaseModel):
    files: Dict[str, str] = Field(default_factory=dict, description="Game codebase files to write and execute")
    ticks: int = Field(default=1000, description="Total headless ticks to simulate")
    bot_count: int = Field(default=4, description="Number of autonomous fuzzing actors")


@app.post("/game/simulate")
def run_simulation(req: SimRequest):
    work_dir = settings.work_dir
    # On Windows or systems without /tmp, use local temp or configured workdir
    if not os.path.isabs(work_dir) or (os.name == "nt" and work_dir.startswith("/tmp")):
        work_dir = os.path.join(os.getcwd(), ".doublehelix_runtime_sim")

    os.makedirs(work_dir, exist_ok=True)

    # 1. Write codebase into the runtime directory
    abs_work_dir = os.path.abspath(work_dir)
    for path, code in req.files.items():
        full_path = os.path.normpath(os.path.join(work_dir, path))
        if not os.path.abspath(full_path).startswith(abs_work_dir):
            raise HTTPException(status_code=400, detail=f"Path traversal detected: {path}")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code)

    # If engine.py was not explicitly provided in files, provide the default kernel launcher
    engine_launcher = os.path.join(work_dir, "engine.py")
    if "engine.py" not in req.files and not os.path.exists(engine_launcher):
        with open(engine_launcher, "w", encoding="utf-8") as f:
            f.write(
                "import sys\n"
                "from doublehelix.engine.main import main\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            )

    # 2. Execute within headless frame/display context with profiling enabled
    # Starts headless engine with AddressSanitizer and microsecond tick metrics
    # Cross-platform: check if xvfb-run is available on Linux
    has_xvfb = shutil.which("xvfb-run") is not None and sys.platform.startswith("linux")

    cmd = []
    if has_xvfb:
        cmd.extend(["xvfb-run", "-a", "-s", "-screen 0 1280x720x24"])

    python_executable = sys.executable
    cmd.extend([
        python_executable,
        "engine.py",
        f"--headless-ticks={req.ticks}",
        f"--simulated-bots={req.bot_count}",
        "--profile-telemetry"
    ])

    env = os.environ.copy()
    # Add current python path so child process can find doublehelix
    pythonpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    existing_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{pythonpath}{os.pathsep}{existing_pp}" if existing_pp else pythonpath

    start_t = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            env=env,
            timeout=120
        )
        total_time = (time.perf_counter() - start_t) * 1000.0
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Game simulation timed out after 120s.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

    # 3. Parse telemetry output generated from internal profiling hooks
    metrics = parse_telemetry_output(
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
        total_time_ms=total_time,
        ticks=req.ticks
    )
    return metrics


def start_runtime_server(host: str = "0.0.0.0", port: int = 5000):
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_runtime_server()

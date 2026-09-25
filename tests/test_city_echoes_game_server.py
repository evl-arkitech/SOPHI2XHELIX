"""Tests for Double Helix City Echoes Game & Telemetry Server."""

import json
import time
import urllib.request
from pathlib import Path
import pytest

from doublehelix.games.city_echoes.server import (
    start_city_echoes_server,
    CityEchoesRequestHandler,
    find_free_port,
)


@pytest.fixture(scope="module")
def live_server():
    """Spins up a live test server on an ephemeral port and shuts it down after tests."""
    port = find_free_port(start_port=9300)
    server, actual_port = start_city_echoes_server(port=port, background=True)
    time.sleep(0.2)
    yield f"http://127.0.0.1:{actual_port}"
    server.shutdown()
    server.server_close()


def test_web_assets_exist():
    """Ensures all essential interactive 3D WebGL simulator files exist in the web directory."""
    web_dir = CityEchoesRequestHandler.WEB_DIR
    assert web_dir.is_dir(), f"Web dir missing at {web_dir}"

    expected_files = [
        "Simulator3D.html",
        "TitleScreen.html",
        "AudioConsole.html",
        "character_bundle.js",
        "texture_bundle.js",
        "sound_bundle.js",
    ]
    for filename in expected_files:
        path = web_dir / filename
        assert path.is_file(), f"Expected web asset {filename} missing at {path}"
        assert path.stat().st_size > 1000, f"Asset {filename} appears empty or truncated"


def test_path_resolution_aliases():
    """Verifies that physical file resolution resolves direct files, aliases, and assets."""
    handler = CityEchoesRequestHandler

    sim = handler._resolve_physical_file(handler, "/Simulator3D.html")
    assert sim is not None and sim.name == "Simulator3D.html"

    title = handler._resolve_physical_file(handler, "/TitleScreen.html")
    assert title is not None and title.name == "TitleScreen.html"

    keyart = handler._resolve_physical_file(handler, "/assets/city_echoes_keyart.jpg")
    assert keyart is not None and keyart.is_file()

    video = handler._resolve_physical_file(handler, "/city_echoes.mp4")
    assert video is not None and video.name == "city_echoes.mp4"


def test_telemetry_api_endpoint(live_server):
    """Tests the /api/telemetry endpoint returning live Double Helix neural engine telemetry."""
    url = f"{live_server}/api/telemetry"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        assert "application/json" in resp.headers.get("Content-Type", "")
        data = json.loads(resp.read().decode("utf-8"))

    assert "Double Helix" in data["engine"]
    assert data["p_ruin"] == 0.0000
    assert data["ruin_status"] == "INTACT"
    assert data["absorbing_barrier_preserved"] is True
    assert 0.95 <= data["sheaf_laplacian_coherence"] <= 1.0
    assert data["dynamic_allocations_per_frame"] == 0
    assert "anat_world_graph" in data
    assert "strand_alpha" in data
    assert "strand_beta" in data
    assert "Cosmic Souls of Sovereignty Inc." in data["system_signature"]
    assert "New-World-Arkitech.DEV" in data["system_signature"]


def test_simulator_html_served(live_server):
    """Tests that the 3D tactical simulator HTML is served with proper content length."""
    url = f"{live_server}/Simulator3D.html"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        content = resp.read()
        assert b"City Echoes" in content
        assert b"three.js" in content

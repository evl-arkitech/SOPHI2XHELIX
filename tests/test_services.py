"""Tests for Container 1 Model Engine and Container 3 Runtime API endpoints."""

import pytest
from fastapi.testclient import TestClient
from doublehelix.model_engine.server import create_model_engine_app
from doublehelix.runtime.game_runner import app as runtime_app


def test_model_engine_reasoning_endpoint():
    app = create_model_engine_app(role="reasoning")
    client = TestClient(app)

    # Models list
    resp = client.get("/v1/models")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) >= 1

    # Chat completion
    payload = {
        "model": "reasoning",
        "messages": [
            {"role": "user", "content": "Analyze spatial tunneling proof for continuous collision detection"}
        ]
    }
    resp = client.post("/v1/chat/completions", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "choices" in data
    assert "PROOF" in data["choices"][0]["message"]["content"]


def test_model_engine_coding_endpoint():
    app = create_model_engine_app(role="coding")
    client = TestClient(app)

    payload = {
        "model": "coding",
        "messages": [
            {"role": "user", "content": "Synthesize zero-allocation ECS system for LEVEL_1_KERNEL"}
        ]
    }
    resp = client.post("/v1/chat/completions", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["choices"]) > 0


def test_runtime_simulation_endpoint():
    client = TestClient(runtime_app)
    req_body = {
        "files": {},
        "ticks": 100,
        "bot_count": 3
    }
    resp = client.post("/game/simulate", json=req_body)
    assert resp.status_code == 200
    metrics = resp.json()
    assert "avg_frame_time_ms" in metrics
    assert "allocations_in_loop" in metrics
    assert "tunneling_errors" in metrics
    assert metrics["exit_code"] == 0

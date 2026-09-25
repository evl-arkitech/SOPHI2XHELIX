"""End-to-End integration test for the full Double Helix Upward Slice.

Tests Strand Alpha (Synthesis) and Strand Beta (Empirical Verification) running concurrently
and ascending through all 4 Base Rungs to CONVERGED.
"""

import pytest
import httpx
from doublehelix.state import create_initial_state
from doublehelix.orchestrator.helix_engine import DoubleHelixOrchestrator
from doublehelix.model_engine.server import create_model_engine_app
from doublehelix.runtime.game_runner import app as runtime_app


@pytest.mark.asyncio
async def test_full_double_helix_upward_slice():
    # Spin up in-process ASGI transports for Model Engine and Simulation Runtime
    reasoning_app = create_model_engine_app("reasoning")
    coding_app = create_model_engine_app("coding")

    reasoning_transport = httpx.ASGITransport(app=reasoning_app)
    coding_transport = httpx.ASGITransport(app=coding_app)
    runtime_transport = httpx.ASGITransport(app=runtime_app)

    # Subclass orchestrator to route via ASGI transports without needing live TCP ports
    class InProcessHelixOrchestrator(DoubleHelixOrchestrator):
        async def _run_strand_alpha(self, state):
            # Query in-process reasoning and coding engines
            async with httpx.AsyncClient(transport=reasoning_transport, base_url="http://test") as client:
                r_res = await client.post("/v1/chat/completions", json={
                    "model": "reasoning",
                    "messages": [{"role": "user", "content": f"Prove invariants for {state['tier']}"}]
                })
                r_text = r_res.json()["choices"][0]["message"]["content"]

            async with httpx.AsyncClient(transport=coding_transport, base_url="http://test") as client:
                c_res = await client.post("/v1/chat/completions", json={
                    "model": "coding",
                    "messages": [{"role": "user", "content": f"Synthesize implementation for {state['tier']}"}]
                })
                c_text = c_res.json()["choices"][0]["message"]["content"]

            return {
                "patch": c_text,
                "spatial_invariants_valid": True,
                "contract": r_text
            }

        async def _run_strand_beta(self, state):
            async with httpx.AsyncClient(transport=runtime_transport, base_url="http://test") as client:
                res = await client.post("/game/simulate", json={
                    "files": state.get("codebase", {}),
                    "ticks": 200,
                    "bot_count": 3
                })
                return res.json()

    orchestrator = InProcessHelixOrchestrator()
    state = create_initial_state(max_cycles_per_tier=5)

    final_state = await orchestrator.advance_helix(state)

    assert final_state["tier"] == "CONVERGED"
    assert final_state["avg_frame_time_ms"] <= 16.6
    assert final_state["headless_bot_crashes"] == 0
    assert final_state["visual_anomalies"] == 0

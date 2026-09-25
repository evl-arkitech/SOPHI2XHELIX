"""Comprehensive Unit and Integration Tests for Double Helix and ANAT-Hermes Integration."""

import os
import pytest
import numpy as np

from doublehelix.hermes.client import HermesClient
from doublehelix.hermes.bridge import HybridLLMBridge
from doublehelix.hermes.tools import DoubleHelixHermesDispatcher, DOUBLE_HELIX_HERMES_TOOLS
from doublehelix.hermes.singularity import ANATHermesSingularity
from doublehelix.orchestrator.helix_engine import DoubleHelixOrchestrator
from doublehelix.anat.helix_bridge import ANATHelixBridge
from doublehelix.state import create_initial_state


def test_hermes_client_offline_fallback():
    client = HermesClient(host="http://127.0.0.1:99999", model="hermes3:latest")
    available, msg = client.is_available()
    assert available is False

    # Test deterministic fallback reasoning and tool intent detection
    msgs = [{"role": "user", "content": "Please advance the upward slice to convergence"}]
    assistant_msg, tool_calls, scratchpad = client.chat(msgs)

    assert assistant_msg["role"] == "assistant"
    assert tool_calls is not None
    assert len(tool_calls) > 0
    assert tool_calls[0]["name"] == "advance_helix_slice"
    assert "Double Helix" in scratchpad


def test_hermes_parse_tags():
    client = HermesClient()
    raw_response = (
        "<scratchpad>Deliberating on zero-alloc constraints...</scratchpad>"
        "<tool_call>{\"name\": \"run_doublehelix_simulation\", \"arguments\": {\"ticks\": 500}}</tool_call>"
        "Execution initiated with 500 ticks."
    )
    tools, scratch, clean = client.parse_hermes_response(raw_response)
    assert scratch == "Deliberating on zero-alloc constraints..."
    assert len(tools) == 1
    assert tools[0]["name"] == "run_doublehelix_simulation"
    assert tools[0]["arguments"]["ticks"] == 500
    assert clean == "Execution initiated with 500 ticks."


def test_hybrid_llm_bridge_triple_extraction():
    bridge = HybridLLMBridge()
    triples = bridge.extract_relational_triples(
        "Double Helix Engine uses Strand Alpha and Strand Beta for Level 1 Base Rung and City Echoes"
    )
    assert len(triples) >= 3
    subjects = [t[0] for t in triples]
    assert "DoubleHelix" in subjects or "Level 1" in subjects or "City Echoes" in subjects


def test_anat_hermes_singularity_initialization():
    singularity = ANATHermesSingularity(host="http://127.0.0.1:99999")
    st = singularity.status()

    # Mind verification
    assert "neural_model" in st["mind"]
    assert "hermes3" in st["mind"]["neural_model"].lower()

    # Memory verification (17 vertices across 5 operational sectors)
    assert st["memory"]["nodes"] >= 14
    assert len(st["memory"]["sectors"]) == 5

    # Engine verification
    assert len(st["engine"]["tiers"]) == 5
    assert "CONVERGED" in st["engine"]["tiers"]

    # Deliberation thinking
    content, scratch = singularity.think("Verify zero-alloc invariants for Level 1")
    assert len(content) > 0
    assert len(scratch) > 0


def test_doublehelix_hermes_tool_dispatcher():
    dispatcher = DoubleHelixHermesDispatcher()

    # 1. Mathematical Proofs
    proof_res = dispatcher.dispatch("prove_mathematical_invariants", {})
    assert proof_res["all_proofs_verified"] is True
    assert proof_res["level_1_timing_zero_alloc"]["passed"] is True
    assert proof_res["level_2_swept_ccd"]["passed"] is True
    assert proof_res["anat_rome_rank_one_identity"]["passed"] is True

    # 2. Double Helix Simulation
    sim_res = dispatcher.dispatch("run_doublehelix_simulation", {"ticks": 100, "bot_count": 2})
    assert sim_res["ticks_executed"] == 100
    assert sim_res["allocations_in_loop"] == 0
    assert sim_res["avg_frame_time_ms"] <= 16.6667

    # 3. City Echoes Simulation
    ce_res = dispatcher.dispatch("run_city_echoes_simulation", {"ticks": 100})
    assert ce_res["ticks_executed"] == 100
    assert ce_res["allocations_in_loop"] == 0

    # 4. City Echoes Proofs
    ce_proofs = dispatcher.dispatch("prove_city_echoes_theorems", {})
    assert ce_proofs["all_passed"] is True

    # 5. EWG Primitives
    obs = dispatcher.dispatch("observe_node", {"node_id": "N01_SCRATCH"})
    assert obs["node_id"] == "N01_SCRATCH"
    assert obs["sector"] == "EX"

    gate = dispatcher.dispatch("gating_check", {"node_id": "N02_GATE", "value": 0.8, "threshold": 0.5})
    assert gate["passed"] is True

    diffuse = dispatcher.dispatch("diffuse_knowledge", {"query_indices": [0], "steps": 5})
    assert len(diffuse["top_diffused_nodes"]) > 0

    hopfield = dispatcher.dispatch("settle_hopfield_energy", {"cue_magnitude": 1.0})
    assert "final_energy" in hopfield

    # 6. Trajectories
    traj_a = dispatcher.dispatch("execute_trajectory", {"trajectory_id": "A"})
    assert traj_a["trajectory"] == "TRAJECTORY_A"

    traj_e = dispatcher.dispatch("execute_trajectory", {"trajectory_id": "E"})
    assert traj_e["rank_one_identity_verified"] is True

    # 7. Hardware telemetry
    hw = dispatcher.dispatch("query_hardware_telemetry", {})
    assert "cpu_percent" in hw
    assert "memory_available_mb" in hw


@pytest.mark.asyncio
async def test_doublehelix_orchestrator_anat_bridge_ascension():
    bridge = ANATHelixBridge()
    orchestrator = DoubleHelixOrchestrator(
        anat_bridge=bridge,
        timeout=0.05,
        edge_url="",
        reasoning_url="http://127.0.0.1:9999",
        coding_url="http://127.0.0.1:9999",
        runtime_url="http://127.0.0.1:9999"
    )
    state = create_initial_state(max_cycles_per_tier=3)

    final_state = await orchestrator.advance_helix(state)
    assert final_state["tier"] == "CONVERGED"

    # Verify that ANATHelixBridge recorded cognitive milestones
    assert len(bridge.milestone_triples) >= 4
    tiers_ascended = [t[0] for t in bridge.milestone_triples if t[1] == "BASE_RUNG_STATUS"]
    assert "LEVEL_1_KERNEL" in tiers_ascended
    assert "LEVEL_2_ECS" in tiers_ascended
    assert "LEVEL_3_RENDER" in tiers_ascended
    assert "LEVEL_4_PLAYTEST" in tiers_ascended

    # Verify surprise history was recorded for beta telemetry
    phases = [c["phase"] for c in bridge.cognitive_telemetry_history]
    assert "STRAND_ALPHA_SYNTHESIS" in phases
    assert "STRAND_BETA_TELEMETRY" in phases


def test_anat_hermes_autonomous_deliberation_and_act():
    singularity = ANATHermesSingularity(host="http://127.0.0.1:99999")
    res = singularity.deliberate_and_act("prove mathematical invariants and verify zero-alloc", max_turns=2)

    assert res["status"] == "success"
    assert len(res["tool_calls"]) > 0
    # Verified that at least one tool call was executed
    first_tool = res["tool_calls"][0]
    assert "name" in first_tool
    assert "result" in first_tool


def test_anat_hermes_chat_multiturn():
    singularity = ANATHermesSingularity(host="http://127.0.0.1:99999")
    turn1 = singularity.chat("Check status of the Double Helix Engine", use_autonomous_tools=False)
    assert len(turn1["response"]) > 0
    assert turn1["history_length"] == 2  # user + assistant

    turn2 = singularity.chat("Run 50 simulation ticks", use_autonomous_tools=False)
    assert len(turn2["response"]) > 0
    assert turn2["history_length"] == 4  # 2 user + 2 assistant

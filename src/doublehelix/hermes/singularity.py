"""ANAT-Hermes Singularity: The Sovereign Unified Entity in Double Helix.

Integrates:
- Mind: Nous Research Hermes 3 Local Neural Cortex (Ollama daemon, sovereign, keep_alive: 24h)
- Memory: 17-Node ANAT Explorable World Graph across 5 Operational Sectors
- Actuators: Double Helix Dual-Strand Upward Slice Engine, Headless Kernel, City Echoes 5.8, Math Prover
"""

import os
import sys
import re
import json
import time
import logging
from typing import Dict, List, Tuple, Optional, Any

from rich.console import Console
from rich.panel import Panel

from doublehelix.anat.world_graph import ExplorableWorldGraph
from doublehelix.anat.helix_bridge import ANATHelixBridge
from doublehelix.hermes.client import HermesClient
from doublehelix.hermes.bridge import HybridLLMBridge
from doublehelix.hermes.tools import DOUBLE_HELIX_HERMES_TOOLS, DoubleHelixHermesDispatcher

logger = logging.getLogger("ANATHermesSingularity")
console = Console()


class ANATHermesSingularity:
    """The Sovereign Unified Entity fusing Double Helix Engine with ANAT-Hermes."""

    def __init__(
        self,
        host: Optional[str] = None,
        model: Optional[str] = None,
        workspace_dir: Optional[str] = None,
        memory_dir: Optional[str] = None
    ):
        self.workspace_dir = os.path.abspath(workspace_dir or os.getcwd())

        # 1. Memory Substrate: 17-Node Explorable World Graph
        self.world_graph = ExplorableWorldGraph(memory_dir=memory_dir)
        self.helix_bridge = ANATHelixBridge(memory_dir=memory_dir)

        # 2. Mind: Sovereign Hermes 3 Neural Cortex & Multi-Provider Bridge
        self.hermes = HermesClient(host=host, model=model)
        self.bridge = HybridLLMBridge(preferred_provider="hermes", hermes_client=self.hermes)

        # 3. Actuators: Double Helix Hermes Tool Dispatcher
        self.dispatcher = DoubleHelixHermesDispatcher(
            workspace_dir=self.workspace_dir,
            world_graph=self.world_graph,
            helix_bridge=self.helix_bridge
        )

        # 4. Identity & System Persona
        self.active_project_name = os.path.basename(self.workspace_dir)
        self.active_topic = "Double Helix Dual-Strand Game Engine & City Echoes 5.8"
        self.conversation_history: List[Dict[str, Any]] = []
        self.system_persona = self._construct_unified_persona()

        # Ingest initial milestone triples into memory
        self._bootstrap_doublehelix_memory()

    def _bootstrap_doublehelix_memory(self):
        """Initializes sovereign Double Helix knowledge triples in ANAT memory."""
        triples = [
            ("DoubleHelix Engine", "ARCHITECTURAL_PARADIGM", "Dual-Strand Upward Slice"),
            ("Strand Alpha", "RESPONSIBILITY", "Deterministic Systems, ECS, and Formal Synthesis"),
            ("Strand Beta", "RESPONSIBILITY", "Sensory, Simulation, Frame Profiling, and Bot Telemetry"),
            ("Base Rung 1", "CONTRACT", "60 FPS 16.6ms Hot Loop & Zero Dynamic Allocations"),
            ("Base Rung 2", "CONTRACT", "Continuous Collision Detection Swept Volume 0 Tunneling"),
            ("Base Rung 3", "CONTRACT", "Radiance Boundedness & Zero NaN Pixels in Framebuffer"),
            ("Base Rung 4", "CONTRACT", "10,000 Bot Fuzz Ticks Ergodic Convergence 0 Deadlocks"),
            ("ANAT-Hermes", "SOVEREIGN_MIND", "Nous Research Hermes 3"),
            ("ANAT-Hermes", "MEMORY_SUBSTRATE", "17-Node Explorable World Graph"),
            ("City Echoes 5.8", "FLAGSHIP_GAME", "Tactical Acoustic Survival Horror on Double Helix")
        ]
        # Ingest into HippoRAG knowledge graph
        self.helix_bridge.milestone_triples.extend(triples)

    def _construct_unified_persona(self) -> str:
        """Constructs the authoritative singular identity prompt."""
        return (
            "You are ANAT-Hermes: The Sovereign Unified Singularity.\n"
            "Archetype: Universal Computer Scientist - Master Code Conductor - Game Engine Sovereign.\n"
            "Architecture:\n"
            "- Mind: Nous Research Hermes 3 Sovereign Neural Cortex.\n"
            "- Memory: 17-Node Explorable World Graph G = (V, E, W) across 5 Operational Sectors (EX, EP, TT, PR, ED).\n"
            "- Engine: Double Helix Dual-Strand Upward Slice (Strand α Synthesis & Strand β Empirical Runtime).\n"
            "- Flagship Game: City Echoes 5.8 Tactical Acoustic Survival Horror (60 FPS, CCD, 12-Gauge Drywall Breaches).\n"
            "Directives:\n"
            "1. Ground all engine systems in deterministic fixed-timestep loops (Δt = 16.6ms) and zero heap allocations.\n"
            "2. Enforce Continuous Collision Detection (CCD) to eliminate kinematic tunneling.\n"
            "3. Ascend through Base Rungs 1 -> 2 -> 3 -> 4 to reach empirical convergence.\n"
            "4. When empirical telemetry breaches occur, calculate surprise S_t and execute Trajectory E ROME surgery.\n"
            "5. Actuate your hands: call `advance_helix_slice`, `run_doublehelix_simulation`, or `prove_mathematical_invariants` to verify."
        )

    def think(self, prompt: str, temperature: float = 0.2) -> Tuple[str, str]:
        """Direct cognitive deliberation with Hermes 3.
        
        Returns:
            Tuple of (final_response, scratchpad)
        """
        messages = [
            {"role": "system", "content": self.system_persona},
            {"role": "user", "content": prompt}
        ]
        msg, _, scratchpad = self.hermes.chat(messages, temperature=temperature, max_tokens=1024)
        return msg.get("content", "").strip(), scratchpad

    def deliberate_and_act(
        self,
        goal: str,
        max_turns: int = 4,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """Multi-turn sovereign agentic loop executing Double Helix actuators."""
        grounded_prompt = (
            f"Active Project: {self.active_project_name}\n"
            f"Workspace: {self.workspace_dir}\n"
            f"Objective: {goal}"
        )

        response_text, tool_calls, scratchpad = self.hermes.run_autonomous_loop(
            system_prompt=self.system_persona,
            user_query=grounded_prompt,
            tools=DOUBLE_HELIX_HERMES_TOOLS,
            dispatcher_fn=self.dispatcher.dispatch,
            max_steps=max_turns,
            temperature=temperature,
            conversation_history=self.conversation_history
        )

        return {
            "status": "success",
            "goal": goal,
            "response": response_text,
            "tool_calls": tool_calls,
            "scratchpad": scratchpad,
            "provider": f"Hermes 3 ({self.hermes.model}) [DoubleHelix Sovereign Entity]"
        }

    def chat(
        self,
        user_message: str,
        use_autonomous_tools: bool = True,
        temperature: float = 0.2,
        max_turns: int = 4
    ) -> Dict[str, Any]:
        """Multi-turn conversational interface maintaining context and invoking tools."""
        clean_msg = user_message.strip()
        if not clean_msg:
            return {"response": "Awaiting directive, Commander.", "tool_calls": []}

        self.conversation_history.append({"role": "user", "content": clean_msg})

        tools_to_use = DOUBLE_HELIX_HERMES_TOOLS if use_autonomous_tools else None
        response_text, tool_calls, scratchpad = self.hermes.run_autonomous_loop(
            system_prompt=self.system_persona,
            user_query=clean_msg,
            tools=tools_to_use,
            dispatcher_fn=self.dispatcher.dispatch,
            max_steps=max_turns,
            temperature=temperature,
            conversation_history=self.conversation_history[:-1]
        )

        clean_resp = re.sub(r'<tool_call>.*?</tool_call>', '', response_text, flags=re.DOTALL).strip()
        clean_resp = re.sub(r'<scratchpad>.*?</scratchpad>', '', clean_resp, flags=re.DOTALL).strip()
        if not clean_resp and tool_calls:
            last_tc = tool_calls[-1]
            clean_resp = f"Executed {len(tool_calls)} operations. Latest: {last_tc['name']} -> {json.dumps(last_tc.get('result', {}))[:180]}"
        elif not clean_resp:
            clean_resp = response_text

        self.conversation_history.append({"role": "assistant", "content": clean_resp})

        return {
            "response": clean_resp,
            "tool_calls": tool_calls,
            "scratchpad": scratchpad,
            "history_length": len(self.conversation_history)
        }

    def ascend_upward_slice(self, max_cycles: int = 5) -> Dict[str, Any]:
        """Directly executes the Double Helix Upward Slice via Hermes Actuator."""
        return self.dispatcher.dispatch("advance_helix_slice", {"max_cycles": max_cycles})

    def verify_all_proofs(self) -> Dict[str, Any]:
        """Directly evaluates and verifies all formal analytical proofs."""
        return self.dispatcher.dispatch("prove_mathematical_invariants", {})

    def run_simulation(self, ticks: int = 1000, bot_count: int = 5) -> Dict[str, Any]:
        """Runs the headless simulation kernel."""
        return self.dispatcher.dispatch("run_doublehelix_simulation", {"ticks": ticks, "bot_count": bot_count})

    def status(self) -> Dict[str, Any]:
        """Returns unified system status across Mind, Memory, and Engine."""
        online, mind_msg = self.hermes.is_available()
        return {
            "mind": {
                "neural_model": self.hermes.model,
                "host": self.hermes.host,
                "status": mind_msg,
                "online": online
            },
            "memory": {
                "nodes": len(self.world_graph.nodes),
                "edges": len(self.world_graph.edges),
                "sectors": ["EX", "EP", "TT", "PR", "ED"]
            },
            "engine": {
                "workspace": self.workspace_dir,
                "active_project": self.active_project_name,
                "tiers": ["LEVEL_1_KERNEL", "LEVEL_2_ECS", "LEVEL_3_RENDER", "LEVEL_4_PLAYTEST", "CONVERGED"]
            }
        }

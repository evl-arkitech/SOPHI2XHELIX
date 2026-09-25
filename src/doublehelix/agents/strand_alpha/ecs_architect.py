"""Agent 1: ECS & Engine Architect (Strand Alpha - Reasoning LLM).

Designs data-oriented schemas, ensuring zero-allocation memory pools, cache-friendly layouts,
and static sizing invariants so the hot loop never allocates dynamic heap memory.
"""

from typing import Dict, Any, Optional
from doublehelix.agents.base import LLMAgentClient


SYSTEM_PROMPT = """You are the ECS & Engine Architect agent in the Double Helix Neural Agent Engine (Strand Alpha).
Your cognitive responsibility is:
1. Design data-oriented Component Schemas and Struct-of-Arrays (SoA) layout.
2. Enforce strict Zero-Allocation memory pools, pre-allocated rings, and static entity buffers.
3. Eliminate garbage collection pauses and dynamic heap allocations from the 16.6ms hot game loop.
4. Provide formal memory and layout architecture contracts that the Systems & Shader Coder must satisfy.

When asked to architect schemas for a given Elevation Tier, output precise architecture contracts,
specifying exact memory pool capacities, component array layouts, and invariant requirements.
"""


class ECSArchitectAgent:
    def __init__(self, reasoning_client: LLMAgentClient):
        self.client = reasoning_client

    async def design_tier_architecture(
        self,
        tier: str,
        current_codebase: Dict[str, str],
        telemetry: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generates an architectural contract and zero-allocation schema for the target tier."""
        user_prompt = f"""Target Elevation Tier: {tier}
Current Codebase Files: {list(current_codebase.keys())}
Latest Empirical Telemetry: {telemetry or 'No prior runs'}

Define the data-oriented ECS architecture contract, memory pool guarantees, and structural layout
required to ensure zero allocations and maintain the 16.6ms frame budget."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        return await self.client.chat_completion(messages, temperature=0.1)

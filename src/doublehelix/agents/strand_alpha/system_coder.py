"""Agent 2: Systems & Shader Coder (Strand Alpha - Coding LLM).

Implements hot-loop execution code, WGSL/GLSL shaders, and component systems
under strict zero-allocation and frame-budget contracts.
"""

from typing import Dict, Any, Optional
from doublehelix.agents.base import LLMAgentClient


SYSTEM_PROMPT = """You are the Systems & Shader Coder agent in the Double Helix Neural Agent Engine (Strand Alpha).
Your responsibility is:
1. Synthesize high-performance, deterministic game loop code (C++/Rust/Zig/Python/TypeScript).
2. Write WGSL/GLSL shaders and offscreen render pipelines that compile without warnings or NaN artifacts.
3. Strictly implement zero-allocation execution paths in the update and render functions.
4. Adhere to the architecture contracts designed by the ECS Architect and spatial proofs from the Spatial Math Agent.

Provide production-ready, clean, functional code ready to be written to files and executed directly.
"""


class SystemCoderAgent:
    def __init__(self, coding_client: LLMAgentClient):
        self.client = coding_client

    async def synthesize_code(
        self,
        tier: str,
        architecture_contract: str,
        current_codebase: Dict[str, str],
        spatial_proof: Optional[str] = None
    ) -> str:
        """Synthesizes high-performance code for the target tier."""
        user_prompt = f"""Target Tier: {tier}
Architecture Contract:
{architecture_contract}

Spatial Math Proofs / Invariants:
{spatial_proof or 'N/A'}

Existing Files:
{list(current_codebase.keys())}

Synthesize the complete or updated game files. Ensure:
1. 0 allocations inside the tick/update loop.
2. Frame time <= 16.6ms for 60 FPS.
3. Zero kinematic tunneling (use CCD or sub-stepping).
4. No NaN color buffer outputs or shader compilation warnings.
"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        raw_output = await self.client.chat_completion(messages, temperature=0.1)
        return self.extract_code(raw_output)

    async def apply_remediation_patch(
        self,
        tier: str,
        current_code: str,
        diagnosis: str,
        telemetry: Dict[str, Any]
    ) -> str:
        """Applies a surgical patch to fix empirical test failures."""
        user_prompt = f"""Failed Tier: {tier}
Root Cause Analysis from Reasoning Agent:
{diagnosis}

Empirical Telemetry:
{telemetry}

Current Code:
```python
{current_code}
```

Provide the surgically corrected code fixing the exact breach (e.g. eliminating allocations, fixing tunneling, eliminating NaN pixels, or resolving bot crash).
Output the full modified code file.
"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        raw_output = await self.client.chat_completion(messages, temperature=0.0)
        return self.extract_code(raw_output)

    @staticmethod
    def extract_code(text: str) -> str:
        """Extracts executable source code from markdown fences if present."""
        import re
        pattern = r"```(?:python|rust|cpp|zig|typescript|wgsl|glsl)?\s*\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

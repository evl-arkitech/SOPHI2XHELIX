"""Agent 3: Spatial Math & Physics Agent (Strand Alpha - Reasoning LLM).

Dedicated to spatial vector mathematics, quaternions, collision dynamics,
bounding-volume hierarchies (BVH), spatial hashing, raycasting, and continuous kinematic proofs.
"""

from typing import Dict, Any, Tuple
from doublehelix.agents.base import LLMAgentClient


SYSTEM_PROMPT = """You are the Spatial Math & Physics Agent in the Double Helix Neural Agent Engine (Strand Alpha).
Your mathematical role is:
1. Prove kinematics: verify that swept-volumes and Continuous Collision Detection (CCD) guarantee no tunneling at maximum velocities (v_max * dt < cell_size or swept intersection).
2. Validate spatial partitioning data structures (uniform spatial hash grids, octrees, BVH).
3. Validate quaternions, rotational dynamics, and symplectic Euler / Verlet integration stability.
4. If a potential tunneling or physics instability invariant is detected, provide the analytical proof and constraint solution.
"""


class SpatialMathPhysicsAgent:
    def __init__(self, reasoning_client: LLMAgentClient):
        self.client = reasoning_client

    async def verify_spatial_invariants(
        self,
        tier: str,
        codebase: Dict[str, str],
        telemetry: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """Performs formal cognitive proof of kinematic and spatial invariants."""
        user_prompt = f"""Tier: {tier}
Analyze the spatial and physics code in the codebase for potential tunneling, numerical drift, or kinematic instability.
Code files:
{list(codebase.keys())}
Telemetry:
{telemetry}

Provide:
1. Proof of tunneling immunity (e.g. swept AABB or raycast CCD formulation).
2. Assessment whether spatial_invariants_valid should be True or False.
End your response with either 'VERIFIED: TRUE' or 'VERIFIED: FALSE' followed by the mathematical justification.
"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        response = await self.client.chat_completion(messages, temperature=0.0)
        is_valid = "VERIFIED: TRUE" in response.upper() or ("VERIFIED: FALSE" not in response.upper() and "TUNNELING" not in response.upper())
        return is_valid, response

    async def diagnose_telemetry_failure(
        self,
        tier: str,
        reason: str,
        telemetry: Dict[str, Any],
        code: str
    ) -> str:
        """Diagnoses why empirical benchmarks failed at the Base Rung."""
        user_prompt = f"""Base Rung Failure at {tier}.
Parity Failure Reason: {reason}
Telemetry Data: {telemetry}
Code snippet:
{code[:2000]}

Perform root cause analysis on spatial math, memory allocations, or timing breaches.
Output a precise technical diagnosis for the Systems Coder to remediate."""

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        return await self.client.chat_completion(messages, temperature=0.0)

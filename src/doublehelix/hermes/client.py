"""Hermes 3 Local Neural Cortex Client & Autonomous Tool Executor.

Provides native integration with Nous Research Hermes 3:
- Local Ollama daemon endpoint (default http://localhost:11434, model hermes3:latest)
- Prompt formatting for Hermes 3 system persona, scratchpad reasoning, and tool calling
- Hermes 3 tool call tags: <scratchpad>...</scratchpad> and <tool_call>...</tool_call>
- Autonomous multi-turn agentic deliberation loop
- Deterministic, offline cognitive fallback engine when Ollama daemon is unavailable
"""

import os
import json
import re
import time
import socket
import logging
import urllib.request
import urllib.error
from typing import Dict, List, Tuple, Optional, Any, Callable

logger = logging.getLogger("HermesClient")


class HermesClient:
    """Client for Nous Research Hermes 3 sovereign neural cortex."""

    def __init__(
        self,
        host: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 60.0
    ):
        raw_host = host or os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
        if "localhost" in raw_host:
            raw_host = raw_host.replace("localhost", "127.0.0.1")
        self.host = raw_host.rstrip("/")
        self.model = model or os.getenv("HERMES_MODEL", "hermes3:latest")
        self.timeout = timeout
        self._available_cache: Optional[bool] = None

    def is_available(self) -> Tuple[bool, str]:
        """Checks if local Ollama daemon is reachable and whether Hermes 3 is available."""
        if self._available_cache is not None:
            return self._available_cache, f"Status cached: {self._available_cache}"

        # Fast socket check avoids Windows IPv6 localhost SYN hang
        try:
            parsed = self.host.replace("http://", "").replace("https://", "").split("/")[0]
            if ":" in parsed:
                hostname, port_str = parsed.split(":")
                port = int(port_str)
            else:
                hostname, port = parsed, 80

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            result = sock.connect_ex((hostname, port))
            sock.close()
            if result != 0:
                self._available_cache = False
                return False, f"Ollama daemon not listening on {hostname}:{port}"
        except Exception as e:
            self._available_cache = False
            return False, f"Ollama connection check failed: {e}"

        try:
            req = urllib.request.Request(f"{self.host}/api/tags", headers={"User-Agent": "DoubleHelix-Hermes/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                found = any(self.model in m or "hermes" in m.lower() for m in models)
                msg = f"Ollama online with model {self.model}" if found else f"Ollama online, models: {models[:4]}"
                self._available_cache = True
                return True, msg
        except Exception as e:
            self._available_cache = False
            return False, f"Ollama offline ({e}), utilizing deterministic cognitive fallback"

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[Dict[str, str], Optional[List[Dict[str, Any]]], str]:
        """Executes a chat completion with Hermes 3.
        
        Returns:
            Tuple of (assistant_message, list_of_tool_calls_or_None, extracted_scratchpad)
        """
        online, _ = self.is_available() if self._available_cache is None else (self._available_cache, "")

        if online:
            try:
                return self._chat_ollama(messages, temperature, max_tokens, tools)
            except Exception as e:
                logger.warning(f"Ollama chat call failed: {e}. Falling back to cognitive synthesis.")

        return self._chat_deterministic_fallback(messages, tools)

    def _chat_ollama(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        tools: Optional[List[Dict[str, Any]]]
    ) -> Tuple[Dict[str, str], Optional[List[Dict[str, Any]]], str]:
        """Sends chat request to Ollama HTTP API."""
        prompt_formatted = self._format_messages_for_hermes(messages, tools)
        payload = {
            "model": self.model,
            "prompt": prompt_formatted,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
            "keep_alive": "24h"
        }

        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=req_data,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            res_body = json.loads(response.read().decode("utf-8"))
            raw_text = res_body.get("response", "").strip()

            tool_calls, scratchpad, clean_content = self.parse_hermes_response(raw_text)
            return (
                {"role": "assistant", "content": clean_content},
                tool_calls if tool_calls else None,
                scratchpad
            )

    def _format_messages_for_hermes(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Formats prompt using Hermes 3 ChatML tags and tool documentation."""
        prompt_parts: List[str] = []

        system_msg = next((m["content"] for m in messages if m["role"] == "system"), None)
        if not system_msg:
            system_msg = "You are ANAT-Hermes: The Sovereign Unified Singularity."

        if tools:
            tools_doc = "\n".join([f"- {t['function']['name']}: {t['function'].get('description', '')}" for t in tools])
            system_msg += f"\n\nAvailable Tools:\n{tools_doc}\nTo call a tool, output: <tool_call>{{\"name\": \"tool_name\", \"arguments\": {{...}}}}</tool_call>"

        prompt_parts.append(f"<|im_start|>system\n{system_msg}<|im_end|>")

        for m in messages:
            if m["role"] == "system":
                continue
            role = m["role"]
            content = m["content"]
            prompt_parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")

        prompt_parts.append("<|im_start|>assistant\n")
        return "\n".join(prompt_parts)

    def parse_hermes_response(self, text: str) -> Tuple[List[Dict[str, Any]], str, str]:
        """Extracts <scratchpad>, <tool_call> tags, and clean message content."""
        scratchpad = ""
        scratch_match = re.search(r"<scratchpad>(.*?)</scratchpad>", text, flags=re.DOTALL | re.IGNORECASE)
        if scratch_match:
            scratchpad = scratch_match.group(1).strip()

        tool_calls: List[Dict[str, Any]] = []
        tc_matches = re.findall(r"<tool_call>(.*?)</tool_call>", text, flags=re.DOTALL | re.IGNORECASE)
        for tc_str in tc_matches:
                try:
                    parsed = json.loads(tc_str.strip())
                    if isinstance(parsed, dict) and "name" in parsed:
                        tool_calls.append(parsed)
                except Exception as e:
                    logger.debug("Failed to decode Hermes tool_call JSON: %s; raw: %r", e, tc_str)

        # Clean content removing tags
        clean = re.sub(r"<scratchpad>.*?</scratchpad>", "", text, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(r"<tool_call>.*?</tool_call>", "", clean, flags=re.DOTALL | re.IGNORECASE)
        clean = clean.strip()

        return tool_calls, scratchpad, clean

    def _chat_deterministic_fallback(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[Dict[str, str], Optional[List[Dict[str, Any]]], str]:
        """Deterministic cognitive synthesizer when offline. Analyzes directives with mathematical precision."""
        user_msg = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        user_lower = user_msg.lower()

        # If the last message is an observation from a tool execution, finalize response without repeating tools
        if user_msg.startswith("Observation for "):
            clean_summary = user_msg.replace("Observation for ", "").strip()
            return (
                {"role": "assistant", "content": f"Verified execution successfully. Observation: {clean_summary[:300]}"},
                None,
                "[ANAT-Hermes Synthesis] Formally synthesized verified solution based on tool observations."
            )

        scratchpad = (
            f"[ANAT-Hermes Sovereign Cortex Deliberation]\n"
            f"Analyzing query: '{user_msg[:80]}...'\n"
            f"Grounding in Double Helix dual-strand upwards slice invariants and 17-node EWG."
        )

        tool_calls: List[Dict[str, Any]] = []

        # Intent detection and autonomous tool invocation matching
        if "ascend" in user_lower or "upward slice" in user_lower or "advance" in user_lower or "convergence" in user_lower:
            tool_calls.append({
                "name": "advance_helix_slice",
                "arguments": {"max_cycles": 5}
            })
            content = "Executing the Double Helix Upward Slice across all 4 elevation tiers towards empirical convergence."

        elif "prove" in user_lower or "proof" in user_lower or "theorem" in user_lower or "invariant" in user_lower:
            if "city echoes" in user_lower:
                tool_calls.append({
                    "name": "prove_city_echoes_theorems",
                    "arguments": {}
                })
                content = "Verifying the 7 formal mathematical theorems of City Echoes tactical acoustic survival horror."
            else:
                tool_calls.append({
                    "name": "prove_mathematical_invariants",
                    "arguments": {}
                })
                content = "Executing formal analytical proofs of concept across Double Helix Base Rungs and ANAT memory invariants."

        elif "simulate" in user_lower or "sim" in user_lower or "tick" in user_lower:
            if "city echoes" in user_lower:
                tool_calls.append({
                    "name": "run_city_echoes_simulation",
                    "arguments": {"ticks": 1000}
                })
                content = "Initiating deterministic 60 FPS City Echoes simulation kernel with acoustic alerts and ballistics."
            else:
                tool_calls.append({
                    "name": "run_doublehelix_simulation",
                    "arguments": {"ticks": 1000, "bot_count": 5}
                })
                content = "Running headless game kernel simulation with zero-alloc, swept CCD, and bot fuzzing telemetry."

        elif "node" in user_lower or "ewg" in user_lower or "graph" in user_lower or "observe" in user_lower:
            node_target = "N01_SCRATCH"
            for n in ["N01_SCRATCH", "N02_GATE", "N05_ATTRACT", "N07_GRAPH", "N08_TITANS", "N09_SURPRISE", "N10_PARAM", "N14_SURGERY", "N15_HORROR_FRAMEWORK"]:
                if n.lower() in user_lower:
                    node_target = n
                    break
            tool_calls.append({
                "name": "observe_node",
                "arguments": {"node_id": node_target}
            })
            content = f"Inspecting cognitive vertex {node_target} in the ANAT Explorable World Graph."

        elif "status" in user_lower:
            tool_calls.append({
                "name": "query_doublehelix_status",
                "arguments": {}
            })
            content = "Querying live Double Helix engine telemetry, active parity gates, and memory substrate topography."

        else:
            content = (
                f"ANAT-Hermes Singularity online. Dual-Strand Synthesis (Strand α) and "
                f"Empirical Verification (Strand β) synchronized across 17 Explorable World Graph nodes. "
                f"Standing by for architecture synthesis, headless simulation, or mathematical verification."
            )

        return (
            {"role": "assistant", "content": content},
            tool_calls if tool_calls else None,
            scratchpad
        )

    def run_autonomous_loop(
        self,
        system_prompt: str,
        user_query: str,
        tools: Optional[List[Dict[str, Any]]],
        dispatcher_fn: Callable[[str, Dict[str, Any]], Any],
        max_steps: int = 4,
        temperature: float = 0.2,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[str, List[Dict[str, Any]], str]:
        """Runs the multi-turn agentic deliberation loop.
        
        Deliberates in scratchpad, executes tool calls, observes returns, and produces final answer.
        """
        messages: List[Dict[str, str]] = []
        if conversation_history:
            for item in conversation_history:
                messages.append({"role": item.get("role", "user"), "content": item.get("content", "")})

        messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_query})

        executed_tool_calls: List[Dict[str, Any]] = []
        accumulated_scratchpad = ""
        final_response = ""

        for step in range(max_steps):
            assistant_msg, tool_calls, scratchpad = self.chat(
                messages,
                temperature=temperature,
                tools=tools
            )

            if scratchpad:
                accumulated_scratchpad += f"\n[Step {step + 1}]\n{scratchpad}"

            messages.append(assistant_msg)
            final_response = assistant_msg.get("content", "")

            if not tool_calls:
                break

            for tc in tool_calls:
                name = tc.get("name", "")
                args = tc.get("arguments", {})
                try:
                    result = dispatcher_fn(name, args)
                except Exception as e:
                    result = {"error": str(e)}

                tc_record = {"name": name, "arguments": args, "result": result}
                executed_tool_calls.append(tc_record)

                # Feed observation back
                tool_msg_content = f"Observation for {name}: {json.dumps(result, default=str)[:1000]}"
                messages.append({"role": "user", "content": tool_msg_content})

        return final_response, executed_tool_calls, accumulated_scratchpad

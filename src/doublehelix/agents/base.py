"""Base Agent infrastructure for Strand Alpha and Strand Beta agents.

Handles structured communication with the Reasoning and Coding LLMs via OpenAI-compatible endpoints,
retaining prefix caching for the game architecture contract across turns.
"""

from typing import List, Dict, Any, Optional
import httpx


class LLMAgentClient:
    """Async HTTP client to communicate with the Reasoning LLM (Port 8001) or Coding LLM (Port 8002)."""

    def __init__(self, base_url: str, model_name: str = "default", api_key: Optional[str] = None, timeout: float = 60.0):
        # Normalize endpoint URL to ensure trailing /chat/completions works cleanly
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.api_key = api_key
        self.timeout = timeout

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        prefix_cache: bool = True
    ) -> str:
        """Sends a chat completion request to the model engine endpoint."""
        url = f"{self.base_url}/chat/completions" if not self.base_url.endswith("/chat/completions") else self.base_url
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if prefix_cache:
            # Tell vLLM / TensorRT-LLM proxy to retain prefix caching for system contracts
            headers["X-Prefix-Cache"] = "true"

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]

"""LLM Provider Backends for Container 1 (Model Engine).

Supports routing to real local/remote inference servers:
- vLLM / TensorRT-LLM (OpenAI-compatible protocol with Prefix Caching)
- Ollama / LocalAI
- Upstream OpenAI / Gemini endpoints
- Direct local model inference
"""

from typing import List, Dict, Any, Optional
import httpx
import logging

logger = logging.getLogger("doublehelix.model_engine.provider")


class UpstreamLLMProvider:
    """Connects to an upstream OpenAI-compatible model server (vLLM, TensorRT-LLM, Ollama, OpenAI)."""

    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        api_key: Optional[str] = None,
        default_model: str = "default-model",
        timeout: float = 60.0
    ):
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.default_model = default_model
        self.timeout = timeout

    async def generate_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        extra_headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Calls the upstream LLM inference server."""
        if not self.endpoint_url:
            raise ValueError(
                "Upstream LLM endpoint URL not configured. Set REASONING_UPSTREAM_URL or CODING_UPSTREAM_URL."
            )

        target_url = self.endpoint_url.rstrip("/")
        if not target_url.endswith("/chat/completions"):
            target_url = f"{target_url}/chat/completions"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if extra_headers:
            headers.update(extra_headers)

        payload: Dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(target_url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()

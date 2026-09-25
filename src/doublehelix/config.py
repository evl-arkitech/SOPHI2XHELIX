"""Configuration settings for DoubleHelix Neural Agent Engine.

Handles environment variable overrides and sensible defaults for Container 1 (Model Engine),
Container 2 (Agent Orchestration), and Container 3 (Headless Game Runtime).
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Container 1: Model Engine
    reasoning_llm_url: str = Field(
        default="http://localhost:8001/v1",
        description="Endpoint for Reasoning LLM (spatial math, quaternions, collision dynamics, profiling analysis)",
        validation_alias="REASONING_LLM_URL"
    )
    coding_llm_url: str = Field(
        default="http://localhost:8002/v1",
        description="Endpoint for Coding LLM (high-throughput C++/Rust/Zig/Python/WGSL game code synthesis)",
        validation_alias="CODING_LLM_URL"
    )
    model_api_key: Optional[str] = Field(
        default=None,
        description="API Key for upstream LLM provider if required (OpenAI, Gemini, vLLM, etc.)",
        validation_alias="MODEL_API_KEY"
    )
    reasoning_model_name: str = Field(
        default="reasoning",
        description="Model name identifier for the reasoning LLM",
        validation_alias="REASONING_MODEL_NAME"
    )
    coding_model_name: str = Field(
        default="coding",
        description="Model name identifier for the coding LLM",
        validation_alias="CODING_MODEL_NAME"
    )

    # Container 2: Helix Orchestrator
    orchestrator_host: str = Field(default="0.0.0.0", validation_alias="ORCHESTRATOR_HOST")
    orchestrator_port: int = Field(default=8000, validation_alias="ORCHESTRATOR_PORT")
    max_cycles_per_tier: int = Field(default=5, validation_alias="MAX_CYCLES_PER_TIER")
    request_timeout: float = Field(default=60.0, validation_alias="REQUEST_TIMEOUT")

    # Container 3: Headless Game Runtime
    runtime_api_url: str = Field(
        default="http://localhost:5000",
        description="Endpoint for Headless Game Simulation Runtime",
        validation_alias="RUNTIME_API_URL"
    )
    runtime_host: str = Field(default="0.0.0.0", validation_alias="RUNTIME_HOST")
    runtime_port: int = Field(default=5000, validation_alias="RUNTIME_PORT")
    work_dir: str = Field(default="/tmp/game_sim", validation_alias="RUNTIME_WORK_DIR")
    default_sim_ticks: int = Field(default=1000, validation_alias="DEFAULT_SIM_TICKS")
    default_bot_count: int = Field(default=5, validation_alias="DEFAULT_BOT_COUNT")
    level4_sim_ticks: int = Field(default=10000, validation_alias="LEVEL4_SIM_TICKS")


settings = Settings()

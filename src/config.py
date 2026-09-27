import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    # API Keys
    JEV_API_KEY = (
        os.getenv("JEV_API_KEY")
        or os.getenv("TYPESAFE_API_KEY", "")
    )
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

    # API endpoints
    NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    # NVIDIA Models (verified active on integrate.api.nvidia.com)
    NVIDIA_FAST_MODEL = os.getenv("NVIDIA_FAST_MODEL", "mistralai/mistral-nemotron")
    NVIDIA_CODING_MODEL = os.getenv("NVIDIA_CODING_MODEL", "mistralai/mistral-nemotron")
    NVIDIA_REASONING_MODEL = os.getenv("NVIDIA_REASONING_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
    NVIDIA_AGENT_MODEL = os.getenv("NVIDIA_AGENT_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")
    NVIDIA_HEAVY_MODEL = os.getenv("NVIDIA_HEAVY_MODEL", "nvidia/nemotron-3-ultra-550b-a55b")

    # OpenRouter Models (Fallback & Direct Route Options)
    OPENROUTER_FALLBACK_MODEL = os.getenv("OPENROUTER_FALLBACK_MODEL", "openrouter/auto")
    OPENROUTER_FAST_MODEL = os.getenv("OPENROUTER_FAST_MODEL", "google/gemini-3.8-flash")
    OPENROUTER_CODING_MODEL = os.getenv("OPENROUTER_CODING_MODEL", "openrouter/auto")
    OPENROUTER_REASONING_MODEL = os.getenv("OPENROUTER_REASONING_MODEL", "openrouter/auto")

    # Baseline Model for Evaluation
    BASELINE_MODEL = os.getenv("BASELINE_MODEL", "openrouter/auto")

    # Routing Thresholds
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.70"))

    # Generation Parameters
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TIMEOUT_SECONDS = float(os.getenv("TIMEOUT_SECONDS", "12.0"))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))

    # Observability / Telemetry
    DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "telemetry.db"))


config = Config()
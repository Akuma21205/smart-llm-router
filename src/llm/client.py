import time
import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from src.config import Config

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Unified LLM Client supporting NVIDIA NIM as primary provider
    and OpenRouter as fallback inference layer, capturing token usage and latency.
    """

    def __init__(self):
        self.nvidia = None
        self.openrouter = None

        if Config.NVIDIA_API_KEY:
            self.nvidia = OpenAI(
                api_key=Config.NVIDIA_API_KEY,
                base_url=Config.NVIDIA_BASE_URL,
                timeout=Config.TIMEOUT_SECONDS,
            )

        if Config.OPENROUTER_API_KEY:
            self.openrouter = OpenAI(
                api_key=Config.OPENROUTER_API_KEY,
                base_url=Config.OPENROUTER_BASE_URL,
                timeout=Config.TIMEOUT_SECONDS,
            )

    def _get_nvidia_model(self, task: str) -> str:
        models = {
            "fast": Config.NVIDIA_FAST_MODEL,
            "coding": Config.NVIDIA_CODING_MODEL,
            "reasoning": Config.NVIDIA_REASONING_MODEL,
            "agent": Config.NVIDIA_AGENT_MODEL,
            "heavy": Config.NVIDIA_HEAVY_MODEL,
        }
        return models.get(task, Config.NVIDIA_REASONING_MODEL)

    def _get_openrouter_model(self, task: str) -> str:
        models = {
            "fast": Config.OPENROUTER_FAST_MODEL,
            "coding": Config.OPENROUTER_CODING_MODEL,
            "reasoning": Config.OPENROUTER_REASONING_MODEL,
        }
        return models.get(task, Config.OPENROUTER_FALLBACK_MODEL)

    def generate(
        self,
        prompt: str,
        task: str = "reasoning",
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Executes generation against NVIDIA NIM primary, falling back to OpenRouter.
        Returns:
            Dict containing content, provider, model, generation_latency_ms,
            input_tokens, output_tokens, fallback_triggered, fallback_reason
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        temperature = temperature if temperature is not None else Config.TEMPERATURE
        max_tokens = max_tokens if max_tokens is not None else Config.MAX_TOKENS

        fallback_reason: Optional[str] = None
        start_time = time.perf_counter()

        # -----------------------------------------
        # 1. NVIDIA PRIMARY
        # -----------------------------------------
        if self.nvidia:
            model = self._get_nvidia_model(task)
            try:
                response = self.nvidia.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000

                content = response.choices[0].message.content or ""
                input_tokens = response.usage.prompt_tokens if response.usage else None
                output_tokens = response.usage.completion_tokens if response.usage else None

                return {
                    "provider": "nvidia",
                    "model": model,
                    "content": content,
                    "generation_latency_ms": elapsed_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "fallback_triggered": False,
                    "fallback_reason": None,
                }

            except Exception as e:
                logger.warning(f"[NVIDIA FAILED] {model}: {e}")
                fallback_reason = f"NVIDIA failed ({model}): {str(e)}"

        # -----------------------------------------
        # 2. OPENROUTER FALLBACK
        # -----------------------------------------
        if self.openrouter:
            fallback_start = time.perf_counter()
            model = self._get_openrouter_model(task)
            try:
                response = self.openrouter.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                elapsed_ms = (time.perf_counter() - fallback_start) * 1000

                content = response.choices[0].message.content or ""
                input_tokens = response.usage.prompt_tokens if response.usage else None
                output_tokens = response.usage.completion_tokens if response.usage else None

                return {
                    "provider": "openrouter",
                    "model": model,
                    "content": content,
                    "generation_latency_ms": elapsed_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "fallback_triggered": True,
                    "fallback_reason": fallback_reason or "Used OpenRouter provider",
                }

            except Exception as e:
                logger.error(f"[OPENROUTER FAILED] {model}: {e}")
                fallback_reason = f"All providers failed. OpenRouter error: {str(e)}"

        raise RuntimeError(f"All configured LLM providers failed. Last error: {fallback_reason}")
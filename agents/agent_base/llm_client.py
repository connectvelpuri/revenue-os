"""LLM inference client with tier management and fallback chains.

Supports OpenRouter (auto-routing) and Anthropic directly.
Fallback chain: primary → fallback model → rule-based → graceful degradation.
"""

from __future__ import annotations

import json
import os
from typing import Any, Optional


class LLMClient:
    """LLM inference with tier-aware routing and fallback.

    Usage:
        client = LLMClient(provider="openrouter", tier="complex")
        result = client.complete(system_prompt="...", user_prompt="...")
    """

    TIER_MODELS = {
        "complex": {
            "openrouter": "openrouter/free",
            "anthropic": "claude-opus-4-20250514",
            "nvidia": "minimaxai/minimax-m3",
        },
        "moderate": {
            "openrouter": "openrouter/free",
            "anthropic": "claude-sonnet-4-20250514",
            "nvidia": "minimaxai/minimax-m3",
        },
        "simple": {
            "openrouter": "openrouter/free",
            "anthropic": "claude-haiku-3-5-20241022",
            "nvidia": "minimaxai/minimax-m3",
        },
    }

    def __init__(
        self,
        provider: str = "openrouter",
        tier: str = "moderate",
        temperature: float = 0.3,
        max_tokens: int = 4000,
        fallback_tier: str = "simple",
    ):
        self.provider = provider
        self.tier = tier
        self.fallback_tier = fallback_tier
        self.temperature = temperature
        self.max_tokens = max_tokens

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> LLMResult:
        """Run LLM completion with fallback chain."""
        result = self._try_provider(system_prompt, user_prompt, temperature, max_tokens)
        if result.success:
            return result
        result = self._try_fallback(system_prompt, user_prompt, temperature, max_tokens)
        if result.success:
            result.used_fallback = True
            return result
        return self._rule_based_fallback(system_prompt, user_prompt)

    #  Internal

    def _try_provider(self, system_prompt: str, user_prompt: str, temperature: float | None, max_tokens: int | None) -> LLMResult:
        model = self.TIER_MODELS.get(self.tier, {}).get(self.provider)
        if not model:
            return LLMResult(success=False, error=f"No model for tier={self.tier} provider={self.provider}")
        if self.provider == "openrouter":
            return self._call_openrouter(model, system_prompt, user_prompt, temperature, max_tokens)
        elif self.provider == "anthropic":
            return self._call_anthropic(model, system_prompt, user_prompt, temperature, max_tokens)
        elif self.provider == "nvidia":
            return self._call_nvidia(model, system_prompt, user_prompt, temperature, max_tokens)
        return LLMResult(success=False, error=f"Unknown provider: {self.provider}")

    def _try_fallback(self, system_prompt: str, user_prompt: str, temperature: float | None, max_tokens: int | None) -> LLMResult:
        # Try OpenRouter first, then Anthropic, then NVIDIA NIM
        for fb_provider in ["anthropic", "nvidia"]:
            if fb_provider == self.provider:
                continue
            model = self.TIER_MODELS.get(self.fallback_tier, {}).get(fb_provider)
            if not model:
                continue
            if fb_provider == "openrouter":
                result = self._call_openrouter(model, system_prompt, user_prompt, temperature, max_tokens)
            elif fb_provider == "anthropic":
                result = self._call_anthropic(model, system_prompt, user_prompt, temperature, max_tokens)
            elif fb_provider == "nvidia":
                result = self._call_nvidia(model, system_prompt, user_prompt, temperature, max_tokens)
            else:
                continue
            if result.success:
                result.used_fallback = True
                return result
        return LLMResult(success=False, error="All providers failed")

    def _call_openrouter(self, model: str, system: str, user: str, temperature: float | None, max_tokens: int | None) -> LLMResult:
        try:
            import openai
            client = openai.OpenAI(
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
            )
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            text = resp.choices[0].message.content or ""
            return LLMResult(success=True, text=text, model=model, usage=resp.usage.model_dump() if resp.usage else {})
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                error_msg = "OpenRouter API key is invalid or deactivated. Generate a new key at https://openrouter.ai/keys"
            elif "402" in error_msg or "insufficient" in error_msg.lower():
                error_msg = "OpenRouter account has insufficient credits. Add funds at https://openrouter.ai/settings/credits"
            elif "429" in error_msg or "rate" in error_msg.lower():
                error_msg = "OpenRouter rate limit exceeded. Try again in a few seconds."
            return LLMResult(success=False, error=error_msg)

    def _call_anthropic(self, model: str, system: str, user: str, temperature: float | None, max_tokens: int | None) -> LLMResult:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            resp = client.messages.create(
                model=model,
                system=system,
                messages=[{"role": "user", "content": user}],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            text = resp.content[0].text if resp.content else ""
            return LLMResult(success=True, text=text, model=model, usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens})
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                error_msg = "OpenRouter API key is invalid or deactivated. Generate a new key at https://openrouter.ai/keys"
            elif "402" in error_msg or "insufficient" in error_msg.lower():
                error_msg = "OpenRouter account has insufficient credits. Add funds at https://openrouter.ai/settings/credits"
            elif "429" in error_msg or "rate" in error_msg.lower():
                error_msg = "OpenRouter rate limit exceeded. Try again in a few seconds."
            return LLMResult(success=False, error=error_msg)

    def _call_nvidia(self, model, system, user, temperature, max_tokens):
        """Call NVIDIA NIM API."""
        try:
            import openai
            client = openai.OpenAI(
                api_key=os.getenv("NVIDIA_NIM_API_KEY"),
                base_url="https://integrate.api.nvidia.com/v1",
            )
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            text = resp.choices[0].message.content or ""
            return LLMResult(success=True, text=text, model=model, usage=resp.usage.model_dump() if resp.usage else {})
        except Exception as e:
            err_msg = str(e)
            if "403" in err_msg:
                err_msg = "NVIDIA NIM authorization failed. Check your API key."
            return LLMResult(success=False, error=err_msg)


    def _rule_based_fallback(self, system: str, user: str) -> LLMResult:
        return LLMResult(
            success=True,
            text=f"[RULE-BASED FALLBACK] All LLM providers unavailable.\n  System: {system[:200]}\n  User: {user[:200]}",
            model="rule-based",
            used_fallback=True,
        )

    def format_json(self, text: str) -> dict[str, Any] | None:
        """Try to extract JSON from LLM output."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            import re
            match = re.search(r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            return None


class LLMResult:
    def __init__(
        self,
        success: bool,
        text: str = "",
        error: str = "",
        model: str = "",
        usage: dict | None = None,
        used_fallback: bool = False,
    ):
        self.success = success
        self.text = text
        self.error = error
        self.model = model
        self.usage = usage or {}
        self.used_fallback = used_fallback
_MODEL_TIERS = {
    "complex": {
        "openrouter": "openrouter/free",
        "anthropic": "claude-opus-4-20250514",
    },
    "analysis": {
        "openrouter": "openrouter/free",
        "anthropic": "claude-sonnet-4-20250514",
    },
    "simple": {
        "openrouter": "openrouter/free",
        "anthropic": "claude-haiku-3-5-20241022",
    },
}

# Free model candidates (OpenRouter rates these at $0):
# nvidia/nemotron-3-ultra-550b-a55b:free  - 550B params, 1M ctx - best for complex reasoning
# nvidia/nemotron-3-super-120b-a12b:free  - 120B params, 1M ctx - best for analysis
# nousresearch/hermes-3-llama-3.1-405b:free - 405B params - best for instruction following
# meta-llama/llama-3.3-70b-instruct:free  - 70B params - reliable general purpose
# openrouter/free - auto-routes to best available free model

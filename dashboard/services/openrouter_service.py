import json
import os
import time
from collections.abc import Callable
from typing import Annotated, Any, TypeVar

import httpx
import streamlit as st
from pydantic import BaseModel, Field

from dashboard.data.models.ad_copy import AdCopySchema
from dashboard.data.store import ad_copy_store

T = TypeVar("T")


class AIResponseSchema(BaseModel):
    campaign_name: Annotated[str, Field(min_length=1, max_length=100)]


class AdCopyRequestSchema(BaseModel):
    product_name: Annotated[str, Field(min_length=1)]
    target_audience: Annotated[str, Field(min_length=1)]
    key_features: Annotated[list[str], Field(min_length=1)]
    tone: Annotated[str, Field(default="Professional")]


def with_retry(
    func: Callable[..., T],
    max_retries: int = 3,
    retry_delay_s: int = 2,
) -> T:
    """Execute a function with retry logic."""
    retries = 0
    last_exception = None

    while retries < max_retries:
        try:
            return func()
        except Exception as e:  # noqa: BLE001
            last_exception = e
            retries += 1
            if retries < max_retries:
                time.sleep(retry_delay_s)

    raise last_exception


@st.cache_data(ttl=3600)
def generate_campaign_name(product_type: str, target_audience: str) -> str:
    """Generate a campaign name using OpenRouter.ai API with caching."""
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        st.error(
            "OpenRouter API key not found. "
            "Set OPENROUTER_API_KEY environment variable.",
        )
        return f"Campaign for {product_type}"

    prompt = f"""
    Generate a creative and professional campaign name for:
    - Product/Service: {product_type}
    - Target Audience: {target_audience}

    Provide only the campaign name as a short, catchy phrase (max 5 words).
    """

    def make_request() -> str:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a marketing expert that generates concise, "
                            "creative campaign names."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=15.0,
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip().strip("\"'")

    try:
        return with_retry(make_request)
    except Exception as e:  # noqa: BLE001
        st.warning(f"Failed to generate campaign name: {e!s}")
        return f"Campaign for {product_type}"


@st.cache_data(ttl=3600)
def generate_ad_copy(
    campaign_id: str,
    request: AdCopyRequestSchema,
) -> AdCopySchema:
    """Generate ad copy using OpenRouter.ai API with caching."""
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        st.error(
            "OpenRouter API key not found. "
            "Set OPENROUTER_API_KEY environment variable.",
        )
        return AdCopySchema(
            campaign_id=campaign_id,
            headline=f"{request.product_name} - Perfect for {request.target_audience}",
            description="Check out our amazing product with its great features!",
            call_to_action="Learn More",
            is_ai_generated=False,
        )

    features_text = ", ".join(request.key_features)
    prompt = f"""
    Generate compelling ad copy for:
    - Product: {request.product_name}
    - Target Audience: {request.target_audience}
    - Key Features: {features_text}
    - Tone: {request.tone}

    Return the response as a JSON object with these fields:
    - headline: A catchy headline (max 50 chars)
    - description: Compelling description (max 200 chars)
    - call_to_action: Clear CTA (max 15 chars)
    """

    def make_request() -> dict[str, Any]:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a marketing expert that creates "
                            "compelling ad copy. Respond only with the "
                            "requested JSON format."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=15.0,
        )
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        return json.loads(content)

    try:
        result = with_retry(make_request)
        ad_copy = AdCopySchema(
            campaign_id=campaign_id,
            headline=result.get("headline", ""),
            description=result.get("description", ""),
            call_to_action=result.get("call_to_action", "Learn More"),
            is_ai_generated=True,
        )

        # Store the generated ad copy
        ad_copy_store.add(ad_copy)
    except Exception as e:  # noqa: BLE001
        st.warning(f"Failed to generate ad copy: {e!s}")
        return AdCopySchema(
            campaign_id=campaign_id,
            headline=f"{request.product_name} - Perfect for {request.target_audience}",
            description="Check out our amazing product with its great features!",
            call_to_action="Learn More",
            is_ai_generated=False,
        )
    else:
        return ad_copy

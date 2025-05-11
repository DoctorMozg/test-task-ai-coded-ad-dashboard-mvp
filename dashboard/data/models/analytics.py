from datetime import date
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class MetricsSchema(BaseModel):
    impressions: Annotated[int, Field(ge=0, description="Number of impressions")]
    clicks: Annotated[int, Field(ge=0, description="Number of clicks")]
    ctr_pct: Annotated[
        float,
        Field(ge=0, le=100, description="Click-through rate percentage"),
    ]
    cost_usd: Annotated[float, Field(ge=0, description="Cost spent in USD")]


class CampaignAnalyticsSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for analytics record",
        ),
    ]
    campaign_id: Annotated[str, Field(description="ID of the campaign")]
    date: Annotated[date, Field(description="Date of the analytics data")]
    metrics: Annotated[MetricsSchema, Field(description="Campaign metrics")]

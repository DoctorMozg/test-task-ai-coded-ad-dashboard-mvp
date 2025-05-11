from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class AdBannerSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the banner",
        ),
    ]
    name: Annotated[str, Field(min_length=1, max_length=100)]
    image_url: Annotated[str, Field(description="URL to the banner image")]
    width_px: Annotated[int, Field(gt=0, description="Width of the banner in pixels")]
    height_px: Annotated[int, Field(gt=0, description="Height of the banner in pixels")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    created_by: Annotated[str, Field(description="User ID of creator")]


class CampaignStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    REJECTED = "rejected"


class CampaignSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the campaign",
        ),
    ]
    name: Annotated[str, Field(min_length=1, max_length=100)]
    banner_id: Annotated[str, Field(description="ID of the associated banner")]
    targeting_id: Annotated[str, Field(description="ID of the associated targeting")]
    status: Annotated[CampaignStatusEnum, Field(default=CampaignStatusEnum.DRAFT)]
    budget_usd: Annotated[float, Field(gt=0, description="Campaign budget in USD")]
    start_date: Annotated[datetime, Field(description="Campaign start date and time")]
    end_date: Annotated[
        datetime | None,
        Field(default=None, description="Campaign end date and time"),
    ]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    created_by: Annotated[str, Field(description="User ID of creator")]
    updated_at: Annotated[datetime, Field(default_factory=datetime.now)]


class CampaignListItemSchema(BaseModel):
    id: Annotated[str, Field(description="Campaign ID")]
    name: Annotated[str, Field(description="Campaign name")]
    status: Annotated[CampaignStatusEnum, Field(description="Campaign status")]
    budget_usd: Annotated[float, Field(description="Campaign budget")]
    start_date: Annotated[datetime, Field(description="Start date")]
    created_at: Annotated[datetime, Field(description="Creation date")]

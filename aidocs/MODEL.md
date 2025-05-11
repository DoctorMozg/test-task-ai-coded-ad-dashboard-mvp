# Data Models for Advertising Dashboard MVP

## User Model

```python
from uuid import uuid4
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated

class UserSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the user")]
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")]
    password_hash: Annotated[str, Field(description="Hashed password")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    last_login: Annotated[datetime | None, Field(default=None)]
```

## Ad Banner Model

```python
class AdBannerSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the banner")]
    name: Annotated[str, Field(min_length=1, max_length=100)]
    image_url: Annotated[str, Field(description="URL to the banner image")]
    width_px: Annotated[int, Field(gt=0, description="Width of the banner in pixels")]
    height_px: Annotated[int, Field(gt=0, description="Height of the banner in pixels")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    created_by: Annotated[str, Field(description="User ID of creator")]
```

## Audience Targeting Model

```python
class AgeRangeSchema(BaseModel):
    min_age: Annotated[int, Field(ge=13, le=100, description="Minimum age for targeting")]
    max_age: Annotated[int, Field(ge=13, le=100, description="Maximum age for targeting")]

class LocationSchema(BaseModel):
    country: Annotated[str, Field(description="Country code (ISO 3166-1 alpha-2)")]
    region: Annotated[str | None, Field(default=None, description="State, province, or region")]
    city: Annotated[str | None, Field(default=None, description="City name")]

class InterestSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the interest")]
    name: Annotated[str, Field(min_length=1, max_length=50, description="Interest name")]
    category: Annotated[str | None, Field(default=None, description="Category of interest")]

class AudienceTargetingSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the targeting")]
    age_range: Annotated[AgeRangeSchema, Field(description="Age range targeting")]
    locations: Annotated[list[LocationSchema], Field(min_items=1, description="Locations for targeting")]
    interests: Annotated[list[str], Field(description="List of interest IDs")]
```

## Campaign Model

```python
class CampaignStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    REJECTED = "rejected"

class CampaignSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the campaign")]
    name: Annotated[str, Field(min_length=1, max_length=100)]
    banner_id: Annotated[str, Field(description="ID of the associated banner")]
    targeting_id: Annotated[str, Field(description="ID of the associated targeting")]
    status: Annotated[CampaignStatusEnum, Field(default=CampaignStatusEnum.DRAFT)]
    budget_usd: Annotated[float, Field(gt=0, description="Campaign budget in USD")]
    start_date: Annotated[datetime, Field(description="Campaign start date and time")]
    end_date: Annotated[datetime | None, Field(default=None, description="Campaign end date and time")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    created_by: Annotated[str, Field(description="User ID of creator")]
    updated_at: Annotated[datetime, Field(default_factory=datetime.now)]
```

## Basic Analytics Model

```python
class MetricsSchema(BaseModel):
    impressions: Annotated[int, Field(ge=0, description="Number of impressions")]
    clicks: Annotated[int, Field(ge=0, description="Number of clicks")]
    ctr_pct: Annotated[float, Field(ge=0, le=100, description="Click-through rate percentage")]
    cost_usd: Annotated[float, Field(ge=0, description="Cost spent in USD")]

class CampaignAnalyticsSchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for analytics record")]
    campaign_id: Annotated[str, Field(description="ID of the campaign")]
    date: Annotated[date, Field(description="Date of the analytics data")]
    metrics: Annotated[MetricsSchema, Field(description="Campaign metrics")]
```

## AI-Generated Content Model with OpenRouter.ai

```python
class AdCopySchema(BaseModel):
    id: Annotated[str, Field(default_factory=uuid4, description="Unique identifier for the ad copy")]
    campaign_id: Annotated[str, Field(description="ID of the associated campaign")]
    headline: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(min_length=1, max_length=500)]
    call_to_action: Annotated[str, Field(min_length=1, max_length=50)]
    generated_at: Annotated[datetime, Field(default_factory=datetime.now)]
    is_ai_generated: Annotated[bool, Field(default=True)]
```

## In-Memory Data Structure

The MVP implementation uses Python's in-memory data structures:

```python
# Example in-memory storage structure
class InMemoryStorage:
    def __init__(self):
        self.users = {}  # Indexed by user_id
        self.campaigns = {}  # Indexed by campaign_id
        self.banners = {}  # Indexed by banner_id
        self.targeting = {}  # Indexed by targeting_id
        self.analytics = {}  # Indexed by analytics_id
        self.ad_copies = {}  # Indexed by ad_copy_id

        # Secondary indices for efficient lookups
        self.users_by_username = {}
        self.users_by_email = {}
        self.campaigns_by_user = {}  # user_id -> list of campaign_ids
```

## Implementation Notes

- All models use Pydantic for validation and type checking
- UUID4 is used for all entity IDs
- In-memory storage provides fast access during the MVP phase
- The structure supports the ability to transition to a database in the future
- Memory usage should be monitored and limited for larger datasets
- For persistence between runs, implement optional JSON serialization/deserialization

## OpenRouter.ai Integration

The AI-Generated Content Model is designed to work with OpenRouter.ai:

- Ad copy generation using LLM capabilities
- Campaign name suggestions
- Performance insights generation
- Audience targeting recommendations

This model structure provides a solid foundation for the Advertising Dashboard MVP while keeping implementation simple and focused on core functionality.

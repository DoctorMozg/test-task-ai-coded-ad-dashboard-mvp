from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class AgeRangeSchema(BaseModel):
    min_age: Annotated[
        int,
        Field(ge=13, le=100, description="Minimum age for targeting"),
    ]
    max_age: Annotated[
        int,
        Field(ge=13, le=100, description="Maximum age for targeting"),
    ]


class LocationSchema(BaseModel):
    country: Annotated[str, Field(description="Country code (ISO 3166-1 alpha-2)")]
    region: Annotated[
        str | None,
        Field(default=None, description="State, province, or region"),
    ]
    city: Annotated[str | None, Field(default=None, description="City name")]


class InterestSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the interest",
        ),
    ]
    name: Annotated[
        str,
        Field(min_length=1, max_length=50, description="Interest name"),
    ]
    category: Annotated[
        str | None,
        Field(default=None, description="Category of interest"),
    ]


class AudienceTargetingSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the targeting",
        ),
    ]
    age_range: Annotated[AgeRangeSchema, Field(description="Age range targeting")]
    locations: Annotated[
        list[LocationSchema],
        Field(min_items=1, description="Locations for targeting"),
    ]
    interests: Annotated[list[str], Field(description="List of interest IDs")]

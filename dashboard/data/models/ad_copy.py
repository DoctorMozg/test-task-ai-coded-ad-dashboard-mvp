from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class AdCopySchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the ad copy",
        ),
    ]
    campaign_id: Annotated[str, Field(description="ID of the associated campaign")]
    headline: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str, Field(min_length=1, max_length=500)]
    call_to_action: Annotated[str, Field(min_length=1, max_length=50)]
    generated_at: Annotated[datetime, Field(default_factory=datetime.now)]
    is_ai_generated: Annotated[bool, Field(default=True)]

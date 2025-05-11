from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: Annotated[
        str,
        Field(
            default_factory=lambda: str(uuid4()),
            description="Unique identifier for the user",
        ),
    ]
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[
        str,
        Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    ]
    password_hash: Annotated[str, Field(description="Hashed password")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now)]
    last_login: Annotated[datetime | None, Field(default=None)]


class UserLoginSchema(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(min_length=8)]


class UserRegistrationSchema(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: Annotated[
        str,
        Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"),
    ]
    password: Annotated[str, Field(min_length=8)]
    password_confirm: Annotated[str, Field(min_length=8)]

from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Literal

class CampaignBase(BaseModel):
    name: str
    status: Literal["draft", "active", "paused"]

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    name: str | None = None
    status: Literal["draft", "active", "paused"] | None = None

class CampaignResponse(CampaignBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True # enables ORM mode
    )


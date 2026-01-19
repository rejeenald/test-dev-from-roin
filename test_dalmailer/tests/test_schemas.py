import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse
)


def test_campaign_create_valid():
    campaign = CampaignCreate(
        name="Summer Sale",
        status="active"
    )

    assert campaign.name == "Summer Sale"
    assert campaign.status == "active"


def test_campaign_create_invalid_status():
    with pytest.raises(ValidationError):
        CampaignCreate(
            name="Bad Campaign",
            status="running"  # not allowed
        )

def test_campaign_update_partial():
    campaign = CampaignUpdate(status="paused")
    assert campaign.status == "paused"
    assert campaign.name is None

def test_campaign_update_invalid_status():
    with pytest.raises(ValidationError):
        CampaignUpdate(status="deleted")

def test_campaign_response_from_orm():
    orm_obj = FakeCampaignORM()
    campaign = CampaignResponse.model_validate(orm_obj)
    assert campaign.id == 1
    assert campaign.name == "Winter Sale"
    assert campaign.status == "draft"
    assert campaign.created_at.year == 2025

def test_campaign_response_missing_field():
    with pytest.raises(ValidationError):
        CampaignResponse(
            id=1,
            name="Invalid",
            status="active",
            created_at=datetime.now(timezone.utc)
            # updated_at missing
        )


class FakeCampaignORM:
    def __init__(self):
        self.id = 1
        self.name = "Winter Sale"
        self.status = "draft"
        self.created_at = datetime(2025, 1, 1, 10, 0, 0)
        self.updated_at = datetime(2025, 1, 2, 12, 0, 0)



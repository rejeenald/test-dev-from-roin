import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.crud.campaign import (
    create_campaign,
    get_campaign_by_id,
    get_campaign_list,
    update_campaign,
    delete_campaign,
)

# -------------------------
# Test Database (SQLite)
# -------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# -------------------------
# Tests
# -------------------------
def test_create_campaign(db):
    payload = CampaignCreate(name="Summer Sale", status="active")
    campaign = create_campaign(db, payload)
    assert campaign.id is not None
    assert campaign.name == "Summer Sale"
    assert campaign.status == "active"

def test_get_campaign_by_id(db):
    campaign = create_campaign(db, CampaignCreate(name="Winter Sale", status="draft"))
    result = get_campaign_by_id(db, campaign.id)
    assert result is not None
    assert result.id == campaign.id

def test_get_campaign_by_id_missing_id(db):
    with pytest.raises(ValueError):
        get_campaign_by_id(db, None)

def test_get_campaign_list(db):
    create_campaign(db, CampaignCreate(name="C1", status="active"))
    create_campaign(db, CampaignCreate(name="C2", status="paused"))
    campaigns = get_campaign_list(db)
    assert len(campaigns) == 2


def test_update_campaign(db):
    campaign = create_campaign(db, CampaignCreate(name="Old Name", status="draft"))
    update = CampaignUpdate(name="New Name", status="active")
    updated = update_campaign(db, campaign.id, update)
    assert updated.name == "New Name"
    assert updated.status == "active"

def test_update_campaign_not_found(db):
    result = update_campaign(db, 999, CampaignUpdate(status="active"))
    assert result is None

def test_delete_campaign(db):
    campaign = create_campaign(db, CampaignCreate(name="To Delete", status="active"))
    result = delete_campaign(db, campaign.id)
    assert result is True
    assert get_campaign_by_id(db, campaign.id) is None

def test_delete_campaign_not_found(db):
    result = delete_campaign(db, 999)
    assert result is False

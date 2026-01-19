import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.api.campaign import router as campaign_router
from app.main import app

# -------------------------
# Test Database Setup
# -------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    app = FastAPI()
    app.include_router(campaign_router)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)

# -------------------------
# Tests
# -------------------------

def test_create_campaign(client):
    response = client.post(
        "/campaign/create",
        json={
            "name": "Summer Sale",
            "status": "active",
        },
    )

    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Summer Sale"
    assert data["status"] == "active"
    assert "created_at" in data
    assert "updated_at" in data


def test_list_campaigns(client):
    client.post("/campaign/create", json={"name": "C1", "status": "active"})
    client.post("/campaign/create", json={"name": "C2", "status": "paused"})
    
    response = client.get("/campaign/list")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "C1"
    assert data[1]["name"] == "C2"


def test_get_campaign_by_id(client):
    create = client.post(
        "/campaign/create",
        json={"name": "Winter Sale", "status": "draft"},
    )

    campaign_id = create.json()["id"]
    response = client.get(f"/campaign/{campaign_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == campaign_id
    assert data["name"] == "Winter Sale"


def test_get_campaign_by_id_not_found(client):
    response = client.get("/campaign/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Campaign not found"


def test_delete_campaign(client):
    create = client.post(
        "/campaign/create",
        json={"name": "To Delete", "status": "active"},
    )

    campaign_id = create.json()["id"]
    response = client.delete(f"/campaign/{campaign_id}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Campaign {campaign_id} deleted successfully"

    # Verify deletion
    response = client.get(f"/campaign/{campaign_id}")
    assert response.status_code == 404


def test_delete_campaign_not_found(client):
    response = client.delete("/campaign/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Campaign not found"

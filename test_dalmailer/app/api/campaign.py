from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from app.database import get_db
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from app.crud import campaign as campaign_crud
from app.core.security import verify_api_key

router = APIRouter(
    prefix="/campaign",
    tags=["campaigns"],
    # dependencies=[Depends(verify_api_key)]
)

@router.post("/create", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    return campaign_crud.create_campaign(db, campaign)

@router.get("/list", response_model=list[CampaignResponse])
def list_campaigns(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return campaign_crud.get_campaign_list(db, skip=skip, limit=limit)

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign_by_id(campaign_id: int, db: Session = Depends(get_db)):
    db_campaign = campaign_crud.get_campaign_by_id(db, campaign_id)
    if db_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return db_campaign

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    success = campaign_crud.delete_campaign(db, campaign_id)
    if not success:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"message": f"Campaign {campaign_id} deleted successfully"}
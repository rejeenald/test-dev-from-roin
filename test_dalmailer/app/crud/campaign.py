from sqlalchemy.orm import Session
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignResponse, CampaignUpdate
from typing import List, Optional       


def create_campaign(db: Session, campaign: CampaignCreate) -> CampaignResponse:
    db_campaign = Campaign(**campaign.model_dump())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def get_campaign_by_id(db: Session, campaign_id: int = None) -> Optional[Campaign]:
    if not campaign_id:
        raise ValueError("campaign_id must be provided")
    
    q = db.query(Campaign)

    if campaign_id:
        q = q.filter(Campaign.id == campaign_id)

    return q.first()

def get_campaign_list(db: Session, skip: int = 0, limit: int = 100) -> List[Campaign]:
    return db.query(Campaign).offset(skip).limit(limit).all()

def update_campaign(db: Session, campaign_id: int, campaign_update: CampaignUpdate) -> Optional[Campaign]:
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not db_campaign:
        return None

    for key, value in campaign_update.model_dump().items():
        # this will update only provided fields
        # setattr is used to set attribute dynamically
        setattr(db_campaign, key, value)

    db.commit()
    db.refresh(db_campaign)
    return db_campaign

def delete_campaign(db: Session, campaign_id: int) -> bool:
    db_campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not db_campaign:
        return False

    db.delete(db_campaign)
    db.commit()
    return True
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session  
from app.core.security import verify_api_key
from app.database import get_db, Base, engine
from app.api import campaign

app = FastAPI(
    title="DalMailer",
    description="DalMailer is a backend-driven email automation platform focused on reliable outbound email workflows for B2B companies. The system handles things like campaign logic, email queues, lead data, and automation flows.",
    version="1.0.0"
)


@app.get("/health", dependencies=[Depends(verify_api_key)])
def health_check(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "db_connected": db is not None
    }

Base.metadata.create_all(bind=engine)

app.include_router(store.router)    
app.include_router(campaign.router)    

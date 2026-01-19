from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, nullable=False)  # e.g., "draft", "active", "paused"
    created_at = Column(DateTime, default=func.now(), onupdate=None, nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
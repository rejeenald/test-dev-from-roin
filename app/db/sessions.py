from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import Settings



Base = declarative_base()
settings = Settings()
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args={},
)

def init_session():
    global engine, SessionLocal
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

def get_db():
    init_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

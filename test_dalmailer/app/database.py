from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path
import os

# Get the current directory (app folder)
CURRENT_DIR = Path(__file__).resolve().parent

# Load environment variables from .env
load_dotenv(CURRENT_DIR / ".env")

PRODUCTION = True

# Fetch variables
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")


if PRODUCTION:
    DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
else:
    DATABASE_URL = "sqlite:///./dalmailer.db"

# manages the DB connection
engine = create_engine(DATABASE_URL)

# creates new sessions for interacting with the DB
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# base class for declarative models
Base = declarative_base()


# non-negotiable function to get DB session
# to prevent connection leaks
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




import os
from urllib.parse import quote_plus

def is_production():
    """Determine if the environment is production based on an environment variable."""
    return os.getenv("RENDER") == "true"

# Load .env only in development
if not is_production():
    from dotenv import load_dotenv
    from pathlib import Path

    CURRENT_DIR = Path(__file__).resolve().parent
    load_dotenv(CURRENT_DIR / ".env")

class Settings:
    """Configuration settings for the application."""
    PRODUCTION: bool = True#is_production()
    DB_USER: str = os.environ["DB_USER"]
    DB_PASSWORD: str = quote_plus(os.environ["DB_PASSWORD"])
    DB_HOST: str = os.environ["DB_HOST"]
    DB_PORT: str = os.getenv("DB_PORT", "6543")
    DB_NAME: str = os.environ["DB_NAME"]
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct the database URL based on the environment."""
        if self.PRODUCTION:
            return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
        else:
            return "sqlite:///./dalmailer.db"
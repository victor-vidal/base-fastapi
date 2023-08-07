import os
from typing import List

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

ENV: str = ""

class Configs(BaseSettings):
    # base
    ENV: str = os.getenv("ENV", "dev")
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "base-fastapi"
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
    }

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 60 minutes * 24 hours * 30 days = 30 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # analytics database config
    ANALYTICS_DB: str = os.getenv(f"ANALYTICS_DB", "postgresql")
    ANALYTICS_DB_USER: str = os.getenv(f"ANALYTICS_DB_USER")
    ANALYTICS_DB_PASSWORD: str = os.getenv(f"ANALYTICS_DB_PASSWORD")
    ANALYTICS_DB_HOST: str = os.getenv(f"ANALYTICS_DB_HOST")
    ANALYTICS_DB_PORT: str = os.getenv(f"ANALYTICS_DB_PORT", "3306")
    ANALYTICS_DB_ENGINE: str = DB_ENGINE_MAPPER.get(ANALYTICS_DB, "postgresql")
    ANALYTICS_DB_NAME: str = os.getenv(f"ANALYTICS_DB_NAME")

    DATABASE_URI_FORMAT: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}"

    # Databases
    ANALYTICS_DATABASE_URI = DATABASE_URI_FORMAT.format(
        db_engine=ANALYTICS_DB_ENGINE,
        user=ANALYTICS_DB_USER,
        password=ANALYTICS_DB_PASSWORD,
        host=ANALYTICS_DB_HOST,
        port=ANALYTICS_DB_PORT,
        database=ANALYTICS_DB_NAME,
    )

    # find query
    PAGE = 1
    PAGE_SIZE = 20
    ORDERING = "-id"

    class Config:
        case_sensitive = True


class TestConfigs(Configs):
    ENV: str = "test"


configs = Configs()

if ENV == "prod":
    pass
elif ENV == "stage":
    pass
elif ENV == "test":
    setting = TestConfigs()

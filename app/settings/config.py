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

    PROJECT_ROOT: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        60 * 24 * 30
    )  # 60 minutes * 24 hours * 30 days = 30 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # analytics database config
    FRAUD_DB: str = os.getenv(f"FRAUD_DB", "postgresql")
    FRAUD_DB_USER: str = os.getenv(f"FRAUD_DB_USER")
    FRAUD_DB_PASSWORD: str = os.getenv(f"FRAUD_DB_PASSWORD")
    FRAUD_DB_HOST: str = os.getenv(f"FRAUD_DB_HOST")
    FRAUD_DB_PORT: str = os.getenv(f"FRAUD_DB_PORT", "5432")
    FRAUD_DB_ENGINE: str = DB_ENGINE_MAPPER.get(FRAUD_DB, "postgresql")
    FRAUD_DB_NAME: str = os.getenv(f"FRAUD_DB_NAME")

    AWS_S3_ENDPOINT_URL: str = os.getenv("MINIO_ENDPOINT")
    AWS_ACCESS_KEY_ID: str = os.getenv("MINIO_ROOT_USER")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME: str = os.getenv("AWS_STORAGE_BUCKET_NAME")

    DATABASE_URI_FORMAT: str = (
        "{db_engine}://{user}:{password}@{host}:{port}/{database}"
    )

    # Databases
    DATABASE_URI = DATABASE_URI_FORMAT.format(
        db_engine=FRAUD_DB_ENGINE,
        user=FRAUD_DB_USER,
        password=FRAUD_DB_PASSWORD,
        host=FRAUD_DB_HOST,
        port=FRAUD_DB_PORT,
        database=FRAUD_DB_NAME,
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

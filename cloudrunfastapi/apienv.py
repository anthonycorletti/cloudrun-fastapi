import sys

from pydantic import BaseSettings, Field


class ApiEnv(BaseSettings):
    DATABASE_URL: str = Field(
        ...,
        env="DATABASE_URL",
        description="Database URL (Postgresql Psycopg2 DSN).",
    )
    API_SECRET_KEY: str = Field(
        ...,
        env="API_SECRET_KEY",
        description="API secret key.",
    )
    DB_POOL_SIZE: int = Field(
        default=20,
        env="DB_POOL_SIZE",
        description="Database pool size.",
    )
    DB_MAX_OVERFLOW: int = Field(
        default=10,
        env="DB_MAX_OVERFLOW",
        description="Database pool max overflow.",
    )

    class Config:
        env_file = ".env"
        env_encoding = "utf-8"


apienv = ApiEnv()
if "pytest" in "".join(sys.argv):
    apienv = ApiEnv(_env_file=".env.test")

from pydantic import BaseModel


class SecretsConfig(BaseModel):
    DATABASE_URL: str = None
    SECRET_KEY: str = None
    DOMAIN: str = None

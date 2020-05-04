from pydantic import BaseModel


class SecretsConfig(BaseModel):
    SECRET_KEY: str = None
    DATABASE_URL: str = None

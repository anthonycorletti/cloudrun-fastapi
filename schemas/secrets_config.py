from pydantic import BaseModel


class SecretsConfig(BaseModel):
    DATABASE_URL: str = None

from pydantic import BaseModel


class SecretsConfig(BaseModel):
    SECRET_KEY: str = "thesecretsauce"
    DATABASE_URL: str = "postgresql+psycopg2://" "postgres@localhost:5432/postgres"

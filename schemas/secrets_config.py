from pydantic import BaseModel


class SecretsConfig(BaseModel):
    PROJECT_ID: str = None
    SECRET_KEY: str = 'thesecretsauce'
    DATABASE_URL: str = 'postgresql+psycopg2://postgres:localhost@/postgres'

import os
import sys

from pydantic import BaseModel


class ApiEnv(BaseModel):
    DATABASE_URL: str
    API_SECRET_KEY: str


if "pytest" in "".join(sys.argv):
    apienv = ApiEnv(
        DATABASE_URL=(
            "postgresql+psycopg2://cloud:run@127.0.0.1:5432/" "cloudrunfastapi_test"
        ),
        API_SECRET_KEY="cloudrunfastapi235",
    )
else:
    apienv = ApiEnv(  # pragma: no cover
        DATABASE_URL=os.environ["DATABASE_URL"],
        API_SECRET_KEY=os.environ["API_SECRET_KEY"],
    )

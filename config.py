import logging
import os
import sys
import time

from google.cloud import secretmanager_v1beta1 as secretmanager
from google.cloud import storage

from schemas.secrets_config import SecretsConfig

project_id = os.getenv('PROJECT_ID')
gcs_client = storage.Client()
secrets_client = secretmanager.SecretManagerServiceClient()


def get_logger():
    tz = time.strftime('%z')
    logging.config = logging.basicConfig(
        format=(f'[%(asctime)s.%(msecs)03d {tz}] '
                '[%(process)s] [%(pathname)s L%(lineno)d] '
                '[%(levelname)s] %(message)s'),
        level='INFO',
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    return logger


def build_secrets_config(project_id: str) -> SecretsConfig:
    result = SecretsConfig()
    if project_id:
        for secret_id in result.dict().keys():
            version_path = secrets_client.secret_version_path(
                project_id, secret_id, 'latest')
            secret_version = secrets_client.access_secret_version(version_path)
            result.__setattr__(secret_id,
                               secret_version.payload.data.decode('UTF-8'))
    return result


# if running in a project, cloud run or cloud build
if project_id:
    apisecrets = build_secrets_config(project_id)
    if 'pytest' in ''.join(sys.argv):
        # use the container in cloudbuild
        url = 'postgresql+psycopg2://postgres@postgres:5432/postgres_test_db'
        apisecrets.DATABASE_URL = url
# if running locally
else:
    apisecrets = build_secrets_config(project_id)
    secret_key = 'thesecretsauce'
    url = 'postgresql+psycopg2://postgres:localhost@/postgres'
    apisecrets.DATABASE_URL = url
    apisecrets.SECRET_KEY = secret_key
    if 'pytest' in ''.join(sys.argv):
        # use localhost in local env
        url = 'postgresql+psycopg2://postgres@localhost:5432/postgres_test_db'
        apisecrets.DATABASE_URL = url

import pytest
from starlette.config import environ
from starlette.testclient import TestClient

from main import api

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.
# This must also be set at runtime in order to inform our middleware of testing
environ['TESTING'] = 'True'


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = api.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    with TestClient(api) as client:
        yield client

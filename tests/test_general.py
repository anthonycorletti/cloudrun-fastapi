import gunicorn_config


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get('detail') == 'alive and kicking'


def test_gunicorn_config_worker_class():
    assert gunicorn_config.worker_class == 'uvicorn.workers.UvicornWorker'

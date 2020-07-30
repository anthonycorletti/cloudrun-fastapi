from tests.v1.factories import PubsubFactory

psf = PubsubFactory()


def test_publish_message(client):
    response = client.post("/v1/pubsub/publisher")
    assert response.status_code == 200


def test_subscription_receiver(client):
    data = psf.mock_encoded_pubsub_message({"test_key": "test_value"},
                                           "apisub")
    response = client.post("/v1/pubsub/subscriber", data=data)
    assert response.status_code == 200


def test_subscription_receiver_no_data_key(client):
    data = psf.mock_encoded_pubsub_message_no_data({"test_key": "test_value"},
                                                   "apisub")
    response = client.post("/v1/pubsub/subscriber", data=data)
    assert response.status_code == 200

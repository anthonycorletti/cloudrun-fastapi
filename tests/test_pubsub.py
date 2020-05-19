from tests.helpers import (mock_encoded_pubsub_message,
                           mock_encoded_pubsub_message_no_data)


def test_publish_message(client):
    response = client.post('/pubsub/publisher')
    assert response.status_code == 200


def test_subscription_receiver(client):
    data = mock_encoded_pubsub_message({"test_key": "test_value"}, 'apisub')
    response = client.post('/pubsub/subscriber', data=data)
    assert response.status_code == 200


def test_subscription_receiver_no_data_key(client):
    data = mock_encoded_pubsub_message_no_data({"test_key": "test_value"},
                                               'apisub')
    response = client.post('/pubsub/subscriber', data=data)
    assert response.status_code == 200

from config import project_id, publisher


class PubsubService:
    def send_message(self, topic_name: str, data: bytes) -> bool:
        result = publisher.publish(
            f"projects/{project_id}/topics/{topic_name}", data)
        return result.done()

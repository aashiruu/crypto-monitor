import json
from confluent_kafka import Producer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC


def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")


class KafkaProducer:
    def __init__(self):
        self.producer = Producer({
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "acks": "all",
            "linger.ms": 10,
        })

    def send(self, event: dict):
        self.producer.produce(
            topic=KAFKA_TOPIC,
            value=json.dumps(event),
            callback=delivery_report,
        )
        self.producer.poll(0)


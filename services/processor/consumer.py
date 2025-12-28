import json
from confluent_kafka import Consumer, Producer
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    RAW_TOPIC,
    ALERT_TOPIC,
)
from detector import detect
from metrics import (
    transactions_consumed,
    high_value_alerts,
    last_tx_value,
)


class Processor:
    def __init__(self):
        self.consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "group.id": "tx-processor-group-v2",
                "auto.offset.reset": "earliest",
            }
        )

        self.producer = Producer(
            {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
        )

        self.consumer.subscribe([RAW_TOPIC])

    def run(self):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue

            tx = json.loads(msg.value().decode())

            transactions_consumed.inc()
            last_tx_value.set(tx["value_wei"])

            alert = detect(tx)

            if alert:
                self.producer.produce(
                    ALERT_TOPIC,
                    json.dumps(alert).encode(),
                )
                self.producer.flush()
                high_value_alerts.inc()


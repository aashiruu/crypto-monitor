import json
from confluent_kafka import Consumer, Producer
from prometheus_client import Counter, Gauge
from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC,
    ALERT_TOPIC,
)
from detector import detect

transactions_consumed = Counter(
    "processor_transactions_consumed_total",
    "Total transactions consumed from Kafka",
)

high_value_alerts = Counter(
    "processor_high_value_alerts_total",
    "High-value transaction alerts triggered",
)

last_tx_value = Gauge(
    "processor_last_transaction_value_wei",
    "Value of the last processed transaction",
)

class Processor:
    def __init__(self):
        self.consumer = Consumer(
            {
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
                "group.id": "processor",
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe([KAFKA_TOPIC])

        self.producer = Producer(
            {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
        )

    def run(self):
        while True:
            msg = self.consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print(f"Kafka error: {msg.error()}")
                continue

            try:
                tx = json.loads(msg.value().decode())
            except Exception as e:
                print(f"Invalid JSON: {e}")
                continue

            # Guard against test / malformed messages
            if "value_wei" not in tx:
                print("Skipping message without value_wei")
                continue

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


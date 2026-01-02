import os

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "redpanda:9092"
)

# Consume from this topic
KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "tx.raw"
)

# Produce alerts to this topic
ALERT_TOPIC = os.getenv(
    "ALERT_TOPIC",
    "tx.alerts"
)

# High-value transaction threshold (default: 1 ETH)
HIGH_VALUE_THRESHOLD_WEI = int(
    os.getenv("HIGH_VALUE_THRESHOLD_WEI", str(10**18))
)


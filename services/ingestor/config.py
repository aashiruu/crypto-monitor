import os

# Kafka
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "redpanda:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "tx.raw"
)

# Ethereum RPC
RPC_URL = os.getenv("RPC_URL")


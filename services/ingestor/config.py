import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")

if not RPC_URL:
    raise RuntimeError("RPC_URL is not set")

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "tx.raw")

SERVICE_NAME = "tx-ingestor"


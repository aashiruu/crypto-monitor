import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"
)

RAW_TOPIC = os.getenv("RAW_TOPIC", "tx.raw")
ALERT_TOPIC = os.getenv("ALERT_TOPIC", "tx.alerts")

SERVICE_NAME = "tx-processor"

# Detection rule (simple but realistic)
HIGH_VALUE_THRESHOLD_WEI = int(
    os.getenv("HIGH_VALUE_THRESHOLD_WEI", "1000000000000000000")
)  # 1 ETH


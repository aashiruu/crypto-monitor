from prometheus_client import Counter, Gauge

blocks_processed = Counter(
    "ingestor_blocks_processed_total",
    "Total blocks processed by ingestor",
)

transactions_published = Counter(
    "ingestor_transactions_published_total",
    "Total transactions published to Kafka",
)

last_block_seen = Gauge(
    "ingestor_last_block_seen",
    "Last Ethereum block number processed",
)


from prometheus_client import Counter, Gauge

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


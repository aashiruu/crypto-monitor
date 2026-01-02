from fastapi import FastAPI
from prometheus_client import start_http_server
from blockchain import BlockchainClient
from producer import KafkaProducer
from metrics import blocks_processed, transactions_published, last_block_seen
import threading
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/healthz")
def healthz():
    return "ok"

def start_metrics_server():
    try:
        logger.info("Starting Prometheus metrics server on 0.0.0.0:9101")
        start_http_server(9101, addr='0.0.0.0')
        logger.info("Prometheus metrics server started successfully")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")
        raise

def ingest_loop():
    blockchain = BlockchainClient()
    producer = KafkaProducer()
    current_block = blockchain.latest_block()
    
    while True:
        try:
            latest = blockchain.latest_block()
            if current_block <= latest:
                block = blockchain.get_block(current_block)
                for tx in block.transactions:
                    event = {
                        "block_number": block.number,
                        "tx_hash": tx.hash.hex(),
                        "from": tx["from"],
                        "to": tx["to"],
                        "value_wei": int(tx["value"]),
                    }
                    producer.send(event)
                    transactions_published.inc()
                blocks_processed.inc()
                last_block_seen.set(block.number)
                current_block += 1
            time.sleep(1)
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            time.sleep(5)

@app.on_event("startup")
def startup():
    # Start metrics server first
    threading.Thread(target=start_metrics_server, daemon=True).start()
    # Start blockchain ingestor in background (it's a blocking loop)
    threading.Thread(target=ingest_loop, daemon=True).start()
    logger.info("All background services started")

import time
import threading
from fastapi import FastAPI
from prometheus_client import generate_latest
from blockchain import BlockchainClient
from producer import KafkaProducer
from metrics import (
    blocks_processed,
    transactions_published,
    last_block_seen,
)

app = FastAPI()

blockchain = BlockchainClient()
producer = KafkaProducer()

current_block = blockchain.latest_block()


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return generate_latest()


def ingest_loop():
    global current_block

    while True:
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


@app.on_event("startup")
def on_startup():
    thread = threading.Thread(target=ingest_loop, daemon=True)
    thread.start()


from fastapi import FastAPI
from prometheus_client import start_http_server
from consumer import Processor
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/healthz")
def healthz():
    return "ok"

def start_metrics_server():
    try:
        logger.info("Starting Prometheus metrics server on 0.0.0.0:9102")
        start_http_server(9102, addr='0.0.0.0')
        logger.info("Prometheus metrics server started successfully")
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")
        raise

def start_processor():
    processor = Processor()
    processor.run()

@app.on_event("startup")
def startup():
    # Start metrics server first
    threading.Thread(target=start_metrics_server, daemon=True).start()
    # Start processor in background (it's a blocking loop)
    threading.Thread(target=start_processor, daemon=True).start()
    logger.info("All background services started")

import threading
from fastapi import FastAPI
from prometheus_client import generate_latest
from consumer import Processor

app = FastAPI()
processor = Processor()


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return generate_latest()


@app.on_event("startup")
def start_processor():
    thread = threading.Thread(target=processor.run, daemon=True)
    thread.start()


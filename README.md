
# Crypto Monitor — Cloud-Native Blockchain Transaction Monitoring System

Crypto Monitor is a **cloud-native, production-oriented blockchain transaction monitoring system** designed to ingest on-chain data in real time, stream it through Kafka, persist checkpoints durably, and expose rich operational metrics.

The project focuses on **reliability, observability, and clean system design**, not just data collection.

---

## Key Features

- **Real-time blockchain ingestion** (Ethereum mainnet via RPC)
- **Kafka-based streaming** (Redpanda)
- **Durable checkpointing** (PostgreSQL) — safe restarts
- **Prometheus metrics** for observability
- **Fully containerized** (Docker + Docker Compose)
- **Production-style configuration** using environment variables

---

## System Architecture

High-level data flow:

1. **Ingestor Service**
   - Polls the Ethereum blockchain via RPC
   - Extracts transactions block by block
   - Publishes raw transaction events to Kafka (`tx.raw`)
   - Persists last processed block to Postgres

2. **Streaming Layer**
   - Kafka (Redpanda) buffers and streams transaction events
   - Decouples ingestion from downstream processing

3. **State & Observability**
   - PostgreSQL stores ingestion checkpoints
   - Prometheus scrapes ingestor metrics
   - Grafana visualizes system health and throughput

---

## Architecture Diagram (Logical)



┌────────────┐
│ Ethereum │
│ Blockchain │
└─────┬──────┘
│ RPC
▼
┌──────────────┐
│ Ingestor │
│ (FastAPI) │
│ │
│ - Block poll │
│ - Tx extract │
│ - Metrics │
└─────┬────────┘
│ Kafka (tx.raw)
▼
┌──────────────┐
│ Redpanda │
│ (Kafka API) │
└──────────────┘
▲
│ checkpoint
┌─────┴────────┐
│ PostgreSQL │
│ (state) │
└──────────────┘

Prometheus ──► /metrics
Grafana ──► Dashboards


---

##  Running Locally

### Prerequisites
- Docker + Docker Compose
- An Ethereum RPC endpoint (e.g. Ankr)

---

### 1 Configure environment variables

Create a `.env` file in `infra/local`:

```env
RPC_URL=https://rpc.ankr.com/eth/YOUR_API_KEY
```


### 2 Start the full system

```
cd infra/local
docker compose up -d
```

This brings up:

• Redpanda (Kafka)

• PostgreSQL

• Prometheus

• Grafana

• Ingestor service

### 3 Verify services

Health check

```
curl http://localhost:8000/healthz
```

Metrics

```
curl http://localhost:8000/metrics
```

Kafka stream

```
kafkacat -b localhost:9092 -C -t tx.raw -o beginning
```


## Metrics Exposed

The ingestor exposes Prometheus metrics such as:

• ingestor_blocks_processed_total

• ingestor_transactions_published_total

• ingestor_last_block_seen

These enable alerting and dashboards.

## Design Decisions

• Kafka over direct processing
Enables decoupling, buffering, and horizontal scaling.

• Checkpointing in Postgres
Ensures exactly-once block processing semantics across restarts.

• Metrics-first design
Observability is treated as a core feature, not an afterthought.

• Container-native
Everything runs the same locally and in production-like environments.

## Roadmap

• Planned extensions:

• Transaction processor & alerting engine

• Prometheus alert rules

• Grafana dashboards

• Kubernetes deployment

• Cloud-managed Kafka / Postgres

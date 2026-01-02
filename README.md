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
## Architecture Overview

Crypto Monitor is a local, cloud-native blockchain transaction monitoring system built with an event-driven architecture.

**Data flow:**

Ethereum RPC  
→ Ingestor service  
→ Redpanda (Kafka-compatible broker)  
→ Processor service  
→ Alerts + Metrics

**Core components:**

- **Ingestor**
  - Connects to an Ethereum RPC endpoint
  - Streams blocks and transactions
  - Publishes raw transaction events to Kafka
  - Exposes Prometheus metrics

- **Redpanda**
  - Kafka-compatible message broker
  - Handles transaction streaming between services

- **Processor**
  - Consumes transactions from Kafka
  - Detects high-value transactions
  - Emits alerts and exposes metrics

- **Prometheus**
  - Scrapes metrics from all services
  - Evaluates alerting rules

- **Grafana**
  - Visualizes system and application metrics

All components run locally using Docker Compose.

---

## Architecture Diagram (Logical)


```
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

```

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


## Observability & Monitoring

The system is fully observable using **Prometheus** and **Grafana**.

### Metrics

Each service exposes Prometheus-compatible metrics:

#### Ingestor Metrics
- `ingestor_blocks_processed_total` – total Ethereum blocks processed
- `ingestor_transactions_published_total` – transactions sent to Kafka
- `ingestor_last_block_seen` – latest block number ingested

#### Processor Metrics
- `processor_transactions_consumed_total` – transactions consumed from Kafka
- `processor_high_value_alerts_total` – number of high-value alerts generated
- `processor_last_transaction_value_wei` – value of the most recent transaction

Prometheus scrapes all metrics automatically and stores them for visualization and alerting.

## Alerting

Alerting is implemented using **Prometheus alert rules**.

Current alerts include:
- **IngestorDown** – triggers when the ingestor is unavailable
- **ProcessorDown** – triggers when the processor is unavailable
- **NoTransactionsProcessed** – triggers when no transactions are consumed for a defined period

Alerts are evaluated continuously by Prometheus and can be routed to external systems (Slack, email, PagerDuty) if desired.

## Access services

Grafana: http://localhost:3000

Prometheus: http://localhost:9090

Ingestor metrics: http://localhost:9101/metrics

Processor metrics: http://localhost:9102/metrics

An Ethereum RPC URL must be provided via environment variable:

```
RPC_URL=https://your-ethereum-rpc-endpoint
```


---

# ✅ 5️⃣ Screenshots Section (exact text)

## Screenshots

### Grafana Dashboard
<img width="1366" height="652" alt="image" src="https://github.com/user-attachments/assets/00cba621-ea30-424a-b73c-3b3aa287f970" />

### Ingestor Metrics
<img width="558" height="265" alt="image" src="https://github.com/user-attachments/assets/1f97a6ea-66f3-4ba9-bcff-088fc71c7341" />

### Processor Metrics
<img width="558" height="269" alt="image" src="https://github.com/user-attachments/assets/5fc32c44-524b-4b42-98cf-74add3f6734b" />

### Prometheus Targets
<img width="1366" height="687" alt="image" src="https://github.com/user-attachments/assets/3b00da21-681f-4592-9a22-64ae82fa896d" />


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

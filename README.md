# AI-Powered Worker Productivity Dashboard

## Overview

Note: I took help from Chatgpt while doing this assignment.

This project is a production-style full-stack web application that simulates how a manufacturing factory can use AI-powered CCTV systems to monitor worker activity and compute productivity metrics.

The system ingests structured AI-generated events, stores them in a database, computes time-based and production-based metrics, and displays them in a clear dashboard for factory monitoring.

No computer vision or machine learning models are built in this project. The focus is on event ingestion, metric computation, system design, and scalability.

## Live Demo & Repository

**Live Web Application:**
https://ai-worker-productivity-dashboard.vercel.app

**Backend API (Swagger):**
https://ai-worker-productivity-dashboard-g2ji.onrender.com/docs

**GitHub Repository:**
https://github.com/Sdhandre/Ai-worker-productivity-dashboard


## Edge → Backend → Dashboard Architecture

### High-Level Flow
AI CCTV Cameras (Edge)
↓
Structured Events (JSON)
↓
FastAPI Backend
↓
SQLite Database
↓
Metrics Computation
↓
React Dashboard


### Explanation

- **Edge (AI CCTV System)**  
  Computer vision models running on cameras generate structured events such as:
  - `working`
  - `idle`
  - `absent`
  - `product_count`

- **Backend (FastAPI)**  
  - Ingests events via REST APIs  
  - Stores all raw events  
  - Computes productivity metrics dynamically  
  - Exposes metrics via APIs  

- **Dashboard (React)**  
  - Fetches metrics from backend APIs  
  - Displays factory, worker, and workstation metrics  
  - Supports filtering by worker and workstation  

---

## Database Schema

### Workers
| Field | Type |
|------|------|
| worker_id | String (PK) |
| name | String |

### Workstations
| Field | Type |
|------|------|
| station_id | String (PK) |
| name | String |

### Events
| Field | Type |
|------|------|
| id | Integer (PK) |
| timestamp | DateTime |
| worker_id | String (FK) |
| workstation_id | String (FK) |
| event_type | String |
| confidence | Float |
| count | Integer (for product_count) |

📌 All metrics are **derived from events**, not stored explicitly.

---

## Metric Definitions

### Worker-Level Metrics
- **Working Time:** Time spent in `working` state
- **Idle Time:** Time spent in `idle` state
- **Utilization %:**  
  `working_time / (working_time + idle_time)`
- **Total Units Produced:** Sum of `product_count`
- **Units per Hour:**  
  `total_units / working_time (hours)`

---

### Workstation-Level Metrics
- **Occupancy Time:** Time workstation is occupied (`working`)
- **Utilization %:**  
  `occupancy_time / (occupancy_time + idle_time)`
- **Total Units Produced**
- **Throughput Rate:** Units per hour of occupancy

---

### Factory-Level Metrics
- **Total Productive Time**
- **Total Production Count**
- **Average Utilization across workers**
- **Average Production Rate**

---

## Assumptions & Tradeoffs

- Events represent **state transitions**, and a state lasts until the next event.
- `product_count` events contribute to production but do not represent time.
- Events are sorted by timestamp before metric computation.
- SQLite is used for simplicity and can be replaced by PostgreSQL for scale.
- Demo data is **auto-seeded on startup** if the database is empty to avoid empty dashboards.

---

## Handling Real-World Challenges

### Intermittent Connectivity
- Events are timestamped and append-only.
- Cameras can send events later when connectivity is restored.
- Metrics rely on timestamps, not arrival order.

---

### Duplicate Events
- Events can be deduplicated using `(timestamp, worker_id, event_type)`.
- Time-based aggregation minimizes duplicate impact.

---

### Out-of-Order Timestamps
- Events are sorted before computation.
- Arrival order does not affect results.

---

## Model Lifecycle (Conceptual)

### Model Versioning
- Events can include a `model_version` field.
- Metrics can be filtered by model version for comparison.

---

### Detecting Model Drift
- Monitor changes in:
  - Idle time
  - Utilization
  - Production rate
  - Confidence scores

---

### Triggering Retraining
- Drift thresholds trigger retraining pipelines.
- New models are deployed gradually.

---

## Scalability

### 5 Cameras → 100+ Cameras
- Stateless backend enables horizontal scaling.
- Replace SQLite with PostgreSQL.
- Introduce message queues (Kafka / RabbitMQ).

### Multi-Site Expansion
- Add `site_id` and `camera_id` to events.
- Aggregate metrics per site.
- Deploy region-specific backends if required.

---

## Containerization & Local Setup

### Prerequisites
- Docker
- Docker Compose

### Run Locally

```bash
git clone https://github.com/Sdhandre/Ai-worker-productivity-dashboard
cd ai-worker-productivity-dashboard
docker compose up --build

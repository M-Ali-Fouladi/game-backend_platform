# Multiplayer Game Backend Platform

A cloud-native multiplayer game backend platform built with a microservices architecture. This project demonstrates backend engineering, distributed systems, real-time communication, observability, and infrastructure skills commonly used in modern online gaming platforms.

## Overview

This project is not a game itself. It is the backend infrastructure that powers multiplayer online games.

Features include:

* Player Management
* Rank & XP System
* Matchmaking System
* Real-Time Leaderboard
* Telemetry Event Processing
* WebSocket Live Updates
* Containerized Deployment
* Monitoring & Observability

---

## Architecture

```text
                        +----------------+
                        |   API Clients  |
                        +--------+-------+
                                 |
                                 v
                     +----------------------+
                     |   FastAPI Services   |
                     +----------------------+

     +----------------+----------------+----------------+
     |                |                |                |
     v                v                v                v

+------------+ +-------------+ +-------------+ +-------------+
|   Player   | | Matchmaking | | Leaderboard | | Telemetry   |
|  Service   | |   Service   | |   Service   | |   Service   |
+------------+ +-------------+ +-------------+ +-------------+

        \            |             |             /
         \           |             |            /
          \          |             |           /
           +----------------------------------+
           |              Redis               |
           +----------------------------------+

                     +----------------+
                     | PostgreSQL     |
                     +----------------+

                     +----------------+
                     | WebSocket Hub  |
                     +----------------+

                     +----------------+
                     | Prometheus     |
                     +----------------+

                     +----------------+
                     | Grafana        |
                     +----------------+
```

---

## Tech Stack

### Backend

* FastAPI
* Python 3.11
* SQLAlchemy
* Pydantic

### Data Layer

* PostgreSQL
* Redis
* Redis Streams
* Redis Sorted Sets

### Infrastructure

* Docker
* Docker Compose

### Monitoring

* Prometheus
* Grafana

### Communication

* REST API
* WebSocket

---

## Services

### Player Service

Responsible for:

* Player Registration
* Profile Management
* XP Tracking
* MMR Tracking

Endpoints:

```http
POST   /players
GET    /players/{id}
PATCH  /players/{id}/xp
PATCH  /players/{id}/mmr
```

---

### Matchmaking Service

Responsible for:

* Queue Management
* MMR-Based Matching
* Match Creation

Features:

* Redis Sorted Set Queue
* Background Match Worker
* Match Events

Example:

```text
Player A (1200 MMR)
Player B (1250 MMR)

→ Match Created
```

---

### Leaderboard Service

Responsible for:

* Global Rankings
* Top Players Retrieval

Redis Sorted Set:

```redis
ZADD leaderboard 1500 player_1
ZADD leaderboard 1800 player_2
```

Top 100:

```redis
ZREVRANGE leaderboard 0 99
```

---

### Telemetry Service

Responsible for collecting game events.

Example Event:

```json
{
  "player_id": 1,
  "event": "kill"
}
```

Events are stored in Redis Streams and exposed through Prometheus metrics.

---

### WebSocket Service

Provides:

* Match Notifications
* Leaderboard Updates
* Real-Time Event Delivery

WebSocket Endpoint:

```text
/ws/leaderboard
```

---

## Monitoring

### Prometheus

Collected Metrics:

```text
players_registered_total
matches_created_total
telemetry_events_total
```

---

### Grafana Dashboards

Example Panels:

* Registered Players
* Match Creation Rate
* Telemetry Events
* Leaderboard Activity

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/your-username/game-backend-platform.git

cd game-backend-platform
```

### Configure Environment

```bash
cp .env.example .env
```

### Start Services

```bash
docker compose up --build
```

---

## Service Ports

| Service             | Port |
| ------------------- | ---- |
| Player Service      | 8000 |
| Matchmaking Service | 8002 |
| Leaderboard Service | 8003 |
| WebSocket Service   | 8004 |
| Telemetry Service   | 8005 |
| Prometheus          | 9090 |
| Grafana             | 3000 |
| PostgreSQL          | 5432 |
| Redis               | 6379 |

---

## Example Workflow

### 1. Create Players

```http
POST /players
```

### 2. Join Matchmaking Queue

```http
POST /matchmaking/join
```

### 3. Match Created

```json
{
  "type": "match_created",
  "players": [1, 2]
}
```

### 4. Leaderboard Updated

```http
GET /leaderboard/top
```

### 5. Real-Time Notification

```text
ws://localhost:8004/ws/leaderboard
```

---

## Project Goals

This project was built to demonstrate:

* Distributed Systems Design
* Event-Driven Architecture
* Real-Time Communication
* Backend Engineering
* DevOps Fundamentals
* Observability
* Cloud-Native Development

---

## Future Improvements

* Kafka Integration
* Kubernetes Deployment
* ArgoCD GitOps
* OpenTelemetry Tracing
* JWT Authentication
* Match History Service
* Anti-Cheat Event Processing
* Multi-Region Support

---

## License

MIT License

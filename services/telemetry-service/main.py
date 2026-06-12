from fastapi import FastAPI
from pydantic import BaseModel
from redis_client import redis_client
from prometheus_client import Counter
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import generate_latest
import json

app = FastAPI()

STREAM_NAME = "telemetry-stream"

telemetry_events_total = Counter(
    "telemetry_events_total",
    "Total telemetry events"
)
class TelemetryEvent(BaseModel):
    player_id: int
    event: str

@app.post("/telemetry/event")
def create_event(payload: TelemetryEvent):
    telemetry_events_total.inc()
    redis_client.xadd(
        STREAM_NAME,
        {
            "player_id": str(payload.player_id),
            "event": payload.event
        }
    )
    return {
        "status": "accepted"
    }

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
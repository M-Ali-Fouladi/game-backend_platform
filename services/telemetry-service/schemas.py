from pydantic import BaseModel


class TelemetryEvent(BaseModel):
    player_id: int
    event: str
from pydantic import BaseModel

class PlayerJoin(BaseModel):
    player_id: int
    mmr: int
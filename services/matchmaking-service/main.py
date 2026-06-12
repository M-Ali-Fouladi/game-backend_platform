from fastapi import FastAPI
import schemas 
from redis_utils import redis_client
import threading
from worker import run_worker
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response

threading.Thread(target=run_worker, daemon=True).start()

app = FastAPI()

QUEUE_KEY = "matchmaking_queue"

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
#-------------------join matchmaking---------------
@app.post("/matchmaking/join")
def join_matchmaking(player: schemas.PlayerJoin):
    redis_client.zadd(
        QUEUE_KEY,
        {
            str(player.player_id): player.mmr
        }
    )
    return {
        "message": "joined queue",
        "player_id": player.player_id,
        "mmr": player.mmr
    }
  
#---------------Leave Queue------------------
@app.post("/matchmaking/leave")
def leave_matchmaking(player_id: int):

    redis_client.zrem(QUEUE_KEY, player_id)

    return {"message": "left queue"}
from fastapi import FastAPI
import redis
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

LEADERBOARD_KEY = "leaderboard"

@app.get("/leaderboard/top")
def top_leaderboard(limit: int = 100):
    top = r.zrevrange(LEADERBOARD_KEY, 0, limit - 1, withscores=True)
    return [{"player_id": pid, "mmr": int(score)} for pid, score in top]

def create_match(p1, p2):
    match = {
        "type": "match_created",
        "players": [p1, p2]
    }

    # Publish event to Redis Stream
    r.xadd("events", match)

    print("MATCH CREATED:", match)
    
import redis
import json

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True,
    socket_timeout=None,
    socket_connect_timeout=10,
    retry_on_timeout=True
)

LEADERBOARD_KEY = "leaderboard"

last_id = "$"

print("Leaderboard worker started...", flush=True)

while True:
    try:
        messages = r.xread(
            {"events": last_id},
            block=5000
        )

        if not messages:
            continue

        for stream_name, events in messages:
            for event_id, data in events:

                last_id = event_id

                if data.get("type") == "match_created":

                    players = json.loads(data["players"])

                    for pid in players:
                        r.zincrby("leaderboard", 10, pid)

                    print("Leaderboard updated:", players, flush=True)

    except Exception as e:
        print("Worker error:", e, flush=True)
        continue
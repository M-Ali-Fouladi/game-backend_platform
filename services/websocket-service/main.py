from fastapi import FastAPI, WebSocket
import redis
import json
import asyncio

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.websocket("/ws/leaderboard")
async def ws_leaderboard(ws: WebSocket):
    await ws.accept()

    last_id = "0"

    try:
        while True:

            messages = r.xread(
                {"events": last_id},
                block=5000
            )

            for stream_name, events in messages:
                for event_id, data in events:

                    last_id = event_id

                    # فقط event های match
                    if data.get("type") == "match_created":

                        # players از string → list
                        players = json.loads(data["players"])

                        await ws.send_json({
                            "type": "match_created",
                            "players": players
                        })

    except Exception as e:
        print("WS error:", e)
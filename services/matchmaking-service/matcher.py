import time
import json
from redis_utils import redis_client
from prometheus_client import Counter

matches_created_total = Counter(
    "matches_created",
    "Total matches created"
)
QUEUE_KEY = "matchmaking_queue"

#-----------------------Mactching_logic----------------
def get_queue():
    return redis_client.zrange(
        QUEUE_KEY,
        0,
        -1,
        withscores=True
    )

#-------------------pairing_system--------------------
def find_matches():
    players = get_queue()
    #print("QUEUE:", players, flush=True)
    matched = set()

    for i in range(len(players)):

        p1_id, p1_mmr = players[i]

        if p1_id in matched:
            continue

        for j in range(i + 1, len(players)):

            p2_id, p2_mmr = players[j]

            if p2_id in matched:
                continue

            if abs(p1_mmr - p2_mmr) <= 100:

                create_match(p1_id, p2_id)

                matched.add(p1_id)
                matched.add(p2_id)

                break
#------------------Create_match_event-----------------------
def create_match(p1, p2):
    matches_created_total.inc()
    match = {
        "type": "match_created",
        "players": json.dumps([p1, p2])
    }

    redis_client.xadd("events", match)

    print("MATCH CREATED:", match, flush=True)
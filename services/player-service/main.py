from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
import crud
import schemas
import models
from database import (
    Base,
    engine,
    get_db
)
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
from prometheus_client import Counter
players_registered_total = Counter(
    "players_registered_total",
    "Total players registered"
)


app = FastAPI()
import time

for attempt in range(30):
    try:
        with engine.connect():
            print("Database connected")
        break
    except Exception as e:
        print(f"Waiting for database... {attempt + 1}/30")
        time.sleep(2)

Base.metadata.create_all(bind=engine)

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.get("/health")
def health():
    return {"status": "ok"}
#---------------------create_player-------------------
@app.post(
    "/players",
    response_model=schemas.PlayerResponse
)
def create_player(player: schemas.PlayerCreate,db: Session = Depends(get_db)):
    players_registered_total.inc()
    return crud.create_player(
        db,
        username=player.username,
        email=player.email
    )
#-----------------------Get_player--------------------
@app.get(
    "/players/{player_id}",
    response_model=schemas.PlayerResponse
)
def get_player(
    player_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_player(
        db,
        player_id
    )
#-----------------------Add_XP---------------------
@app.patch(
    "/players/{player_id}/xp",
    response_model=schemas.PlayerResponse
)
def add_xp(
    player_id: int,
    payload: schemas.XPUpdate,
    db: Session = Depends(get_db)
):
    return crud.add_xp(
        db,
        player_id,
        payload.amount
    )
#----------------------Update_MMR-----------------
@app.patch(
    "/players/{player_id}/mmr",
    response_model=schemas.PlayerResponse
)
def update_mmr(
    player_id: int,
    payload: schemas.MMRUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_mmr(
        db,
        player_id,
        payload.amount
    )